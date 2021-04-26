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

const HerokuDeploy = () => {
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
    setLoading(true);
    try {
      let obj = {
        app_name: selectedApp,
        provision_db: provisionDb,
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
        <Span type="heading">Deploy Your App on Heroku</Span>
      </Box>
      <Box type="row" justifyContent="center" mt={8}>
        <form onSubmit={handleSubmit(handleSignup)} style={{ width: "35vw" }}>
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
              onChange={({ value }) => setSelectedApp(value)}
              theme={CARD_ELEMENT_OPTIONS}
              placeholder="Select App "
              options={selectAppName}
            />
          </Box>
          <Label>provision DB</Label>

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
              onChange={({ value }) => setProvisionDb(value)}
              theme={CARD_ELEMENT_OPTIONS}
              placeholder="provision DB"
              options={[
                {
                  value: true,
                  label: "True",
                },
                {
                  value: false,
                  label: "False",
                },
              ]}
            />
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

export default HerokuDeploy;
