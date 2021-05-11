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
from botocore.exceptions import (
    BotoCoreError,
    ClientError,
    ParamValidationError,
)

import paramiko
from paramiko.ssh_exception import NoValidConnectionsError

from admin.aws_config import *
from admin.export.errors import *
from admin.models import Restricted_by_JWT
from admin.utils import extract_database_name

from admin.export.aws_defaults import *

from dbs import DB_DICT

from config import PORT

KEY_NAME = "doga_key"
SG_GROUP_NAME = "sg_doga"


def create_random_string(length: int) -> str:
    """ Returns a unique string of given lenth
    """
    random_string = "".join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(length)
    )
    return random_string


def get_current_ip() -> str:
    """ Retrun a string containing the current IP address
    """
    ip = get("https://api.ipify.org").text
    return ip


def create_requirements(
    db_engine: str,
    target_dir: str,
    parent_dir: str = "templates/export/requirements",
):
    """ Generates the appropriate requirements.txt file for the /exported_app,
        uses the stored requirements in the templates folder.

        Parameters:
        ----------
         db_engine: string
                    name of the database engine that the app uses
         parent_dir: string
                     name of the directory where the requirements.txt templates
                     are stored.
         target_dor: string
                     name of the directory where the requirements.txt file
                     should be generated.
    """
    s = parent_dir + "/common_requirements.txt"
    d = target_dir + "/requirements.txt"
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(s, d)

    file = open(d, "a+")

    if db_engine == "postgres":
        specific = parent_dir + "/postgres_requirements.txt"
        file.write(open(specific, "r").read())
    if db_engine == "mysql":
        specific = parent_dir + "/mysql_requirements.txt"
        file.write(open(specific, "r").read())

    file.close()


def create_dockerfile(port, target_dir):
    """Uses the template Dockerfile to create the same at the target_directory

      Paratemers:
      ----------
      port: string,int
            This should be the port address that the application Dockerfile
            will expose
      target_dir: string
            The destination to create the file.
    """
    # open dockerfile template
    dockerfile = open("templates/export/Dockerfile", "r")
    dockerfile_contents = dockerfile.read()
    dockerfile_contents = dockerfile_contents.replace("PORT", str(port))

    # create Dockerfile
    exported_dockerfile = open(target_dir, "a+")
    exported_dockerfile.write(dockerfile_contents)

    exported_dockerfile.close()
    dockerfile.close()


def export_blueprints(
    app_name: str, parent_dir: str, target_dir: str,
):
    """
    Creates the blueprints file for the exported app

    Parameters:
    -----------
    app_name: string
              Name of the application being exported.
    parent_dir: string
                path to DOGA's main blueprints file.
    target_dir: string
                file path where the app's blueprints should be created.
    """
    contents = open(parent_dir, "r").readlines()
    to_write = open(target_dir, "a+")

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
    """Function to environment variables for 'provisioned' databases for
       apps exported to the Heroku Platform.
    """
    to_write = open(destination, "a+")
    import_statement = "import os\n"
    conn_dict = '{ "' + app_name + '":' + 'os.environ["DATABASE_URL"]}\n'
    to_write.write(import_statement + conn_dict)
    return


def create_dbs_file(app_name, destination, rds_instance):
    """Creates the dbs.py file for the exported app, this file keeps track
       of the URI of the Database.

       Parameters:
       ----------
       app_name: string
                 name of the application the is being exported.
       destination: string
                    path of the file to be created.
      rds_instance: rds instance object
                    The RDS instace object returned by boto3
    """
    to_write = open(destination, "a+")

    engine = rds_instance["Engine"]
    username = rds_instance["MasterUsername"]
    password = rds_instance["MasterUserPassword"]
    server = rds_instance["Endpoint"]["Address"]
    port = str(rds_instance["Endpoint"]["Port"])

    url = (
        engine
        + "://"
        + username
        + ":"
        + password
        + "@"
        + server
        + ":"
        + port
        + "/"
        + app_name
    )

    content = 'DB_DICT = { "' + app_name + '": "' + url + '"}'

    to_write.write(content)
    to_write.close()


