import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useGlobal } from "reactn";
import { Box, Button, Span, H5, Input, Label } from "../../styles";
import { useQuery, useQueryClient } from "react-query";
import { createStandaloneToast } from "@chakra-ui/react";
import Api, { APIURLS } from "../../Api";
import { useIsFetching } from "react-query";
import Select from "react-select";
import ClipLoader from "react-spinners/ClipLoader";

const Deploy = ({ setStep, setUserConfig, setUserCredential }) => {
  const [token] = useGlobal("token");
  const { handleSubmit, register, errors } = useForm();
  const [selectedApp, setSelectedApp] = useState();
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

  async function handleSignup(params) {
    try {
      let obj = {
        app_name: selectedApp,
        aws_username: params.aws_username,
        aws_secret_key: params.aws_secret_key,
        aws_access_key: params.aws_access_key,
      };

      setUserCredential(obj);
      let { data } = await Api.post(APIURLS.getUserCongif(), {
        aws_username: params.aws_username,
        aws_secret_key: params.aws_secret_key,
        aws_access_key: params.aws_access_key,
      });
      setUserConfig(data);
      setStep(2);
    } catch ({ response }) {}
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
              <Label mt={8}>App name</Label>
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
                  onChange={({ value }) => setSelectedApp(value)}
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
