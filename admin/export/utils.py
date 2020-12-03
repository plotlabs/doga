import os

import boto3
from botocore.config import Config
from botocore.exceptions import (BotoCoreError, ClientError,
                                 ParamValidationError)

from requests import get

import shutil

from time import sleep

from admin.aws_config import *
from admin.export.errors import *
from admin.utils import extract_database_name

from dbs import DB_DICT

KEY_NAME = 'doga_key'


def get_current_ip() -> str:
    ip = get('https://api.ipify.org').text
    return ip


def create_requirements(db_engine: str, parent_dir, target_dir):

    s = parent_dir + '/common_requirements.txt'
    d = target_dir + '/requirements.txt'
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(s, d)

    file = open(d, 'a+')

    if db_engine == 'postgres':
        specific = parent_dir + '/postgres_requirements.txt'
        file.write(open(specific, 'r').read())
    if db_engine == 'mysql':
        specific = parent_dir + '/mysql_requirements.txt'
        file.write(open(specific, 'r').read())

    file.close()


def create_dockerfile(PORT, parent_dir, target_dir):
    # open dockerfile template
    Dockerfile = open('templates/export/Dockerfile', 'r')
    Dockerfile_contents = Dockerfile.read()
    Dockerfile_contents = Dockerfile_contents.replace('PORT', str(PORT))

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
        i += 1

    to_write.close()
    return


def create_dbs_file(app_name, destination, rds, user_credentials, aws_config):

    to_write = open(destination, 'a+')

    for connection, string in DB_DICT.items():
        for app_name in string:
            connection_string = string
            break

    try:
        rds_client = boto3.client('rds',
                                  aws_access_key_id=user_credentials['aws_access_key'],  # noqa 401
                                  aws_secret_access_key=user_credentials['aws_secret_key'],  # noqa 401
                                  region_name=aws_config.region_name,
                                  config=aws_config
                                  )

        waiter = rds_client.get_waiter('db_instance_available')
        waiter.wait(
            DBInstanceIdentifier=rds["DBInstance"]["DBInstanceIdentifier"])

        rds_instance = rds_client.describe_db_instances(
            DBInstanceIdentifier=rds["DBInstance"]["DBInstanceIdentifier"]
            )['DBInstances'][0]

    except ClientError as error:
        raise DogaDirectoryCreationError(str(error))

    engine = rds_instance['Engine']
    username = rds_instance['MasterUsername']
    password = 'password'
    # password = rds_instance['PendingModifiedValues']['MasterUserPassword']
    server = rds_instance['Endpoint']['Address']
    port = str(rds_instance['Endpoint']['Port'])

    string = engine + '://' + username + ':' + password + '@' + server + ':' + port + '/' + app_name +'.db'

    content = 'DB_DICT = { "' + connection + '": "' + string + '"}'

    to_write.write(content)
    to_write.close()


def create_user_credentials(**kwargs):
    required_keys = set(['aws_username', 'aws_access_key', 'aws_secret_key'])

    missed_keys = required_keys.difference(kwargs.keys())

    if len(missed_keys) != 0:
        raise KeyError(list(missed_keys))

    return kwargs


def extract_engine_or_fail(app_name: str):
    # create an RDS using users credentials
    db_engine = ''
    for bind_key, db_url in DB_DICT.items():
        if app_name == extract_database_name(bind_key):
            db_engine = db_url.split(':')[0]
            break
        else:
            continue

    if db_engine == '':
        raise RDSCreationError('Given app ' + app_name + ' does not exist.')

    return db_engine


def create_aws_config(**kwargs):
    kwargs['region_name'] = kwargs.get('region_name', region_name)
    kwargs['signature_version'] = kwargs.get('signature_version', signature_version)  # noqa E401
    kwargs['retries'] = kwargs.get('retries', {})
    kwargs['retries']['max_attempts'] = kwargs.get('max_attempts', max_attempts)  # noqa E401
    kwargs['retries']['mode'] = kwargs.get('mode', mode)

    # passed as kwargs for now
    # TODO: check default values we need to modify
    # user_agent
    # user_agent_extra
    # connect_timeout
    # read_timeout
    # parameter_validation
    # max_pool_connections
    # s3
    # retries
    # client_cert

    try:
        aws_config = Config(**kwargs)
        return aws_config
    except BotoCoreError as e:
        return {
            'result': 'An error occured while trying to create the config',
            'error': str(e)
        }


