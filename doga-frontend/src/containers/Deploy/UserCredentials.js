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

const Deploy = ({ setStep, setUserConfig, setUserCredential }) => {
  const [token] = useGlobal("token");
  const { handleSubmit, register, errors } = useForm();
  const [toggle, setToggle] = useState(true);
  const [selectedApp, setSelectedApp] = useState();
  const [loading, setLoading] = useState(false);
  const [provisionDb, setProvisionDb] = useState();
  // const queryClient = useQueryClient();
  const isFetching = useIsFetching();
  const toast = createStandaloneToast();
  const queryClient = useQueryClient();
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
    // setLoading(true);
    try {
      let obj = {
        app_name: selectedApp,
        aws_username: params.aws_username,
        aws_secret_key: params.aws_secret_key,
        aws_access_key: params.aws_access_key,
      };

      //   let { data } = await Api.post(APIURLS.awsExport(), obj);
      setUserCredential(obj);
      let { data } = await Api.post(APIURLS.getUserCongif(), {
        aws_username: params.aws_username,
        aws_secret_key: params.aws_secret_key,
        aws_access_key: params.aws_access_key,
      });
      console.log(data);
      setUserConfig(data);
      setStep(2);

      //   toast({
      //     title: "Success",
      //     description: data?.result,
      //     status: "success",
      //     duration: 9000,
      //     isClosable: false,
      //   });

      //   setLoading(false);
      //   onClose();
    } catch ({ response }) {
      //   setLoading(false);
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