def create_user_credentials(**kwargs):
    """
    Given the kwargs the function checks check if sufficient credentials
    are provided by the user to authenticate the aws account.

    returns a list or dict
    """
    required_keys = {"aws_username", "aws_access_key", "aws_secret_key"}

    missed_keys = required_keys.difference(kwargs.keys())

    if len(missed_keys) != 0:
        raise KeyError(list(missed_keys))

    return kwargs


def extract_engine_or_fail(app_name: str):
    """If app exists returns the db engine else raises DogaAppNotFound error.
    """
    db_engine = ""
    for bind_key, db_url in DB_DICT.items():
        if app_name == extract_database_name(bind_key):
            db_engine = db_url.split(":")[0]
            break
        else:
            continue

    if db_engine == "":
        raise DogaAppNotFound("Given app " + app_name + " does not exist.")

    return db_engine


def create_aws_config(**kwargs):
    """Creates configuration for the exported aws app.
       Required Arguments:
       ------------------
       - region_name:
         type: string
         example: us-east-1
         description: This indicates the region where the EC2 instance as well
                      as RDS will be created in, please ensure you choose a
                      region that has SSM, RDS and EC2 services.
       - signature_version:
         type: string
         example: 'v4'
         description: Outlines the method used by AWS for authenticating
                      request. ( version 4 is most stable and reccomended)
       - retries:
         type: integer
         example:4
         description: In the case that aws requests fail this specifies the
                      number of retires the user would like to perform.
    """

    # check for the required kwargs

    kwargs["region_name"] = kwargs.get("region_name", region_name)
    kwargs["signature_version"] = kwargs.get(
        "signature_version", signature_version
    )
    kwargs["retries"] = kwargs.get("retries", {})
    kwargs["retries"]["max_attempts"] = kwargs.get(
        "max_attempts", max_attempts
    )
    kwargs["retries"]["mode"] = kwargs.get("mode", mode)

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
            "result": "An error occurred while trying to create the config",
            "error": str(e),
        }


def validate_ec2_instance_id(user_credentials, aws_config, image_id) -> str:
    """ The function validates the ec2 instance's state and verifies
        what operating system it runs and and decided what user to ssh as
    """

    try:
        ec2_client = boto3.client(
            "ec2",
            aws_access_key_id=user_credentials["aws_access_key"],
            aws_secret_access_key=user_credentials["aws_secret_key"],
            region_name=region_name,
            config=aws_config,
        )
    except ClientError as e:
        raise EC2CreationError(
            "Error connecting to EC2 with given kwags ", str(e)
        )

    images = ec2_client.describe_instances(InstanceIds=[image_id])
    image_dict = images["Reservations"][0]["Instances"][0]
    # image_frame = pd.DataFrame.from_dict(image_dict).dropna(axis=1)

    # if image_id not in image_frame['image_id']:
    #    raise EC2CreationError("Image ID provided is not valid.")

    # image_info = image_frame.loc[
    #        image_frame['ImageId'] == image_id
    #        ].to_dict()
    # print(image_info)
    # info = str(image_info)

    platform = "other"
    platforms = ["amazon linux", "centos", "debian", "fedora", "ubuntu"]

    # for i in platforms:
    #    if i in info:
    #        return i

    return "ubuntu"
    # return platform

    # Connect to EC2
    # ec2 = boto3.resource('ec2')

    # Get information for all running instances
    # running_instances = ec2.instances.filter(Filters=[{
    #    'Name': 'instance-state-name',
    #    'Values': ['running']}])

    # return "ubuntu"


def create_and_store_keypair(ec2_instance, key_name=KEY_NAME) -> str:
    """To access a ec2 isntance, we must ensure that the ssh key file is
       accessable to DOGA. This function creates and stores a unique keypair
       within DOGA's directory.
       Parameters:
       ----------
       - ec2_isntance:
         type: boto3 ec2 instance
         required: true
         description: The ec2 instance that the new key should be attached to
       - key_name:
         type: string
         required: false
         description: the name of the custom key

       Returns:
       -------
        - key_name
          type: string
          description: the name of the key file created.
    """

    doga_key = ec2_instance.create_key_pair(KeyName=key_name)
    if os.path.exists(key_name + ".pem"):
        os.remove(key_name + ".pem")

    file = open(key_name + ".pem", "a+")
    file.write(doga_key.key_material)
    file.close()
    os.popen("chmod 400 " + doga_key.name + ".pem")
    return doga_key.name


