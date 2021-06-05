import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useGlobal } from "reactn";
import { Box, Button, Span, H5, Input, Label, Para } from "../../styles";
import { useQueryClient } from "react-query";
import { createStandaloneToast } from "@chakra-ui/react";
import Api, { APIURLS } from "../../Api";
import { useIsFetching } from "react-query";
import Select from "react-select";
import ClipLoader from "react-spinners/ClipLoader";

const RdsConfig = ({
  userCredential,
  setStep,
  userConfig,
  setUserCredential,
  rdsConfig,
  setEc2Config,
}) => {
  const { handleSubmit, register, errors } = useForm();

  const [selectedRds, setSelectedRds] = useState();
  const [loading, setLoading] = useState(false);

  let selectRds = [];
  if (rdsConfig.rds_config) {
    let data = rdsConfig.rds_config.Engine;
    for (let key in data) {
      selectRds.push({
        value: data[key],
        label: data[key],
      });
    }
  }

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
        },
        rds_config: {
          Engine: selectedRds,
          AllocatedStorage: parseInt(params.AllocatedStorage),
          DBInstanceIdentifier: params.DBInstanceIdentifier,
          DBInstanceClass: params.DBInstanceClass,
          MasterUsername: params.MasterUsername,
          MasterUserPassword: params.MasterUserPassword,
          MaxAllocatedStorage: parseInt(params.MaxAllocatedStorage),
        },
      };
      setUserCredential(obj);
      let { data } = await Api.post(APIURLS.getUserEc2Congif(), {
        aws_username: params.aws_username,
        aws_secret_key: params.aws_secret_key,
        aws_access_key: params.aws_access_key,
      });
      setEc2Config(data);
      setStep(4);
      setLoading(false);
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
                RDS Config
              </H5>

              <Label>Engine</Label>
              <Para type="info">
                AWS provides users a hassle free way to configure remote data
                storage for relational database stores through this service. The
                users may chose from an array of options.
              </Para>

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
                  onChange={({ value }) => setSelectedRds(value)}
                  theme={CARD_ELEMENT_OPTIONS}
                  placeholder="Select Engine"
                  options={selectRds}
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
                  defaultValue={rdsConfig.rds_config.AllocatedStorage}
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
              <Para type="info">
                Name of the DB to be given by the user the default should be app
                name
              </Para>
              <Box type="relative">
                <Input
                  name={"DBInstanceIdentifier"}
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
              <Label>DB Instance Class </Label>
              <Para type="info">
                depending on the region and the engine chosen, AWS will allow
                userschose form an array different machines with different
                hardware configurations. Refer to this doc for further details.
                <a href="https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html">
                  https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html
                </a>
              </Para>
              <Box type="relative">
                <Input
                  name={"DBInstanceClass"}
                  color="grey"
                  fontSize={3}
                  p={2}
                  required
                  defaultValue={rdsConfig.rds_config.DBInstanceClass}
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
              <Para type="info">
                The admin username for the master user of the RDS instace.
              </Para>
              <Box type="relative">
                <Input
                  name={"MasterUsername"}
                  color="grey"
                  fontSize={3}
                  p={2}
                  required
                  defaultValue={rdsConfig.rds_config.MasterUsername}
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
              <Para type="info">
                The admin password for the master user of the RDS instace.
              </Para>
              <Box type="relative">
                <Input
                  name={"MasterUserPassword"}
                  color="grey"
                  fontSize={3}
                  p={2}
                  required
                  defaultValue={rdsConfig.rds_config.MasterUserPassword}
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
              <Label>Max Allocated Storage</Label>
              <Para type="info">
                Minimum storage allocated in GB's minimum is 20 similarly max is
                1634
              </Para>
              <Box type="relative">
                <Input
                  name={"MaxAllocatedStorage"}
                  color="grey"
                  fontSize={3}
                  p={2}
                  required
                  defaultValue={rdsConfig.rds_config.MaxAllocatedStorage}
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

              {/* </Box> */}
              <Button mt={4} width="100%" fontSize={18} type="submit">
                {"Next"}
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

export default RdsConfig;
