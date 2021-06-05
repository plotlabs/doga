import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useGlobal } from "reactn";
import { Box, Button, Span, Input, Label } from "../../styles";
import Select from "react-select";
import { useQueryClient, useQuery } from "react-query";
import { createStandaloneToast } from "@chakra-ui/react";
import Api, { APIURLS } from "../../Api";
import ClipLoader from "react-spinners/ClipLoader";

const CreateDatabase = ({ edit, setStep, appName }) => {
  const { handleSubmit, register, errors } = useForm();
  const [loading, setLoading] = useState(false);
  const [apiErr, setApiErr] = useState(null);
  const queryClient = useQueryClient();
  const toast = createStandaloneToast();
  const [dbType, setDbType] = useState();

  const { data } = useQuery(APIURLS.getDbDefaults);

  async function handleSignup(params) {
    setLoading(true);
    try {
      let { data } = edit
        ? await Api.put(APIURLS.createDB, {
            ...params,
            database_type: dbType,
          })
        : await Api.post(APIURLS.createDB, {
            ...params,
            database_type: dbType,
          });
      await queryClient.refetchQueries([APIURLS.getDbConnections]);

      toast({
        title: "Database created successfully.",
        status: "success",
        duration: 9000,
        isClosable: false,
      });
      setLoading(false);
      setStep(3);
    } catch ({ response }) {
      toast({
        title: "An error occurred.",

        status: "error",
        duration: 9000,
        isClosable: true,
      });

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
        <Span type="heading">Congif Databse for your App </Span>
      </Box>
      <Box p={"300px"} pt={"50px"}>
        <form onSubmit={handleSubmit(handleSignup)}>
          <Label>Database/App Name</Label>
          <Box type="relative">
            <Input
              name="database_name"
              color="grey"
              required
              fontSize={3}
              p={2}
              defaultValue={edit ? edit.database_name : appName}
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

          <Label>Database Type</Label>
          <Box
            style={{
              marginBottom: "1.5rem",
              color: "#6E798C",
              fontSize: "1.25rem",
              paddingTop: "10px",
            }}
          >
            <Select
              key={1}
              onChange={({ value }) => setDbType(value)}
              required
              theme={CARD_ELEMENT_OPTIONS}
              placeholder="database_type"
              options={[
                {
                  value: "mysql",
                  label: "mysql",
                },
                {
                  value: "sqlite",
                  label: "sqlite",
                },
                {
                  value: "postgres",
                  label: "postgres",
                },
              ]}
            />
          </Box>
          <Label>Host</Label>
          <Box type="relative">
            <Input
              name="host"
              color="grey"
              fontSize={3}
              required
              p={2}
              defaultValue={edit ? edit.host : data?.host[dbType]}
              ref={register}
              width="100%"
              mb={2}
            />

            {errors?.password && (
              <Span color="orange" mb={4}>
                {errors?.password?.message}
              </Span>
            )}
          </Box>
          <Label>Port</Label>
          <Box type="relative">
            <Input
              name="port"
              color="grey"
              fontSize={3}
              required
              p={2}
              defaultValue={edit ? edit.port : data?.port[dbType]}
              ref={register}
              width="100%"
              mb={2}
            />

            {errors?.password && (
              <Span color="orange" mb={4}>
                {errors?.password?.message}
              </Span>
            )}
          </Box>
          <Label>Username</Label>
          <Box type="relative">
            <Input
              name="username"
              color="grey"
              fontSize={3}
              required
              p={2}
              defaultValue={edit ? edit.username : null}
              ref={register}
              width="100%"
              mb={2}
            />

            {errors?.password && (
              <Span color="orange" mb={4}>
                {errors?.password?.message}
              </Span>
            )}
          </Box>
          <Label>Password</Label>
          <Box type="relative">
            <Input
              name="password"
              type="password"
              color="grey"
              fontSize={3}
              p={2}
              defaultValue={""}
              ref={register}
              width="100%"
              mb={2}
            />

            {errors?.password && (
              <Span color="orange" mb={4}>
                {errors?.password?.message}
              </Span>
            )}
          </Box>

          {apiErr && (
            <Span color="orange" mb={4}>
              {apiErr}
            </Span>
          )}

          <Button mt={4} width="100%" fontSize={18} type="submit">
            {edit ? "Update" : "Create"}
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

export default CreateDatabase;