def create_and_store_keypair(ec2_instance, key_name=KEY_NAME) -> str:

    doga_key = ec2_instance.create_key_pair(KeyName=key_name)
    if os.path.exists(key_name+'.pem'):
        os.remove(key_name+'.pem')

    file = open(key_name + '.pem', 'a+')
    file.write(doga_key.key_material)
    file.close()
    os.popen('chmod 400 doga_key.pem')
    return doga_key.name


def create_security_group(ec2, group_name='sg_doga'):
    SG_IP_PROTOCOL = 'tcp'
    SG_FROM_PORT = 22
    SG_TO_PORT = 22
    SG_IP = get_current_ip() + '/32'
    SG_GROUP_NAME = 'sg_doga'

    # Create a security group and allow SSH inbound rule through the VPC
    securitygroup = ec2.create_security_group(
        GroupName=SG_GROUP_NAME,
        Description='created by doga to allow ssh from doga and http/https'
                    'from everywhere else'
    )

    securitygroup.authorize_ingress(
        IpPermissions=[
            {'IpProtocol': SG_IP_PROTOCOL,
             'FromPort': SG_FROM_PORT,
             'ToPort': SG_TO_PORT,
             'IpRanges': [{'CidrIp': SG_IP}]},
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 443,
             'ToPort': 443,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ]
    )

    return ec2


def create_RDS(user_credentials, aws_config, app_name, **kwargs):
    """
    Function used to create a RDS instance

    ::params::
    user_credentials: dict
    aws_config      : dict

    returns: RDSCreationError or RDS details in a dict
    """
    required_keys = set(['MasterUsername', 'MasterUserPassword',
                         'DBInstanceIdentifier', 'MaxAllocatedStorage',
                         'AllocatedStorage',
                         ])

    missed_keys = required_keys.difference(kwargs.keys())

    if len(missed_keys) != 0:
        raise KeyError(list(missed_keys))

    # these are defined in DOGA while creation of app
    DBName = kwargs.get('DBName', app_name)
    Engine = kwargs.get('Engine', extract_engine_or_fail(app_name))
    MasterUsername = kwargs['MasterUsername']
    MasterUserPassword = kwargs['MasterUserPassword']
    # DBSecurityGroups = kwargs['DBSecurityGroups']

    # from user while exporing
    # REQUIRED
    DBInstanceIdentifier = kwargs['DBInstanceIdentifier']
    AllocatedStorage = kwargs['AllocatedStorage']
    MaxAllocatedStorage = kwargs['MaxAllocatedStorage']

    # Optional
    DBInstanceClass = kwargs.get('DBInstanceClass', 'db.t2.micro')
    DeletionProtection = kwargs.get('DeletionProtection', False),
    EnableIAMDatabaseAuthentication = kwargs.get('EnableIAMDatabaseAuthentication', True)  # noqa 401
    EnablePerformanceInsights = kwargs.get('EnablePerformanceInsights', False)  # noqa 401
    MultiAZ = kwargs.get('MultiAZ', False)
    PubliclyAccessible = kwargs.get('PubliclyAccessible', True)
    PerformanceInsightsKMSKeyId = kwargs.get(
        'PerformanceInsightsKMSKeyId', '')
    # TODO: what should be the default
    # EnableCloudwatchLogsExports = kwargs.get()

    try:
        rds_client = boto3.client('rds',
                                  aws_access_key_id=user_credentials['aws_access_key'],  # noqa 401
                                  aws_secret_access_key=user_credentials['aws_secret_key'],  # noqa 401
                                  region_name=aws_config.region_name,
                                  config=aws_config
                                  )

        response = rds_client.create_db_instance(
            AllocatedStorage=AllocatedStorage,
            DBInstanceIdentifier=DBInstanceIdentifier,
            DBInstanceClass=DBInstanceClass,
            Engine=Engine,
            DBName=DBName,
            MasterUsername=MasterUsername,
            MasterUserPassword=MasterUserPassword,
            MaxAllocatedStorage=MaxAllocatedStorage,
        )
    #                                **kwargs,
    # )
        return response

    except ParamValidationError as e:
        raise RDSCreationError("Error creating RDS with given kwags",
                               str(e))

    except ClientError as e:
        raise RDSCreationError("Error creating RDS with given kwags",
                               str(e))


