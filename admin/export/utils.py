import os
from collections import defaultdict
from requests import get
import random
import shutil
import string
import subprocess
from time import sleep

import boto3
from botocore.config import Config
from botocore.exceptions import (BotoCoreError, ClientError,
                                 ParamValidationError)

import paramiko

from admin.aws_config import *
from admin.export.errors import *
from admin.models import Restricted_by_JWT
from admin.utils import extract_database_name

from admin.export.aws_defaults import *

from dbs import DB_DICT

from config import PORT

KEY_NAME = 'doga_key'
SG_GROUP_NAME = 'sg_doga'


def create_random_string(length: int) -> str:
    random_string = ''.join(
        random.choice(
            string.ascii_uppercase + string.digits) for _ in range(length))
    return random_string


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


def create_dockerfile(port, parent_dir, target_dir):
    # open dockerfile template
    dockerfile = open('templates/export/Dockerfile', 'r')
    dockerfile_contents = dockerfile.read()
    dockerfile_contents = dockerfile_contents.replace('PORT', str(port))

    # create Dockerfile
    exported_dockerfile = open(target_dir, 'a+')
    exported_dockerfile.write(dockerfile_contents)

    exported_dockerfile.close()
    dockerfile.close()


def export_blueprints(app_name, parent_dir, target_dir):
    contents = open(parent_dir, 'r').readlines()
    to_write = open(target_dir, 'a+')

    for i in range(0, len(contents)):
        if i in [2, 3, 4]:
            pass
        elif i in [0, 1]:
            to_write.write(contents[i])
        else:
            if app_name in contents[i]:
                to_write.write(contents[i])

    to_write.close()
    return


def create_heroku_postgres(app_name, destination):

    to_write = open(destination, 'a+')
    import_statement = "import os\n"
    conn_dict = '{ "' + app_name + '":' + 'os.environ["DATABASE_URL"]}\n'
    to_write.write(import_statement + conn_dict)
    return


def create_dbs_file(
        app_name,
        destination,
        rds_instance,
        user_credentials,
        aws_config):

    to_write = open(destination, 'a+')

    engine = rds_instance['Engine']
    username = rds_instance['MasterUsername']
    password = rds_instance['MasterUserPassword']
    server = rds_instance['Endpoint']['Address']
    port = str(rds_instance['Endpoint']['Port'])

    url = engine + '://' + username + ':' + password + \
        '@' + server + ':' + port + '/' + app_name
    # + '.db'  aws doesn't need this

    content = 'DB_DICT = { "' + app_name + '": "' + url + '"}'

    to_write.write(content)
    to_write.close()


def create_jwt_dict(app_name, destination):

    bind_key = ""
    for bind_key, db_string in DB_DICT.items():
        if app_name == extract_database_name(bind_key):
            break

    query = Restricted_by_JWT.query.filter_by(connection_name=bind_key)

    if query is None:
        return False

    jwt_dict = Restricted_by_JWT.query.filter_by(
        connection_name=bind_key).first()
    if jwt_dict is not None:
        jwt_dict = jwt_dict[0].asdict()
    file = open(destination, 'a+')
    file.write(str(jwt_dict))

    return True


def create_user_credentials(**kwargs):
    required_keys = {'aws_username', 'aws_access_key', 'aws_secret_key'}

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
        raise DogaAppNotFound('Given app ' + app_name + ' does not exist.')

    return db_engine


def create_aws_config(**kwargs):
    kwargs['region_name'] = kwargs.get('region_name', region_name)
    kwargs['signature_version'] = kwargs.get('signature_version', signature_version)  # noqa E401
    kwargs['retries'] = kwargs.get('retries', {})
    kwargs['retries']['max_attempts'] = kwargs.get('max_attempts', max_attempts)  # noqa E401
    kwargs['retries']['mode'] = kwargs.get('mode', mode)

    # PASSED AS KWARGS for now :
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
            'result': 'An error occurred while trying to create the config',
            'error': str(e)
        }


def validate_ec2_instance_id(user_credentials, aws_config, image_id):
    """
    try:
        ec2_client = boto3.client('ec2',
                              aws_access_key_id=user_credentials['aws_access_key'],  # noqa 401
                              aws_secret_access_key=user_credentials['aws_secret_key'],  # noqa 401
                              region_name=region_name,
                              config=aws_config
                             )
    except ClientError as e:
        raise EC2CreationError("Error connecting to EC2 with given kwags ",
                               str(e))

    images = ec2_client.describe_images()
    image_dict = images['Images']
    image_frame = pd.DataFrame.from_dict(image_dict).dropna(axis=1)

    if ImageId not in image_frame['ImageId']:
        raise EC2CreationError("Image ID provided is not valid.")

    image_info = image_frame.loc[
            image_frame['ImageId'] == image_id
            ].to_dict()

    info = str(image_info)

    platform = 'other'
    platforms = ['amazon linux', 'centos', 'debian', 'fedora', 'ubuntu']

    for i in platforms:
        if i in info:
            return i

    print(platform)
    return platform
    """
    # Connect to EC2
    # ec2 = boto3.resource('ec2')

    # Get information for all running instances
    # running_instances = ec2.instances.filter(Filters=[{
    #    'Name': 'instance-state-name',
    #    'Values': ['running']}])

    return "ubuntu"


