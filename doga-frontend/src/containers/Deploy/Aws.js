import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { useGlobal } from "reactn";
// import { setGlobal, useGlobal } from "reactn";
import { NavLink } from "react-router-dom";
import {
  Box,
  ResponsiveImage,
  Image,
  Button,
  StyledLink,
  Span,
  MotionBox,
  H2,
  H5,
  Input,
  Label,
  Para,
} from "../../styles";
import { BsPlusCircleFill } from "react-icons/bs";
import { FaAws } from "react-icons/fa";
import { AiOutlineDelete } from "react-icons/ai";
import { Icon } from "@chakra-ui/react";
import { SiAmazonaws, SiHeroku } from "react-icons/si";
import { useQuery, useQueryClient } from "react-query";
import { useToast, createStandaloneToast } from "@chakra-ui/react";
import Api, { setHeader, APIURLS, ApiJwt } from "../../Api";
import { useIsFetching } from "react-query";
import Select from "react-select";
import ClipLoader from "react-spinners/ClipLoader";

const Aws = ({
  userCredential,
  setStep,
  userConfig,
  setUserCredential,
  rdsConfig,
  ec2Config,
}) => {
  const [token] = useGlobal("token");
  const { handleSubmit, register, errors, reset } = useForm();
  const [toggle, setToggle] = useState(true);
  const [selectedApp, setSelectedApp] = useState();
  const [loading, setLoading] = useState(false);
  const [provisionDb, setProvisionDb] = useState();
  // const queryClient = useQueryClient();
  const isFetching = useIsFetching();
  const toast = createStandaloneToast();
  const queryClient = useQueryClient();

  const [deviceList, setDeviceList] = useState([]);
  const [instanceType, setInstanceType] = useState();
  const [imageId, setImageId] = useState();
  const [deviceName, setDeviceName] = useState(
    ec2Config.ec2_config.BlockDeviceMappings[0].DeviceName
  );
  const [engineType, setEngineType] = useState();
  const [volumeType, setVolumeType] = useState(
    ec2Config.ec2_config.BlockDeviceMappings[0].Ebs.VolumeType
  );
  const [volumeSize, setVolumeSize] = useState(
    ec2Config.ec2_config.BlockDeviceMappings[0].Ebs.VolumeSize
  );
  const [deleteOnTermination, setDeleteOnTermination] = useState(
    ec2Config.ec2_config.BlockDeviceMappings[0].Ebs.DeleteOnTermination
  );
  const addDeviceHandler = () => {
    setDeviceList([
      ...deviceList,
      {
        DeviceName: deviceName,
        Ebs: {
          DeleteOnTermination: deleteOnTermination,
          VolumeSize: volumeSize,
          VolumeType: volumeType,
        },
      },
    ]);
    setDeviceName("");
    setDeleteOnTermination("");
    setVolumeSize("");
    setVolumeType("");

    // setUserEmail("");
    // reset();
  };
  const removeDeviceHandler = (index) => {
    let newDeviceList = [];
    for (let key in deviceList) {
      console.log(deviceList[key], "key", key);
      if (key != index) {
        newDeviceList.push(deviceList[key]);
      }
    }
    //  userList.slice(0, index).concat(userList.slice(-index));
    console.log(newDeviceList);
    setDeviceList(newDeviceList);
    // console.log(userList.splice(index, 1))
  };
  console.log(ec2Config.ec2_config.BlockDeviceMappings[0].DeviceName, "here");
  async function handleSignup(params) {
    setLoading(true);
    try {
      let obj = {
        app_name: userCredential.app_name,
        user_credentials: {
          aws_username: userCredential.user_credentials.aws_username,
          aws_secret_key: userCredential.user_credentials.aws_secret_key,
          aws_access_key: userCredential.user_credentials.aws_access_key,
        },
        config: {
          region_name: userCredential.config.region_name,
          signature_version: userCredential.config.signature_version,
          //  "retries": {
          //      "max_attempts":"string",
          //      "mode": "string"
          //      }
        },
        rds_config: {
          Engine: userCredential.rds_config.Engine,
          AllocatedStorage: userCredential.rds_config.AllocatedStorage,
          DBInstanceIdentifier: userCredential.rds_config.DBInstanceIdentifier,
          DBInstanceClass: userCredential.rds_config.DBInstanceClass,
          MasterUsername: userCredential.rds_config.MasterUsername,
          MasterUserPassword: userCredential.rds_config.MasterUserPassword,
          MaxAllocatedStorage: userCredential.rds_config.MaxAllocatedStorage,
        },
        ec2_config: {
          BlockDeviceMappings: deviceList,
          InstanceType: params.InstanceType,
          ImageId: params.ImageId,
          // "ami-0885b1f6bd170450c"
        },
      };
      console.log(obj);
      setUserCredential();
      let { data } = await Api.post(APIURLS.awsExport(), obj);
      setStep(5);
      setLoading(false);
      //   let { data } = await Api.post(APIURLS.awsExport(), obj);
    } catch ({ response }) {
      setLoading(false);
    }
  }

  return loading ? (
    <Box type="loader">
      <ClipLoader color={"#ffffff"} size={55} />
    </Box>
  ) : (
    <>
      <Box type="heading" textAlign="center">
        <Span type="heading">Deploy Your App on AWS</Span>
      </Box>
      <Box type="row" justifyContent="center" mt={8}>
        <form onSubmit={handleSubmit(handleSignup)} style={{ width: "34vw" }}>
          <Box>
            <Box>
              <H5 m={2} ml="0px">
                EC2 Config
              </H5>
              <Para type="info">
                This specifies values that need to be configured for the
                instances storage, each block device needs to be added to the
                list separately. the defaults provided:
              </Para>
              <Label>Device Name</Label>
              <Box type="relative">
                <Input
                  name={"DeviceName"}
                  color="grey"
                  fontSize={3}
                  p={2}
                  value={deviceName}
                  width="100%"
                  ref={register}
                  mb={2}
                  onChange={(e) => setDeviceName(e.target.value)}
                />

                {errors?.name && (
                  <Span color="orange" mb={4}>
                    {errors?.name?.message}
                  </Span>
                )}
              </Box>
              <Label>Delete On Termination</Label>
              <Para type="info">
                if true all backed up sotrage and snapshots of volume are lost
                and instance cannot be reverted to it's initial AMI state.
              </Para>
              <Box type="relative">
                <Input
                  name={"DeleteOnTermination"}
                  color="grey"
                  fontSize={3}
                  p={2}
                  width="100%"
                  value={deleteOnTermination}
                  ref={register}
                  mb={2}
                  onChange={(e) => setDeleteOnTermination(e.target.value)}
                />

                {errors?.name && (
                  <Span color="orange" mb={4}>
                    {errors?.name?.message}
                  </Span>
                )}
              </Box>
              <Label>VolumeSize</Label>
              <Para type="info">
                VolumeSize specifies the size of the attached block device in
                GBs
              </Para>
              <Box type="relative">
                <Input
                  name={"VolumeSize"}
                  color="grey"
                  fontSize={3}
                  p={2}
                  width="100%"
                  value={volumeSize}
                  ref={register}
                  mb={2}
                  onChange={(e) => setVolumeSize(e.target.value)}
                />

                {errors?.name && (
                  <Span color="orange" mb={4}>
                    {errors?.name?.message}
                  </Span>
                )}
              </Box>
              <Label>Volume Type</Label>
              <Para type="info">
                VolumeType can be one of gp3, gp2 for General purpose SSD and
                one of io2, io1 for a Provisioned IOPS SSD, more information can
                be found [at]
                <a href="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html">
                  https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html
                </a>
              </Para>
              <Box type="relative">
                <Input
                  name={"VolumeType"}
                  color="grey"
                  fontSize={3}
                  p={2}
                  width="100%"
                  value={volumeType}
                  ref={register}
                  mb={2}
                  onChange={(e) => setVolumeType(e.target.value)}
                />

                {errors?.name && (
                  <Span color="orange" mb={4}>
                    {errors?.name?.message}
                  </Span>
                )}
              </Box>

              <Box style={{ textAlign: "center" }}>
                <Icon
                  as={BsPlusCircleFill}
                  w={"3.5rem"}
                  h={"3.5rem"}
                  color={"rgb(56 46 108 / 92%)"}
                  mt={5}
                  onClick={addDeviceHandler}
                />
              </Box>
              <Box>
                {deviceList.map((key, index) => {
                  // let user = Object.keys(key)[0];
                  console.log(index);
                  return (
                    <Box
                      boxShadow="card"
                      type="row"
                      justifyContent="space-between"
                      style={{
                        height: "50px",
                        backgroundColor: "rgb(241 218 249)",
                      }}
                      m={4}
                      p={2}
                    >
                      <Box type="row" justifyContent="flex-start">
                        <Icon
                          as={FaAws}
                          w={"1.5rem"}
                          h={"1.5rem"}
                          color={"rgb(157 57 160 / 87%)"}
                        />
                        {/* <Para ml={2}> {user}</Para> */}
                        <Para ml={2}> {key.DeviceName}</Para>
                      </Box>
                      <Box>
                        <Icon
                          as={AiOutlineDelete}
                          w={"1.5rem"}
                          h={"1.5rem"}
                          color={"red"}
                          onClick={() => removeDeviceHandler(index)}
                        />
                      </Box>
                    </Box>
                  );
                })}
              </Box>
              <Label>Instance Type</Label>
              <Box type="relative">
                <Input
                  name={"InstanceType"}
                  color="grey"
                  fontSize={3}
                  p={2}
                  required
                  width="100%"
                  defaultValue={ec2Config.ec2_config.InstanceType}
                  ref={register}
                  mb={2}
                  onChange={(e) => setInstanceType(e.target.value)}
                />

                {errors?.name && (
                  <Span color="orange" mb={4}>
                    {errors?.name?.message}
                  </Span>
                )}
              </Box>
              <Label>ImageId</Label>
              <Box type="relative">
                <Input
                  name={"ImageId"}
                  color="grey"
                  fontSize={3}
                  p={2}
                  required
                  defaultValue={ec2Config.ec2_config.ImageId}
                  width="100%"
                  ref={register}
                  mb={2}
                  onChange={(e) => setImageId(e.target.value)}
                />

                {errors?.name && (
                  <Span color="orange" mb={4}>
                    {errors?.name?.message}
                  </Span>
                )}
              </Box>
              <Button mt={4} width="100%" fontSize={18} type="submit">
                {"Deploy"}
              </Button>
            </Box>
          </Box>
        </form>
      </Box>
    </>
  );
};

const CARD_ELEMENT_OPTIONS = {
  style: {
    base: {
      color: "#32325d",
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: "antialiased",
      fontSize: "18px",
      "::placeholder": {
        color: "#aab7c4",
      },
    },
    invalid: {
      color: "#fa755a",
      iconColor: "#fa755a",
    },
  },
};

export default Aws;
