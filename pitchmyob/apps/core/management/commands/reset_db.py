import time

import boto3
from botocore.exceptions import ClientError

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Delete the current db instance and replace it by a new one'

    db_instance_identifier = 'v2-backend-dev'
    db_name = 'pitchdev'
    db_username = 'pitch'
    db_user_password = 'vbH456jE'
    sleep_time = 8

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.client = boto3.client('rds')

    def get_describe_db_instance(self):
        response = self.client.describe_db_instances(DBInstanceIdentifier=self.db_instance_identifier)

        db_instances = response['DBInstances']
        if len(db_instances) != 1:
            raise Exception('More than one DB instance returned')

        return db_instances[0]

    def handle(self, *args, **options):
        self.stdout.write('> Delete old DBInstance')

        try:
            self.client.delete_db_instance(DBInstanceIdentifier=self.db_instance_identifier, SkipFinalSnapshot=True)
        except ClientError as e:
            if 'DBInstanceNotFound' in str(e):
                self.stderr.write('DBInstance {} not found'.format(self.db_instance_identifier))
            elif 'InvalidDBInstanceState' in str(e):
                self.stderr.write('Instance {} is already being deleted'.format(self.db_instance_identifier))
            else:
                raise
        else:
            self.stdout.write(self.style.SUCCESS('Instance {} is being deleted'.format(self.db_instance_identifier)))

        self.stdout.write('\n> Create new DBInstance')

        running_create = True
        while running_create:
            try:
                self.client.create_db_instance(
                    DBInstanceIdentifier=self.db_instance_identifier,
                    DBName=self.db_name,
                    AllocatedStorage=5,
                    StorageType='standard',
                    DBInstanceClass='db.t2.micro',
                    Engine='postgres',
                    MasterUsername=self.db_username,
                    MasterUserPassword=self.db_user_password,
                    VpcSecurityGroupIds=['sg-446c7e23'],
                    MultiAZ=False,
                    EngineVersion='9.6.1',
                )
            except ClientError as e:
                if 'DBInstanceAlreadyExists' in str(e):
                    db_instance = self.get_describe_db_instance()
                    self.stdout.write('Last DB status : {}...'.format(db_instance['DBInstanceStatus']))
                    time.sleep(self.sleep_time)
                else:
                    raise
            else:
                running_create = False

        running_describe = True
        while running_describe:
            db_instance = self.get_describe_db_instance()
            status = db_instance['DBInstanceStatus']

            self.stdout.write('Last DB status : {}...'.format(status))

            if status == 'available':
                running_describe = False

                endpoint = db_instance['Endpoint']
                host = endpoint['Address']

                self.stdout.write(self.style.SUCCESS('DB instance ready with host : {}'.format(host)))
            else:
                time.sleep(self.sleep_time)