def create_and_store_keypair(ec2_instance, key_name=KEY_NAME) -> str:

    doga_key = ec2_instance.create_key_pair(KeyName=key_name)
    if os.path.exists(key_name + '.pem'):
        os.remove(key_name + '.pem')

    file = open(key_name + '.pem', 'a+')
    file.write(doga_key.key_material)
    file.close()
    os.popen('chmod 400 ' + doga_key.name + '.pem')
    return doga_key.name


def create_security_group(ec2_client, ec2, db_port, group_id='sg_id',
                          **kwargs):

    waiter = ec2_client.get_waiter('instance_running')
    waiter.wait(InstanceIds=[ec2.instance_id])
    ec2.reload()

    if 'Not Connected ' in sg_defaults['SG_IP']:
        raise EC2CreationError('DOGA cannot connect to the internet.')

    ec2_client.authorize_security_group_ingress(
        GroupId=group_id,
        IpPermissions=[
            {'IpProtocol': sg_defaults["SG_IP_PROTOCOL"],
             'FromPort': sg_defaults["SG_FROM_PORT"],
             'ToPort': sg_defaults["SG_TO_PORT"],
             'IpRanges': [{'CidrIp': sg_defaults["SG_IP"]}]},
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 443,
             'ToPort': 443,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 8080,
             'ToPort': 8080,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': db_port,
             'ToPort': db_port,
             'IpRanges': [{'CidrIp': ec2.public_ip_address + '/32'}]}
        ],
        DryRun=False
    )

    ec2_resource = boto3.resource('ec2', **kwargs)
    vpc = ec2_resource.Vpc(ec2.vpc_id)
    vpc.create_tags(Tags=[{"Key": "Name", "Value": "doga_" + group_id[-5:]}])
    vpc.wait_until_available()

    vpc_sg = vpc.create_security_group(
        Description='created by doga to allow RDS and EC2 connect'
                    'from everywhere else',
        GroupName="doga_" + group_id[-5:],
    )

    ec2_client.authorize_security_group_ingress(
        GroupId=vpc_sg.id,
        IpPermissions=[
            {'IpProtocol': sg_defaults["SG_IP_PROTOCOL"],
             'FromPort': sg_defaults["SG_FROM_PORT"],
             'ToPort': sg_defaults["SG_TO_PORT"],
             'IpRanges': [{'CidrIp': sg_defaults["SG_IP"]}]},
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': db_port,
             'ToPort': db_port,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
             # ec2.public_ip_address + '/32'}]
             }
        ]
    )

    return ec2, vpc_sg