def create_security_group(
    ec2_client, ec2, db_port, group_id="sg_id", **kwargs
):

    waiter = ec2_client.get_waiter("instance_running")
    waiter.wait(InstanceIds=[ec2.instance_id])
    ec2.reload()

    if "Not Connected " in sg_defaults["SG_IP"]:
        raise EC2CreationError("DOGA cannot connect to the internet.")

    ec2_client.authorize_security_group_ingress(
        GroupId=group_id,
        IpPermissions=[
            {
                "IpProtocol": sg_defaults["SG_IP_PROTOCOL"],
                "FromPort": sg_defaults["SG_FROM_PORT"],
                "ToPort": sg_defaults["SG_TO_PORT"],
                "IpRanges": [{"CidrIp": sg_defaults["SG_IP"]}],
            },
            {
                "IpProtocol": "tcp",
                "FromPort": 80,
                "ToPort": 80,
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
            },
            {
                "IpProtocol": "tcp",
                "FromPort": 443,
                "ToPort": 443,
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
            },
            {
                "IpProtocol": "tcp",
                "FromPort": 8080,
                "ToPort": 8080,
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
            },
            {
                "IpProtocol": "tcp",
                "FromPort": db_port,
                "ToPort": db_port,
                "IpRanges": [{"CidrIp": ec2.public_ip_address + "/32"}],
            },
        ],
        DryRun=False,
    )

    ec2_resource = boto3.resource("ec2", **kwargs)
    vpc = ec2_resource.Vpc(ec2.vpc_id)
    vpc.create_tags(Tags=[{"Key": "Name", "Value": "doga_" + group_id[-5:]}])
    vpc.wait_until_available()

    vpc_sg = vpc.create_security_group(
        Description="created by doga to allow RDS and EC2 connect"
        "from everywhere else",
        GroupName="doga_" + group_id[-5:],
    )

    ec2_client.authorize_security_group_ingress(
        GroupId=vpc_sg.id,
        IpPermissions=[
            {
                "IpProtocol": sg_defaults["SG_IP_PROTOCOL"],
                "FromPort": sg_defaults["SG_FROM_PORT"],
                "ToPort": sg_defaults["SG_TO_PORT"],
                "IpRanges": [{"CidrIp": sg_defaults["SG_IP"]}],
            },
            {
                "IpProtocol": "tcp",
                "FromPort": 80,
                "ToPort": 80,
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
            },
            {
                "IpProtocol": "tcp",
                "FromPort": db_port,
                "ToPort": db_port,
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
                # ec2.public_ip_address + '/32'}]
            },
        ],
    )

    return ec2, vpc_sg


