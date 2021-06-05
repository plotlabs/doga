import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { useGlobal } from "reactn";
import { Box, Button, Span, H5, Input, Label, Para } from "../../styles";
import { useQuery } from "react-query";
import Api, { APIURLS } from "../../Api";
import Select from "react-select";
import ClipLoader from "react-spinners/ClipLoader";

const Deploy = ({
  userCredential,
  setStep,
  userConfig,
  setUserCredential,
  setRdsConfig,
}) => {
  const [token] = useGlobal("token");
  const { handleSubmit, register, errors } = useForm();
  const [selectedRegion, setSelectedRegion] = useState();
  const [loading, setLoading] = useState(false);
  const { data } = useQuery([APIURLS.getContentType], {
    enabled: !!token,
  });

  let selectAppName = [];
  if (data) {
    for (let key in data) {
      selectAppName.push({
        value: key,
        label: key,
      });
    }
  }
  let selectRegion = [];
  if (userConfig.config) {
    let data = userConfig.config.region_name;
    for (let key in data) {
      selectRegion.push({
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
          aws_username: userCredential.aws_username,
          aws_secret_key: userCredential.aws_secret_key,
          aws_access_key: userCredential.aws_access_key,
        },
        config: {
          region_name: selectedRegion,
          signature_version: params.signature_version,
        },
      };

      setUserCredential(obj);
      let { data } = await Api.post(APIURLS.getUserRdsCongif(), {
        aws_username: params.aws_username,
        aws_secret_key: params.aws_secret_key,
        aws_access_key: params.aws_access_key,
      });

      setRdsConfig(data);
      setStep(3);
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
                Config
              </H5>

              <Label>Region Name</Label>
              <Para type="info">
                This indicates the region where the EC2 instance as well as RDS
                will be created in, please ensure you choose a region that has
                SSM, RDS and EC2 services.
                {/* Detialed information of the services can be found
[on amazons webpage](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/]) */}
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
                  onChange={({ value }) => setSelectedRegion(value)}
                  theme={CARD_ELEMENT_OPTIONS}
                  placeholder="Select App "
                  options={selectRegion}
                />
              </Box>

              <Label>Signature Version</Label>
              <Para type="info">
                This outlines the method used by AWS for authenticating
                requests. Version 4 is the most stable and reccomended protocol.
                {/* Detialed information of the services can be found
[on amazons webpage](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/]) */}
              </Para>
              <Box type="relative">
                <Input
                  name={"signature_version"}
                  color="grey"
                  fontSize={3}
                  p={2}
                  defaultValue={userConfig.config.signature_version}
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

export default Deploy;