def create_rds(user_credentials, aws_config, app_name, **kwargs):
    """
    Function used to create a RDS instance

    ::params::
    user_credentials: dict
    aws_config      : dict

    returns: RDSCreationError or RDS details in a dict
    """
    required_keys = {'MasterUsername', 'MasterUserPassword',
                     'DBInstanceIdentifier', 'MaxAllocatedStorage',
                     'AllocatedStorage'}

    missed_keys = required_keys.difference(kwargs.keys())

    if len(missed_keys) != 0:
        raise KeyError(list(missed_keys))

    # these are defined in DOGA while creation of app
    dbname = kwargs.get('DBName', app_name)
    engine = kwargs.get('Engine', extract_engine_or_fail(app_name))
    master_username = kwargs['MasterUsername']
    master_password = kwargs['MasterUserPassword']

    # REQUIRED
    db_instance_identifier = kwargs['DBInstanceIdentifier']
    allocated_storage = kwargs['AllocatedStorage']
    max_allocated_storage = kwargs['MaxAllocatedStorage']

    # Optional
    db_instance_class = kwargs.get('DBInstanceClass', 'db.t2.micro')
    delete_protection = kwargs.get('DeletionProtection', False)
    enable_iam_database_authentication = kwargs.get('EnableIAMDatabaseAuthentication', True)  # noqa 401
    EnablePerformanceInsights = kwargs.get('EnablePerformanceInsights', False)  # noqa 401
    multi_az = kwargs.get('MultiAZ', False)
    publicly_accessible = kwargs.get('PubliclyAccessible', True)

    # NOT PASSED FOR NOW: what should be the default
    # EnableCloudwatchLogsExports = kwargs.get()
    # PerformanceInsightsKMSKeyId

    try:
        rds_client = boto3.client('rds',
                                  aws_access_key_id=user_credentials['aws_access_key'],  # noqa 401
                                  aws_secret_access_key=user_credentials['aws_secret_key'],  # noqa 401
                                  region_name=aws_config.region_name,
                                  config=aws_config
                                  )

        rds = rds_client.create_db_instance(
            AllocatedStorage=allocated_storage,
            DBInstanceIdentifier=db_instance_identifier,
            DBInstanceClass=db_instance_class,
            DeletionProtection=delete_protection,
            Engine=engine,
            DBName=dbname,
            MasterUsername=master_username,
            MasterUserPassword=master_password,
            MaxAllocatedStorage=max_allocated_storage,
            EnableIAMDatabaseAuthentication=enable_iam_database_authentication,
            MultiAZ=multi_az,
            PubliclyAccessible=publicly_accessible,
        )

        waiter = rds_client.get_waiter('db_instance_available')
        waiter.wait(
            DBInstanceIdentifier=rds["DBInstance"]["DBInstanceIdentifier"])

        rds_instance = rds_client.describe_db_instances(
            DBInstanceIdentifier=rds["DBInstance"]["DBInstanceIdentifier"]
        )['DBInstances'][0]

        return rds_instance

    except ParamValidationError as e:
        raise RDSCreationError("Error creating RDS with given arguments",
                               str(e))

    except ClientError as e:
        raise RDSCreationError("Error creating RDS with given arguments",
                               str(e))


def create_ec2(user_credentials, aws_config, rds_port, **kwargs):

    required_keys = {'BlockDeviceMappings', 'ImageId', 'InstanceType'}

    missed_keys = required_keys.difference(kwargs.keys())

    if len(missed_keys) != 0:
        raise KeyError(list(missed_keys))

    ec2 = boto3.resource(
        'ec2',
        aws_access_key_id=user_credentials['aws_access_key'],
        aws_secret_access_key=user_credentials['aws_secret_key'],
        config=aws_config
    )

    ec2_client = boto3.client('ec2',
                                aws_access_key_id=user_credentials['aws_access_key'],  # noqa 401
                                aws_secret_access_key=user_credentials['aws_secret_key'],  # noqa 401
                                region_name=aws_config.region_name,
                                config=aws_config
                            )

    random_string = create_random_string(5)
    sg_name = SG_GROUP_NAME + random_string
    security_group = ec2.create_security_group(
        GroupName=sg_name,
        Description='created by doga to allow ssh from doga and http/https'
                    'from everywhere else',
    )

    group_id = security_group.id
    try:
        key_name = create_and_store_keypair(ec2_instance=ec2,
                                            key_name=KEY_NAME +
                                            random_string
                                            )
    except ClientError as error:
        raise EC2CreationError('Unable to create EC2 instance: ' + str(error))

    block_device_mappings = kwargs['BlockDeviceMappings']
    image_id = kwargs['ImageId']
    instance_type = kwargs['InstanceType']

    # Optional
    kwargs['MaxCount'] = kwargs.get('MaxCount', 1)
    kwargs['MinCount'] = kwargs.get('MinCount', 1)
    kwargs['Monitoring'] = kwargs.get('Monitoring', {'Enabled': False})
    kwargs['KeyName'] = key_name  # this is the key we will create

    ec2_instance = ec2.create_instances(
        BlockDeviceMappings=block_device_mappings,
        ImageId=image_id,
        InstanceType=instance_type,
        MaxCount=kwargs['MaxCount'],
        MinCount=kwargs['MinCount'],
        Monitoring=kwargs['Monitoring'],
        KeyName=key_name,
        SecurityGroupIds=[group_id, ],
    )

    ec2, vpc_sg = create_security_group(
        ec2_client=ec2_client,
        ec2=ec2_instance[0],
        db_port=rds_port,
        group_id=security_group.id,
        **{
            "aws_access_key_id": user_credentials['aws_access_key'],
            "aws_secret_access_key": user_credentials['aws_secret_key'],
            "region_name": aws_config.region_name,
            "config": aws_config
        }
    )

    platform = validate_ec2_instance_id(user_credentials,
                                        aws_config,
                                        kwargs['ImageId'])

    return key_name, sg_name, ec2, vpc_sg, platform


