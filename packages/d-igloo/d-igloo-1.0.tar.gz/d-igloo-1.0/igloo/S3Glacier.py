#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import json

import boto3
import math
import re
import os
from botocore.exceptions import ClientError
from igloo import __dice_projects_prefixes__

MANDATORY_REGION = 'eu-west-3'
AWS_ARN_PATTERN = R"^arn:(?P<Partition>[^:\n]*):" \
                  R"(?P<Service>[^:\n]*):" \
                  R"(?P<Region>[^:\n]*):" \
                  R"(?P<AccountID>[^:\n]*):" \
                  R"(?P<Ignore>(?P<ResourceType>[^:\/\n]*)[:\/])?(?P<Resource>.*)$"

"""
Convert bytes to human readable storage size
"""
def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


class S3Glacier:
    def __init__(self, bucket_name: str):
        self._bucket_name = bucket_name
        self._session = boto3.session.Session()
        self._s3 = self._session.resource('s3')

        try:
            self._s3.meta.client.head_bucket(Bucket=bucket_name)
        except ClientError as err:
            raise RuntimeError(f"Bucket {bucket_name} not found")

        self._bucket = self._s3.Bucket(bucket_name)

    @property
    def bucket_name(self):
        return self._bucket_name

    @property
    def bucket(self):
        return self._bucket

    @property
    def account_id(self):
        sts = boto3.client('sts')
        return sts.get_caller_identity()['Account']

    def get_projects(self):
        projects = dict()

        # FIXME: avec cette regex, on ne verra que les fichiers avec suffix .tar.gz !!!
        pattern = r'projects/(?P<project_code>.+)/(?P<filename>(?:.+).tar.gz)'
        for obj_summary in self._bucket.objects.all():
            groups = re.match(pattern, obj_summary.key)
            try:
                project_code = groups['project_code']
            except IndexError:
                continue

            if project_code not in projects:
                obj = self._bucket.Object(obj_summary.key)
                projects[project_code] = {
                    'nb_files': 0,
                    'total_size_in_bytes': 0,
                    'files': [],
                    'project_description': obj.metadata['project_description'],
                    'client': obj.metadata['client'],
                }

            # Get the real object
            obj = self._bucket.Object(obj_summary.key)

            projects[project_code]['nb_files'] += 1
            projects[project_code]['total_size_in_bytes'] += obj_summary.size
            projects[project_code]['files'].append(
                {
                    'filename': os.path.basename(obj.key),
                    'project': project_code,
                    'key': obj.key,
                    'last_modified': str(obj.last_modified),
                    'size_in_bytes': obj.content_length,
                    'storage_class': obj.storage_class,
                    'project_description': obj.metadata['project_description'],
                    'client': obj.metadata['client'],
                    'file_description': obj.metadata['file_description'],
                }
            )

        return projects

    def _get_normalized_sns_topic_name(self):
        return f"{self._bucket_name}-sns-topic"

    def get_bucket_topic(self):
        sns = self._session.resource('sns')
        topic_name = self._get_normalized_sns_topic_name()

        bucket_topic = None
        for topic in sns.topics.all():
            if re.match(AWS_ARN_PATTERN, topic.arn)["Resource"] == topic_name:
                bucket_topic = topic
                break

        if bucket_topic is None:
            # No topic associated with this bucket, creating it with proper name
            print(f"No topic with name {topic_name} were found. We just created it...")

            bucket_topic = sns.create_topic(Name=topic_name)

            # https://stackoverflow.com/questions/49961491/using-boto3-to-send-s3-put-requests-to-sns

            # Set topic policy to accept s3 events
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Client.set_topic_attributes
            sns_topic_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "sns:Publish",
                        "Resource": bucket_topic.arn,
                        "Condition": {
                            "ArnLike": {"AWS:SourceArn": f"arn:aws:s3:*:*:{self._bucket_name}"},
                        },
                    },
                ],
            }

            bucket_topic.set_attributes(
                AttributeName='Policy',
                AttributeValue=json.dumps(sns_topic_policy)
            )

            # Set notification config
            notification = self._bucket.Notification()

            notification.put(NotificationConfiguration={
                'TopicConfigurations': [
                    {
                        'TopicArn': bucket_topic.arn,
                        'Events': [  # s3 Events we want to trig notification
                            's3:ObjectCreated:*',
                            's3:ObjectRemoved:*',
                            's3:ObjectRestore:*',
                        ]
                    }
                ]
            }
            )

        return bucket_topic

    def subscribe_to_bucket_notifications(self, email: str):
        # 1- on veut recuperer le topic associe a ce bucket
        bucket_topic = self.get_bucket_topic()

        # Getting subscriptions
        for subscription in bucket_topic.subscriptions.all():
            if subscription.arn == 'PendingConfirmation':
                continue

            if subscription.attributes['Endpoint'] == email:
                return None

        subscription = bucket_topic.subscribe(Protocol='email', Endpoint=email)

        return subscription

    def list_subscriptions(self):
        bucket_topic = self.get_bucket_topic()

        subscriptions = list()
        for subscription in bucket_topic.subscriptions.all():
            if subscription.arn == 'PendingConfirmation':
                subscriptions.append('Pending Subscription')

            else:
                subscriptions.append(subscription.attributes['Endpoint'])

        return subscriptions

    def remove_subscription(self, email: str):
        bucket_topic = self.get_bucket_topic()

        subscription_to_delete = None
        for subscription in bucket_topic.subscriptions.all():
            if subscription.arn == 'PendingConfirmation':
                continue

            if subscription.attributes['Endpoint'] == email:
                subscription_to_delete = subscription

        if subscription_to_delete is not None:
            subscription_to_delete.delete()
            print(f'This subscription is deleted')
        else:
            print(f'\t> Email address {email} was not subscribing to the bucket notifications')

    def upload_file(self,
                    project: str,
                    file: str,
                    file_description: str,
                    client: str,
                    project_description: str,
                    no_prompt=False):

        # Does the file is a file (no directory allowed).
        if not os.path.isfile(file):
            if os.path.isdir(file):
                raise RuntimeError(f"{file} is a directory. Only files are allowed for upload")
            raise RuntimeError(f"{file} not found")

        # TODO: tester si project est valide (RDX, SCE etc...)
        pattern = "^(" + "|".join(__dice_projects_prefixes__) + ")[0-9]{3}$"
        if not bool(re.match(pattern, project)):
            raise RuntimeError(f"Projects names must have the following form: <prefix><number> where "
                               f"prefix is in {__dice_projects_prefixes__} and "
                               f"number is a 3-digit number referencing the project number."
                               f"\nExample: SCE072")
        filename = os.path.basename(file)
        key = f"projects/{project}/{filename}"

        # TODO: tester si on a pas deja la cle...
        projects = self.get_projects()
        if project in projects:
            print(f"{project} is an existing project")
            # We get client and project_description from existing project file and do not use command line options...
            client = projects[project]['client']
            project_description = projects[project]['project_description']

            # TODO: tester si on a specifie client ou project_description et dire que c'est pas utilise...

            # Testing if there is not already a file with the same name...
            project_files = projects[project]['files']
            for file_ in project_files:
                if file_['filename'] == filename:
                    raise RuntimeError(f'In project {project}, a file {filename} already exist.'
                                       f'\nBefore re-uploading this file, please ask an admin to remove it')

        else:
            print(f"{project} is a new project")

            if client == '' or  project_description == '':
                raise RuntimeError(f"{project} is a new project. Client and project_description cannot be empty")

        print(f"\tClient:              {client}")
        print(f"\tProject description: {project_description}")

        print(f"Uploading file:")
        print(f"\tBucket:           {self._bucket_name}")
        print(f"\tKey:              {key}")
        print(f"\tFile:             {file}")
        print(f"\tSize:             {convert_size(os.stat(file).st_size)}")
        print(f"\tFile Description: {file_description}")

        # It is here that it is specified that we will use a deep archive storage class
        ExtraArgs = {
            'Metadata': {
                'project': project,
                'client': client,
                'project_description': project_description,
                'file_description': file_description,

            },
            'StorageClass': 'DEEP_ARCHIVE'
        }

        if not no_prompt:
            print("Please review the information above. Is that correct?")
            answer = input('Proceed? [yes/no] default no\n> ')

            if answer != 'yes':
                print("File has not been uploaded")
                return

        self._bucket.upload_file(file, key, ExtraArgs=ExtraArgs)

    def download_file(self, key: str, output_dir: str):

        file = os.path.basename(key)

        # Where to download the file?
        target = os.path.join(output_dir, file)
        print(target)

        try:
            self._bucket.download_file(key, target)  # plante si deep archive...
            return

        except ClientError:
            # File was not available to download, sending restore request
            s3_object = self._bucket.Object(key)
            s3_object.restore_object(
                RestoreRequest={
                    # We've got 7 days to download the file. After this delay, a new restore request will be necessary
                    'Days': 7
                }
            )

            print("\t> Object is not accessible yet. Restoring it. The file will be available in a few hours.")
