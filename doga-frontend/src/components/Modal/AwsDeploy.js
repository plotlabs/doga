import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { useGlobal } from "reactn";
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
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
} from "@chakra-ui/react";
import { Icon } from "@chakra-ui/react";
import { SiAmazonaws, SiHeroku } from "react-icons/si";
import { useQuery, useQueryClient } from "react-query";
import { useToast, createStandaloneToast } from "@chakra-ui/react";
import Api, { setHeader, APIURLS, ApiJwt } from "../../Api";
import Select from "react-select";

const AwsDeploy = ({
  isOpen,
  onOpen,
  onClose,
  //   app,
  //   columns,
  //   table,
  //   editDataId,
  //   basejwt,
  //   restrictByJwt,
}) => {
  const [token] = useGlobal("token");
  const { handleSubmit, register, errors } = useForm();
  const [toggle, setToggle] = useState(true);
  // const queryClient = useQueryClient();
  const toast = createStandaloneToast();
  const queryClient = useQueryClient();
  //   const { data } = useQuery([APIURLS.getContentType], {
  //     enabled: !!token,
  //   });

  //   let contentTypeApps = null;
  let selectAppName = [];
  //   if (data) {
  //     for (let key in data) {
  //       selectAppName.push({
  //         value: key,
  //         label: key,
  //       });
  //     }
  //   }
  //   const columnTypes = useQuery(APIURLS.getColumnTypes);
  //   const contentType = useQuery([APIURLS.getContentType], {
  //     enabled: !!token,
  //   });
  //   const { data } = useQuery(
  //     [APIURLS.getTableContentById({ app, table, editDataId }), basejwt],
  //     {
  //       enabled: !!token,
  //     }
  //   );
  //   console.log(data?.result);
  //   const [loading, setLoading] = useState(false);
  //   const [success, setSuccess] = useState(false);
  //   const [apiErr, setApiErr] = useState(null);
  //   const queryClient = useQueryClient();
  //   const toast = createStandaloneToast();
  //   console.log(restrictByJwt);

  async function handleSignup(params) {
    try {
      //   let obj = {
      //     app_name: params.app_name,
      //     user_credentials: {
      //       aws_username: params.aws_username,
      //       aws_secret_key: params.aws_secret_key,
      //       aws_access_key: params.aws_access_key,
      //     },
      //     config: {
      //       region_name: params.region_name,
      //       signature_version: params.signature_version,
      //       //  "retries": {
      //       //      "max_attempts":"string",
      //       //      "mode": "string"
      //       //      }
      //     },
      //     rds_config: {
      //       Engine: params.Engine,
      //       AllocatedStorage: params.AllocatedStorage,
      //       DBInstanceIdentifier: params.DBInstanceIdentifier,
      //       DBInstanceClass: params.DBInstanceClass,
      //       MasterUsername: params.MasterUsername,
      //       MasterUserPassword: params.MasterUserPassword,
      //       MaxAllocatedStorage: params.MaxAllocatedStorage,
      //     },
      //     ec2_config: {
      //       BlockDeviceMappings: [
      //         {
      //           DeviceName: params.DeviceName,
      //           Ebs: {
      //             DeleteOnTermination: params.DeleteOnTermination,
      //             VolumeSize: params.VolumeSize,
      //             VolumeType: params.VolumeType,
      //           },
      //         },
      //       ],
      //       InstanceType: params.InstanceType,
      //       ImageId: params.ImageId,
      //     },
      //   };
      //   let { data } = await Api.post(APIURLS.awsExport(), obj);
      let obj = {
        app_name: "value",
        provision_db: false,
        // "tier": "hobby-dev"
      };
      let { data } = await Api.post(APIURLS.herokuExport(), obj);

      toast({
        title: "Success",
        description: data?.result,
        status: "success",
        duration: 9000,
        isClosable: false,
      });
      //   await queryClient.refetchQueries([
      //     APIURLS.getTableContent({ app, table }),
      //     "jwt_info",
      //   ]);

      onClose();
    } catch ({ response }) {}
  }

  return (
    <>
      <Modal isOpen={isOpen} onClose={onClose} size={"large"}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>
            {" "}
            <Label>DEPLOY </Label>
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Box type="row" justifyContent="center">
              <Button
                type="toggleTable"
                style={{
                  width: "20vw",
                  color: toggle ? "white" : "purple",
                  backgroundImage: toggle
                    ? "linear-gradient(to right, #7f00ff, #8b008bd4)"
                    : "none",
                }}
                onClick={() => {
                  setToggle(true);
                }}
              >
                <Icon
                  as={SiAmazonaws}
                  w={"2.5rem"}
                  h={"1.5rem"}
                  color={toggle ? "white" : "purple"}
                  mr={2}
                />
                AWS
              </Button>
              <Button
                type="toggleTable"
                style={{
                  width: "20vw",
                  color: !toggle ? "white" : "purple",
                  backgroundImage: !toggle
                    ? "linear-gradient(to right, #7f00ff, #8b008bd4)"
                    : "none",
                }}
                onClick={() => {
                  setToggle(false);
                }}
              >
                <Icon
                  as={SiHeroku}
                  w={"2.5rem"}
                  h={"1.5rem"}
                  color={!toggle ? "white" : "purple"}
                  mr={2}
                />{" "}
                Heroku
              </Button>{" "}
            </Box>
            <Box type="row" justifyContent="center" m={6}>
              {toggle ? (
                <form
                  onSubmit={handleSubmit(handleSignup)}
                  style={{ width: "35vw" }}
                >
                  <Label>App name</Label>
                  <Box
                    style={{
                      marginBottom: "1.5rem",
                      color: "#6E798C",
                      fontSize: "1.25rem",
                    }}
                  >
                    <Select
                      key={1}
                      required
                      theme={CARD_ELEMENT_OPTIONS}
                      placeholder="Select App "
                      options={selectAppName}
                    />
                  </Box>
                  <H5 m={2} ml="0px">
                    Credentials
                  </H5>
                  <Label>AWS Username</Label>
                  <Box type="relative">
                    <Input
                      name={"aws_username"}
                      color="grey"
                      required
                      fontSize={3}
                      p={2}
                      // defaultValue={editDataId ? data?.result[val.name] : null}
                      width="100%"
                      ref={register}
                      mb={2}
                    />

                    {errors?.name && (
                      <Span color="orange" mb={4}>
                        {errors?.name?.message}
                      </Span>
                    )}
                  </Box>
                  <Label>AWS Secret Key</Label>
                  <Box type="relative">
                    <Input
                      name={"aws_secret_key"}
                      color="grey"
                      required
                      fontSize={3}
                      p={2}
                      // defaultValue={editDataId ? data?.result[val.name] : null}
                      width="100%"
                      ref={register}
                      mb={2}
                    />

                    {errors?.name && (
                      <Span color="orange" mb={4}>
                        {errors?.name?.message}
                      </Span>
                    )}
                  </Box>
                  <Label>AWS Access Key</Label>
                  <Box type="relative">
                    <Input
                      name={"aws_access_key"}
                      color="grey"
                      required
                      fontSize={3}
                      p={2}
                      // defaultValue={editDataId ? data?.result[val.name] : null}
                      width="100%"
                      ref={register}
                      mb={2}
                    />

                    {errors?.name && (
                      <Span color="orange" mb={4}>
                        {errors?.name?.message}
                      </Span>
                    )}
                  </Box>
                  <H5 m={2} ml="0px">
                    Config
                  </H5>

                  <Label>Region Name</Label>
                  <Box type="relative">
                    <Input
                      name={"region_name"}
                      color="grey"
                      fontSize={3}
                      p={2}
                      // defaultValue={editDataId ? data?.result[val.name] : null}
                      width="100%"
                      ref={register}
                      mb={2}
                    />

                    {errors?.name && (
                      <Span color="orange" mb={4}>
                        {errors?.name?.message}
                      </Span>
                    )}
                  </Box>
                  <Label>Signature Version</Label>
                  <Box type="relative">
                    <Input
                      name={"signature_version"}
                      color="grey"
                      fontSize={3}
                      p={2}
                      // defaultValue={editDataId ? data?.result[val.name] : null}
                      width="100%"
                      ref={register}
                      mb={2}
                    />

                    {errors?.name && (
                      <Span color="orange" mb={4}>
                        {errors?.name?.message}
                      </Span>
                    )}
                  </Box>
                  <H5 m={2} ml="0px">
                    RDS Config
                  </H5>
                  <Label>Engine</Label>
                  <Box
                    style={{
                      marginBottom: "1.5rem",
                      color: "#6E798C",
                      fontSize: "1.25rem",
                    }}
                  >
                    <Select
                      key={1}
                      required
                      theme={CARD_ELEMENT_OPTIONS}
                      placeholder="Select Engine type"
                      options={[
                        {
                          value: "MySQL",
                          label: "MySQL",
                        },
                        {
                          value: "SQLite",
                          label: "SQLite",
                        },
                        {
                          value: "Postgres",
                          label: "Postgres",
                        },
                      ]}
                    />
                  </Box>
                  <Label>Allocated Storage </Label>
                  <Box type="relative">
                    <Input
                      name={"AllocatedStorage"}
                      color="grey"
                      fontSize={3}
                      p={2}
                      required
                      // defaultValue={editDataId ? data?.result[val.name] : null}
                      width="100%"
                      ref={register}
                      mb={2}
                    />

                    {errors?.name && (
                      <Span color="orange" mb={4}>
                        {errors?.name?.message}
                      </Span>
                    )}
                  </Box>
                  <Label>DB Instance Identifier </Label>
                  <Box type="relative">
                    <Input
                      name={"DBInstanceIdentifier"}
                      color="grey"
                      fontSize={3}
                      p={2}
                      required
                      // defaultValue={editDataId ? data?.result[val.name] : null}
                      width="100%"
                      ref={register}
                      mb={2}
                    />

                    {errors?.name && (
                      <Span color="orange" mb={4}>
                        {errors?.name?.message}
                      </Span>
                    )}
                  </Box>
                  <Label>DB Instance Class </Label>
                  <Box type="relative">
                    <Input
                      name={"DBInstanceClass"}
                      color="grey"
                      fontSize={3}
                      p={2}
                      required
                      // defaultValue={editDataId ? data?.result[val.name] : null}
                      width="100%"
                      ref={register}
                      mb={2}
                    />

                    {errors?.name && (
                      <Span color="orange" mb={4}>
                        {errors?.name?.message}
                      </Span>
                    )}
                  </Box>
                  <Label>Master Username </Label>
                  <Box type="relative">
                    <Input
                      name={"MasterUsername"}
                      color="grey"
                      fontSize={3}
                      p={2}
                      required
                      // defaultValue={editDataId ? data?.result[val.name] : null}
                      width="100%"
                      ref={register}
                      mb={2}
                    />

                    {errors?.name && (
                      <Span color="orange" mb={4}>
                        {errors?.name?.message}
                      </Span>
                    )}
                  </Box>
                  <Label>Master User Password </Label>
                  <Box type="relative">
                    <Input
                      name={"MasterUserPassword"}
                      color="grey"
                      fontSize={3}
                      p={2}
                      required
                      // defaultValue={editDataId ? data?.result[val.name] : null}
                      width="100%"
                      ref={register}
                      mb={2}
                    />

                    {errors?.name && (
                      <Span color="orange" mb={4}>
                        {errors?.name?.message}
                      </Span>
                    )}
                  </Box>
                  <Label>MaxAllocatedStorage</Label>
                  <Box type="relative">
                    <Input
                      name={"MaxAllocatedStorage"}
                      color="grey"
                      fontSize={3}
                      p={2}
                      required
                      // defaultValue={editDataId ? data?.result[val.name] : null}
                      width="100%"
                      ref={register}
                      mb={2}
                    />

                    {errors?.name && (
                      <Span color="orange" mb={4}>
                        {errors?.name?.message}
                      </Span>
                    )}
                  </Box>
                  <H5 m={2} ml="0px">
                    EC2 Config
                  </H5>
                  <Label>Device Name</Label>
                  <Box type="relative">
                    <Input
                      name={"DeviceName"}
                      color="grey"
                      fontSize={3}
                      p={2}
                      required
                      width="100%"
                      ref={register}
                      mb={2}
                    />

                    {errors?.name && (
                      <Span color="orange" mb={4}>
                        {errors?.name?.message}
                      </Span>
                    )}
                  </Box>
                  <Label>Delete On Termination</Label>
                  <Box type="relative">
                    <Input
                      name={"DeleteOnTermination"}
                      color="grey"
                      fontSize={3}
                      p={2}
                      required
                      width="100%"
                      ref={register}
                      mb={2}
                    />

                    {errors?.name && (
                      <Span color="orange" mb={4}>
                        {errors?.name?.message}
                      </Span>
                    )}
                  </Box>
                  <Label>VolumeSize</Label>
                  <Box type="relative">
                    <Input
                      name={"VolumeSize"}
                      color="grey"
                      fontSize={3}
                      p={2}
                      required
                      width="100%"
                      ref={register}
                      mb={2}
                    />

                    {errors?.name && (
                      <Span color="orange" mb={4}>
                        {errors?.name?.message}
                      </Span>
                    )}
                  </Box>
                  <Label>Volume Type</Label>
                  <Box type="relative">
                    <Input
                      name={"VolumeType"}
                      color="grey"
                      fontSize={3}
                      p={2}
                      required
                      width="100%"
                      ref={register}
                      mb={2}
                    />

                    {errors?.name && (
                      <Span color="orange" mb={4}>
                        {errors?.name?.message}
                      </Span>
                    )}
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
                      ref={register}
                      mb={2}
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
                </form>
              ) : (
                <form
                  onSubmit={handleSubmit(handleSignup)}
                  style={{ width: "35vw" }}
                >
                  <Label>App name</Label>
                  <Box
                    style={{
                      marginBottom: "1.5rem",
                      color: "#6E798C",
                      fontSize: "1.25rem",
                    }}
                  >
                    <Select
                      key={1}
                      required
                      theme={CARD_ELEMENT_OPTIONS}
                      placeholder="Select App "
                      options={selectAppName}
                    />
                  </Box>
                  <Label>provision DB</Label>
                  <Box type="relative">
                    <Input
                      name={"provision_db"}
                      color="grey"
                      fontSize={3}
                      p={2}
                      required
                      width="100%"
                      ref={register}
                      mb={2}
                    />

                    {errors?.name && (
                      <Span color="orange" mb={4}>
                        {errors?.name?.message}
                      </Span>
                    )}
                  </Box>
                  {/* <Label>Tier</Label>
                  <Box type="relative">
                    <Input
                      name={"tier"}
                      color="grey"
                      fontSize={3}
                      p={2}
                      required
                      width="100%"
                      ref={register}
                      mb={2}
                    />

                    {errors?.name && (
                      <Span color="orange" mb={4}>
                        {errors?.name?.message}
                      </Span>
                    )}
                  </Box> */}
                  <Button mt={4} width="100%" fontSize={18} type="submit">
                    {"Deploy"}
                  </Button>
                </form>
              )}
            </Box>
          </ModalBody>
        </ModalContent>
      </Modal>
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

export default AwsDeploy;
