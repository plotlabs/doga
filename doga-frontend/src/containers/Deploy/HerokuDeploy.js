import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useGlobal } from "reactn";
import { Box, Button, Span, Label } from "../../styles";
import { useQuery, useQueryClient } from "react-query";
import { createStandaloneToast } from "@chakra-ui/react";
import Api, { APIURLS } from "../../Api";
import { useIsFetching } from "react-query";
import Select from "react-select";
import ClipLoader from "react-spinners/ClipLoader";

const HerokuDeploy = () => {
  const [token] = useGlobal("token");
  const { handleSubmit, register, errors } = useForm();
  const [selectedApp, setSelectedApp] = useState();
  const [loading, setLoading] = useState(false);
  const [provisionDb, setProvisionDb] = useState();
  const toast = createStandaloneToast();
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
      };
      let { data } = await Api.post(APIURLS.herokuExport(), obj);

      toast({
        title: "Success",
        description: data?.result,
        status: "success",
        duration: 9000,
        isClosable: false,
      });
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
