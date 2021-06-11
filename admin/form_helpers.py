from flask import Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import verify_jwt

from boto3.session import Session

from admin.models import Admin
from admin.default_values import DEFAULT_PORTS


utils = Blueprint("utils", __name__)
api_utils = Api()
api_utils.init_app(utils)


class DBDefaults(Resource):
    """
    Return default host and port for all doga databases
    """

    def get(self):
        default_host = {}
        for key, value in DEFAULT_PORTS.items():
            default_host[key] = "localhost"

        return {"host": default_host, "port": DEFAULT_PORTS}


class AWSFormHelper(Resource):
    """
    Endpoint to provide default values and info regarding the aws exports
    """

    @jwt_required
    def post(self, section=None):

        if not verify_jwt(get_jwt_identity(), Admin):
            return {"result": "JWT authorization invalid, user does not exist."
                    }

        """
        Credentials required by AWS to establish the request it is receiving is
        from a particular aws user.
        you should be able to see them in your aws IAM roles for the new role
        It is recommended you create a new role to deploy your app and make
        sure you have all the necessary permissions to create and modify both
        RDS and EC2 instances as well as send commands over SSM.
        provide the aws:
        "aws_username": "username",
        "aws_secret_key": "XxxX/xxxx",
        "aws_access_key": "XXXXXX"
        """
        # no defaults

        # config
        #   aws region_name
        #       This indicates the region where the EC2 instance as well as RDS
        #       will be created in, please ensure you choose a region that has
        #       SSM, RDS and EC2 services.
        #       Detailed information of the services can be found
        #       (on amazons webpage)[https://aws.amazon.com/about-aws/
        #       global-infrastructure/regional-product-services/]
        s = Session()
        aws_region_names = s.get_available_regions("ssm")

        #   signature_version
        #       this outlines the method used by AWS for authenticating
        #       requests. Version 4 is the most stable and recommended
        #       protocol.
        #       For mode details refer to (how aws signs api requests.)
        #       [https://docs.aws.amazon.com/general/latest/gr/signing_
        #       aws_api_requests.html]
        signature_version = "v4"

        #   retries:
        retries = {"max_attempts": 10, "mode": "standard"}
        #       max_attempts
        #       In case the calls to AWS services fail due to unexpected issues
        #       This field allows users to specify the maximum attempts he
        #       would like to resend the request.

        #       mode
        #       This indicates the retry handler you would like to use

        """
        Relational Data Service (RDS) configuration
        AWS provides users a hassle free way to configure remote data storage
        for relational database stores through this service. The users may
        chose from an array of options.
        A few basic configurations are:
        """
        rds_config = {
            "Engine": ["MySQL", "postgres"],
            "DBInstanceIdentifier": "",
            "DBInstanceClass": "db.t2.micro",
            "AllocatedStorage": 20,
            "MaxAllocatedStorage": 1634,
            "MasterUsername": "admin",
            "MasterUserPassword": "password",
        }

        # Name of the DB to be given by the user the default should be app name

        # Database Engine Instance Class
        # depending on the region and the engine chosen, AWS will allow users
        # chose form an array different machines with different hardware
        # configurations.
        # Refer to (this)[https://docs.aws.amazon.com/AmazonRDS/latest/Us
        # erGuide/Concepts.DBInstanceClass.html]
        # doc for further details

        # Minimum storage allocated in GB s
        # minimum is 20
        # similarly max is 1634

        # The admin username and password for the master user of the RDS
        # instance

        """
        Elastic Compute Cloud 2 services provide the users a virtual machine
        of their choice. These servers have varying downtimes, response 
        times as well as computation power. AWS also provides certain free
        tier instances and configurations, those will be provided as
        defaults.
        """

        ec2_config = {
            "InstanceType": "t2.micro",
            "ImageId": "ami-0885b1f6bd170450c",
            "BlockDeviceMappings": [
                {
                    "DeviceName": "/dev/sda1",
                    "Ebs": {
                        "DeleteOnTermination": True,
                        "VolumeSize": 8,
                        "VolumeType": "gp2",
                    },
                }
            ],
        }

        # Base machine for the instance, this specifies hardware and size
        # the default is for a free tier micro instance

        # The image ID determines what OS and configuration should be loaded
        # onto the instance, the default AMI is for an Ubuntu 20.4 Image

        # This specifies values that need to be configured for the instances
        # storage, each block device needs to be added to the list separately.
        # the defaults provided:

        # *DeleteOnTermination* if true all backed up storage and snapshots of
        #   volume are lost and instance cannot be reverted to it's initial
        #   AMI state.

        # *VolumeSize* specifies the size of the attached block device in GBs

        # *VolumeType* can be one of gp3, gp2 for General purpose SSD and
        #   one of io2, io1 for a Provisioned IOPS SSD, more information can
        #   be found [at](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/
        #   ebs-volume-types.html)

        response = {
            "config": {
                "region_name": aws_region_names,
                "retries": retries,
                "signature_version": signature_version,
            },
            "rds_config": rds_config,
            "ec2_config": ec2_config,
        }

        try:
            return {section: response[section]}, 200
        except KeyError:
            return (
                {"error": "The section " + section + " does not exist."},
                400,
            )


api_utils.add_resource(AWSFormHelper, "/aws/form/<string:section>")
api_utils.add_resource(DBDefaults, "/defaults/db")
