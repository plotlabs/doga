import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from admin.aws_config import *


def create_requirements(db_engine: str, parent_dir, target_dir):

    s = parent_dir + '/common_requirements.txt'
    d = target_dir + '/requirements.txt'
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(s, d)

    file = open(d, 'a+')

    if db_engine == 'postgres':
        specific = parent_dir + '/postgres_requirements.txt'
        file.write(specific.read())
    if db_engine == 'mysql':
        specific = parent_dir + '/mysql_requirements.txt'
        file.write(specific.read())

    s.close()
    d.close()
    specific.close()


def create_dockerfile(PORT, parent_dir, target_dir):
    # open dockerfile template
    Dockerfile = open('templates/export/Dockerfile', 'r')
    Dockerfile_contents = Dockerfile.read()
    Dockerfile_contents = Dockerfile_contents.replace('PORT', PORT)

    # create Dockerfile
    exported_Dockerfile = open(target_dir, 'a+')
    exported_Dockerfile.write(Dockerfile_contents)

    exported_Dockerfile.close()
    Dockerfile.close()


def export_blueprints(app_name, parent_dir, target_dir):
    contents = open(parent_dir, 'r').readlines()
    to_write = open(target_dir, 'a+')

    i = 1
    for line in contents:
        if i in [1, 2]:
            to_write.write(line)
            continue
        if i in [3, 4]:
            continue
        else:
            for app_name in line:
                to_write.write(line)
                continue
        i+=1

    to_write.close()
    return


def create_aws_config(**kwargs):
    region_name = kwargs.get('region_name', region_name)
    signature_version = kwargs.get('val2', signature_version)
    max_attempts = kwargs.get('val2', max_attempts)
    mode = kwargs.get('mode', mode)

    try:
        aws_config = Config(
            region_name=region_name,
            signature_version=signature_version,
            retries={
                'max_attempts': max_attempts,
                'mode': mode
            }
        )
        return aws_config
    except BotoCoreError:
        return {'result': 'An error occured while trying to create the config'}


def create_RDS(config_args={}, **kwargs):
    """
    Default Values:

    """
    try:
        # these are defined in DOGA while creation of app
        DBName = kwargs['DBName']
        Engine = kwargs['Engine']
        MasterUsername = kwargs['MasterUsername']
        MasterUserPassword = kwargs['MasterUserPassword']
        # DBSecurityGroups = kwargs['DBSecurityGroups']

        # from user while exporing
        # REQUIRED
        DBInstanceIdentifier = kwargs['DBInstanceIdentifier']
        MaxAllocatedStorage = int(kwargs['MaxAllocatedStorage'])

        # Optional
        DBInstanceClass = kwargs.get('DBInstanceClass', 'db.t2.micro')
        DeletionProtection = kwargs.get('DeletionProtection', False),
        EnableIAMDatabaseAuthentication = kwargs('EnableIAMDatabaseAuthentication', False)  # noqa 401
        EnablePerformanceInsights = kwargs('EnablePerformanceInsights', False)
        MultiAZ = kwargs.get('MultiAZ', False)
        PubliclyAccessible = kwargs.get('PubliclyAccessible', False)
        PerformanceInsightsKMSKeyId = kwargs.get(
            'PerformanceInsightsKMSKeyId', '')
        # TODO: what should be the default
        # EnableCloudwatchLogsExports = kwargs.get()

    except KeyError as e:
        return {"result": "Key error", "error": str(e)}, 500

    except TypeError as e:
        return {"result": "Type error", "error": str(e)}, 500

    try:
        rds_client = boto3.client('rds',
                                  aws_access_key_id=aws_access_key,
                                  aws_secret_access_key=aws_secret_key,
                                  region_name=aws_config.region_name,
                                  config=create_aws_config(config_args)
                                  )

        response = rds_client.create_db_instance(
            DBInstanceIdentifier="testDB",
            DBInstanceClass="db.t2.micro",
            Engine="MySQL",
            DBName="test_db",
            MasterUsername="admin",
            MasterUserPassword="password",
            AllocatedStorage=20,
        )
    #                                **kwargs,
    # )
        return response

    except ClientError as e:
        return {"result": "Error creating RDS with given kwags",
                "error": str(e)}, 500


def create_EC2(config_args={}, **kwargs):
    try:
        ec2 = boto3.resource('ec2', config_args)
        BlockDeviceMappings = kwargs['BlockDeviceMappings']
        ImageId = kwargs['ImageId']
        InstanceType = kwargs['InstanceType']
        SecurityGroups = kwargs['SecurityGroups']

        # Optional
        MaxCount = kwargs.get('MaxCount', 1)
        MinCount = kwargs('MinCount', 1)
        KeyName = kwargs.get('KeyName', ''),
        Monitoring = kwargs('Monitoring', False)  # noqa 401

    except KeyError as err:
        return {"result": "Key error", "error": str(e)}, 500

    # TODO: fix this
    ec2_instance = ec2.create_instances(
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/sda1',
                'Ebs': {

                    'DeleteOnTermination': True,
                    'VolumeSize': 8,
                    'VolumeType': 'gp2'
                },
            },
        ],
        ImageId='ami-0885b1f6bd170450c',
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        Monitoring={
            'Enabled': False
        },
        SecurityGroups=[
            'launch-wizard-2',
        ],
        KeyName='test1'
    )

    ID = instance[0].id
    instance = ec2.Instance(ID)
    return instance
