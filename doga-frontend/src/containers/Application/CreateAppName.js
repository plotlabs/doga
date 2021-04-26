import React, { useState, useEffect } from "react";
import {
  Box,
  ResponsiveImage,
  Image,
  Button,
  StyledLink,
  Span,
  MotionBox,
  H2,
  H1,
  Input,
  Label,
} from "../../styles";
import { useForm } from "react-hook-form";

const CreateAppName = ({ setStep, setAppName }) => {
  const { handleSubmit, register, errors } = useForm();

  async function handleSignup(params) {
    setAppName(params.appName);
    setStep(2);
  }

  return (
    <>
      <Box display="grid" gridTemplateColumns="1fr" gridGap={8} height="100%">
        <Box type="row" flexDirection="column" justifyContent="center">
          <Box type="heading" textAlign="center">
            <Span type="heading">Create New App </Span>
            {/* <Box my={2} borderBottom="4px solid" borderColor="orange"></Box> */}
          </Box>

          <Box type="row" justifyContent="center" m={6} mt={"50px"}>
            <form
              onSubmit={handleSubmit(handleSignup)}
              style={{ width: "35vw" }}
            >
              <Label>App Name </Label>
              <Box type="relative">
                <Input
                  name="appName"
                  color="grey"
                  required
                  pattern="^([a-z]+[0-9_]*)*$"
                  fontSize={3}
                  p={2}
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
            </form>
          </Box>
          {/* </Box> */}
        </Box>
      </Box>
    </>
  );
};

export default CreateAppName;