def create_EC2(user_credentials, aws_config, **kwargs):

    required_keys = set(['BlockDeviceMappings', 'ImageId', 'InstanceType',
                         'SecurityGroups'])

    missed_keys = required_keys.difference(kwargs.keys())

    if len(missed_keys) != 0:
        raise KeyError(list(missed_keys))

    ec2 = boto3.resource(
                    'ec2',
                    aws_access_key_id=user_credentials['aws_access_key'],
                    aws_secret_access_key=user_credentials['aws_secret_key'],
                    config=aws_config
                        )

    try:
        key_name = create_and_store_keypair(ec2_instance=ec2)
    except ClientError as error:
        raise EC2CreationError('Unable to create EC2 instance: ' + str(error))

    BlockDeviceMappings = kwargs['BlockDeviceMappings']
    ImageId = kwargs['ImageId']
    InstanceType = kwargs['InstanceType']
    SecurityGroups = kwargs['SecurityGroups']

    # Optional
    kwargs['MaxCount'] = kwargs.get('MaxCount', 1)
    kwargs['MinCount'] = kwargs.get('MinCount', 1)

    # KeyName = kwargs.get('KeyName', ''),  we will create the key
    # ourselves
    Monitoring = {'Enabled': False}
    kwargs['Monitoring'] = kwargs.get('Monitoring', Monitoring)
    kwargs['KeyName'] = KEY_NAME  # this is the key we will create

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
        KeyName=key_name
    )

    ec2 = create_security_group(ec2=ec2)

    ID = ec2_instance[0].id
    instance = ec2.Instance(ID)
    return key_name, instance


def deploy_to_aws(user_credentials, aws_config, ec2, key_name=KEY_NAME):

    while ec2.state['Name'] != 'running':
        ec2.load()

    try:
        ec2_client = boto3.client('ec2',
                                  aws_access_key_id=user_credentials['aws_access_key'],  # noqa 401
                                  aws_secret_access_key=user_credentials['aws_secret_key'],  # noqa 401
                                  region_name=aws_config.region_name,
                                  config=aws_config
                                )

        ssm_client = boto3.client('ssm',
                                  aws_access_key_id=user_credentials['aws_access_key'],  # noqa 401
                                  aws_secret_access_key=user_credentials['aws_secret_key'],  # noqa 401
                                  region_name=aws_config.region_name,
                                  config=aws_config
                                )

    except ClientError as e:
        raise EC2CreationError("Error creating EC2 with given kwags ",
                               str(e))

    ec2_client.associate_iam_instance_profile(
        IamInstanceProfile={
            'Name': 'AmazonSSMRoleForInstancesQuickSetup'
        },
        InstanceId=ec2.id
    )

    app_folder = os.sep.join(__file__.split(os.sep)[:-2]) + 'exported/app/*'

    # copy content of files
    os.popen('rsync -rv -e "ssh -i "' + key_name + '.pem " ' + app_folder
             + ' ubuntu@' + ec2.public_dns_name + ':exported_app')

    # run
    load_docker_commands = open('admin/export/install_docker.sh', 'r').read()
    commands = [load_docker_commands]

    ec2_client.reboot_instances(
        InstanceIds=[
            ec2.id
            ]
    )

    while ec2.state != 'running':
        ec2.load()

    ssm_client.send_command(DocumentName="AWS-RunShellScript",
                            Parameters={'commands': commands},
                            InstanceIds=[ec2.id])

    # move into directory and compose dockerfile& run service
    docker_app_commands = open('admin/export/create_and_startapp.sh', 'r').read()  # noqa E401
    commands = [docker_app_commands]

    ssm_client.send_command(DocumentName="AWS-RunShellScript",
                            Parameters={'commands': commands},
                            InstanceIds=[ec2.id])


def connect_rds_to_ec2(rds, ec2, user_credentials, config) -> bool:

    # update security group
    try:
        rds_client = boto3.client('rds',
                                  aws_access_key_id=user_credentials['aws_access_key'],  # noqa 401
                                  aws_secret_access_key=user_credentials['aws_secret_key'],  # noqa 401
                                  region_name=aws_config.region_name,
                                  config=aws_config
                                )

        rds_client.modify_db_instance(
            DBInstanceIdentifier=rds['DBInstance']['DBInstanceIdentifier'],
            VpcSecurityGroupIds=[
                ec2.vpc_id,
            ],
            DBParameterGroupName=['DBParameterGroups'],
            ApplyImmediately=True,
        )

        rds_client.reboot_instances(
            DBInstanceIdentifier=rds['DBInstance']['DBInstanceIdentifier']
            )

    except ClientError as e:
        raise DogaEC2toRDSconnectionError(str(e))

    # modify dbs.py

    rds.client