def create_rds(user_credentials, aws_config, app_name, **kwargs):
    """Function used to create a AWS RDS instance

    Parameters:
    -----------
    user_credentials: dict
    aws_config      : dict

    returns: RDSCreationError or RDS details in a dict
    """
    required_keys = {
        "MasterUsername",
        "MasterUserPassword",
        "DBInstanceIdentifier",
        "MaxAllocatedStorage",
        "AllocatedStorage",
    }

    missed_keys = required_keys.difference(kwargs.keys())

    if len(missed_keys) != 0:
        raise KeyError(list(missed_keys))

    # these are defined in DOGA while creation of app
    dbname = kwargs.get("DBName", app_name)
    engine = kwargs.get("Engine", extract_engine_or_fail(app_name))
    master_username = kwargs["MasterUsername"]
    master_password = kwargs["MasterUserPassword"]

    # REQUIRED
    db_instance_identifier = kwargs["DBInstanceIdentifier"]
    allocated_storage = kwargs["AllocatedStorage"]
    max_allocated_storage = kwargs["MaxAllocatedStorage"]

    # Optional
    db_instance_class = kwargs.get("DBInstanceClass", "db.t2.micro")
    delete_protection = kwargs.get("DeletionProtection", False)
    enable_iam_database_authentication = kwargs.get(
        "EnableIAMDatabaseAuthentication", True
    )
    EnablePerformanceInsights = kwargs.get("EnablePerformanceInsights", False)
    multi_az = kwargs.get("MultiAZ", False)
    publicly_accessible = kwargs.get("PubliclyAccessible", True)

    # NOT PASSED FOR NOW: what should be the default
    # EnableCloudwatchLogsExports = kwargs.get()
    # PerformanceInsightsKMSKeyId
    try:
        rds_client = boto3.client(
            "rds",
            aws_access_key_id=user_credentials["aws_access_key"],
            aws_secret_access_key=user_credentials["aws_secret_key"],
            region_name=aws_config.region_name,
            config=aws_config,
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

        waiter = rds_client.get_waiter("db_instance_available")
        waiter.wait(
            DBInstanceIdentifier=rds["DBInstance"]["DBInstanceIdentifier"]
        )

        rds_instance = rds_client.describe_db_instances(
            DBInstanceIdentifier=rds["DBInstance"]["DBInstanceIdentifier"]
        )["DBInstances"][0]

        return rds_instance

    except ParamValidationError as e:
        raise RDSCreationError(
            "Error creating RDS with given arguments", str(e)
        )

    except ClientError as e:
        raise RDSCreationError(
            "Error creating RDS with given arguments", str(e)
        )


def create_ec2(user_credentials, aws_config, rds_port, **kwargs):

    required_keys = {"BlockDeviceMappings", "ImageId", "InstanceType"}

    missed_keys = required_keys.difference(kwargs.keys())

    if len(missed_keys) != 0:
        raise KeyError(list(missed_keys))

    ec2 = boto3.resource(
        "ec2",
        aws_access_key_id=user_credentials["aws_access_key"],
        aws_secret_access_key=user_credentials["aws_secret_key"],
        config=aws_config,
    )

    ec2_client = boto3.client(
        "ec2",
        aws_access_key_id=user_credentials["aws_access_key"],
        aws_secret_access_key=user_credentials["aws_secret_key"],
        region_name=aws_config.region_name,
        config=aws_config,
    )

    random_string = create_random_string(5)
    sg_name = SG_GROUP_NAME + random_string
    security_group = ec2.create_security_group(
        GroupName=sg_name,
        Description="created by doga to allow ssh from doga and http/https"
        "from everywhere else",
    )

    group_id = security_group.id
    try:
        key_name = create_and_store_keypair(
            ec2_instance=ec2, key_name=KEY_NAME + random_string
        )
    except ClientError as error:
        raise EC2CreationError("Unable to create EC2 instance: " + str(error))

    block_device_mappings = kwargs["BlockDeviceMappings"]
    image_id = kwargs["ImageId"]
    instance_type = kwargs["InstanceType"]

    # Optional
    kwargs["MaxCount"] = kwargs.get("MaxCount", 1)
    kwargs["MinCount"] = kwargs.get("MinCount", 1)
    kwargs["Monitoring"] = kwargs.get("Monitoring", {"Enabled": False})
    kwargs["KeyName"] = key_name  # this is the key we will create

    ec2_instance = ec2.create_instances(
        BlockDeviceMappings=block_device_mappings,
        ImageId=image_id,
        InstanceType=instance_type,
        MaxCount=kwargs["MaxCount"],
        MinCount=kwargs["MinCount"],
        Monitoring=kwargs["Monitoring"],
        KeyName=key_name,
        SecurityGroupIds=[group_id, ],
    )

    ec2, vpc_sg = create_security_group(
        ec2_client=ec2_client,
        ec2=ec2_instance[0],
        db_port=rds_port,
        group_id=security_group.id,
        **{
            "aws_access_key_id": user_credentials["aws_access_key"],
            "aws_secret_access_key": user_credentials["aws_secret_key"],
            "region_name": aws_config.region_name,
            "config": aws_config,
        }
    )

    platform = validate_ec2_instance_id(
        user_credentials, aws_config, ec2.instance_id
    )

    return key_name, sg_name, ec2, vpc_sg, platform


def deploy_to_aws(
    user_credentials, aws_config, ec2, key_name=KEY_NAME, platform="ubuntu"
):
    while ec2.state["Name"] != "running":
        ec2.load()
    try:
        ec2_client = boto3.client(
            "ec2",
            aws_access_key_id=user_credentials["aws_access_key"],
            aws_secret_access_key=user_credentials["aws_secret_key"],
            region_name=aws_config.region_name,
            config=aws_config,
        )

    except ClientError as e:
        raise EC2CreationError(
            "Error connecting to EC2 with given key word" " arguments.", str(e)
        )

    ec2_client.reboot_instances(
        InstanceIds=[ec2.instance_id, ]
    )
    waiter = ec2_client.get_waiter("instance_running")
    waiter.wait(InstanceIds=[ec2.instance_id])

    sleep(22)
    this_folder = os.sep.join(__file__.split(os.sep)[:-3])
    app_folder = os.sep.join(__file__.split(os.sep)[:-3]) + "/exported_app/*"

    # from:
    # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/managing-users.html

    platforms = {
        "amazon linux": "ec2-user",
        "centos": "centos",
        "debian": "admin",
        "fedora": "fedora",
        "ubuntu": "ubuntu",
        "other": "root",
    }

    user = platforms[platform]

    key = paramiko.RSAKey.from_private_key_file(
        this_folder + "/" + key_name + ".pem"
    )
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect/ssh to an instance
    sleep(5)

    done = False
    while done is False:
        try:
            client.connect(
                hostname=ec2.public_dns_name, username=user, pkey=key,
            )
            done = True
        except NoValidConnectionsError as e:
            done = False
    stdin, stdout, stderr = client.exec_command("mkdir -p $HOME/exported_app")
    stdout.channel.recv_exit_status()

    os.system(
        "scp -o UserKnownHostsFile=/dev/null -o "
        "StrictHostKeyChecking=no -r -i "
        + this_folder
        + "/"
        + key_name
        + ".pem "
        + app_folder
        + " "
        + user
        + "@"
        + ec2.public_dns_name
        + ":exported_app/"
    )

    stdin_, stdout_, stderr_ = client.exec_command(
        "curl -sSL https://get.docker.com/ | sh"
    )
    stdout_.channel.recv_exit_status()
    client.close()

    return ec2


def connect_rds_to_ec2(
    rds,
    ec2,
    user_credentials,
    config,
    sg_name,
    vpc_sg,
    platform,
    key_name=KEY_NAME,
) -> bool:

    # update security group
    try:
        rds_client = boto3.client(
            "rds",
            aws_access_key_id=user_credentials["aws_access_key"],
            aws_secret_access_key=user_credentials["aws_secret_key"],
            region_name=config.region_name,
            config=config,
        )

        response = rds_client.modify_db_instance(
            DBInstanceIdentifier=rds["DBInstanceIdentifier"],
            VpcSecurityGroupIds=[vpc_sg.id],
            ApplyImmediately=True,
        )
        rds_client.reboot_db_instance(
            DBInstanceIdentifier=rds["DBInstanceIdentifier"]
        )

        waiter = rds_client.get_waiter("db_instance_available")
        waiter.wait(DBInstanceIdentifier=rds["DBInstanceIdentifier"])

    except ClientError as e:
        raise DogaEC2toRDSconnectionError(str(e))

    platforms = {
        "amazon linux": "ec2-user",
        "centos": "centos",
        "debian": "admin",
        "fedora": "fedora",
        "ubuntu": "ubuntu",
        "other": "root",
    }

    user = platforms[platform]

    key = paramiko.RSAKey.from_private_key_file(key_name + ".pem")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    sleep(10)
    try:
        client.connect(hostname=ec2.public_dns_name, username=user, pkey=key)

        stdin, stdout, stderr = client.exec_command(
            "cd exported_app && " + "sudo docker build --tag app:latest ."
        )
        stdout.channel.recv_exit_status()

        stdin, stdout, stderr = client.exec_command(
            "sudo docker swarm init "
            + "&& sudo docker service"
            + " create --name app -p "
            + "8080:8080 app:latest"
        )
        stdout.channel.recv_exit_status()
    except Exception:
        return False

    return True