def deploy_to_aws(user_credentials, aws_config, ec2, key_name=KEY_NAME,
                  platform='ubuntu'):
    print('505')
    while ec2.state['Name'] != 'running':
        ec2.load()
    print('508')
    try:
        ec2_client = boto3.client('ec2',
                                  aws_access_key_id=user_credentials['aws_access_key'],  # noqa 401
                                    aws_secret_access_key=user_credentials['aws_secret_key'],  # noqa 401
                                  region_name=aws_config.region_name,
                                  config=aws_config
                                )

    except ClientError as e:
        raise EC2CreationError("Error connecting to EC2 with given key word"
                               " arguments.", str(e))

    ec2_client.reboot_instances(
        InstanceIds=[
            ec2.instance_id,
        ]
    )
    print('533')
    waiter = ec2_client.get_waiter('instance_running')
    waiter.wait(InstanceIds=[ec2.instance_id])

    # associated_instances = []

    # while ec2.instance_id not in associated_instances:
    #     for i in ssm_client.describe_instance_information()[
    #             'InstanceInformationList']:
    #         associated_instances.append(i["InstanceId"])

    this_folder = os.sep.join(__file__.split(os.sep)[:-3])
    app_folder = os.sep.join(__file__.split(os.sep)[:-3]) + '/exported_app/*'

    # from:
    # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/managing-users.html
    print('549')

    platforms = {
        'amazon linux': 'ec2-user',
        'centos': 'centos',
        'debian': 'admin',
        'fedora': 'fedora',
        'ubuntu': 'ubuntu',
        'other': 'root'
    }

    user = platforms[platform]

    key = paramiko.RSAKey.from_private_key_file(this_folder + '/' +
                                                key_name + '.pem')
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect/ssh to an instance
    client.connect(
        hostname=ec2.public_dns_name,
        username=user,
        pkey=key,
        allow_agent=False,
        look_for_keys=False)

    client.exec_command('mkdir -p $HOME/exported_app')

    os.system('scp -o UserKnownHostsFile=/dev/null -o '
              'StrictHostKeyChecking=no -r -i ' + this_folder +
              '/' + key_name + '.pem '
              + app_folder + ' ' + user + '@' + ec2.public_dns_name +
              ':exported_app/')

    print("here")
    proc = subprocess.Popen(
        [
            'scp',
            ' -o',
            'UserKnownHostsFile=/dev/null',
            '-o ',
            'StrictHostKeyChecking=no',
            '-r',
            '-i',
            this_folder +
            '/' +
            key_name +
            '.pem' +
            app_folder +
            ' ' +
            user +
            '@' +
            ec2.public_dns_name +
            ':exported_app/'],
        stdout=subprocess.PIPE,
        shell=True)

    out, err = proc.communicate()
    print("program output:", out)

    client.exec_command('curl -sSL https://get.docker.com/ | sh')
    sleep(10)
    client.close()

    return ec2


def connect_rds_to_ec2(rds, ec2, user_credentials, config, sg_name,
                       vpc_sg, platform, key_name=KEY_NAME) -> bool:

    # update security group
    try:
        rds_client = boto3.client('rds',
                                  aws_access_key_id=user_credentials['aws_access_key'],  # noqa 401
                                  aws_secret_access_key=user_credentials['aws_secret_key'],  # noqa 401
                                  region_name=config.region_name,
                                  config=config
                                )

        response = rds_client.modify_db_instance(
            DBInstanceIdentifier=rds['DBInstanceIdentifier'],
            VpcSecurityGroupIds=[
                vpc_sg.id
            ],
            ApplyImmediately=True,
        )
        print('618')
        rds_client.reboot_db_instance(
            DBInstanceIdentifier=rds['DBInstanceIdentifier']
        )

        waiter = rds_client.get_waiter('db_instance_available')
        waiter.wait(
            DBInstanceIdentifier=rds['DBInstanceIdentifier'])

    except ClientError as e:
        raise DogaEC2toRDSconnectionError(str(e))

    platforms = {
        'amazon linux': 'ec2-user',
        'centos': 'centos',
        'debian': 'admin',
        'fedora': 'fedora',
        'ubuntu': 'ubuntu',
        'other': 'root'
    }

    user = platforms[platform]

    print('649')

    key = paramiko.RSAKey.from_private_key_file(key_name + '.pem')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    load_app_commands = open('admin/export/create_and_startapp.sh', 'r'
                             ).read()

    for line in load_app_commands:
        line = line.replace("PORT", str(PORT))

    commands = [load_app_commands]

    print('660')

    try:
        client.connect(
            hostname=ec2.public_dns_name,
            username=user,
            pkey=key
        )

        stdin, stdout, stderr = client.exec_command(commands)
    except Exception as error:
        return False

    return True
