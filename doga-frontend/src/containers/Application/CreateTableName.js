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

const CreateTableName = ({ setStep, setTableName, setNewStep, step }) => {
  const { handleSubmit, register, errors } = useForm();

  async function handleSignup(params) {
    setTableName(params.tableName);
    if (step) {
      setStep(4);
    } else {
      setNewStep(2);
    }
  }

  return (
    <>
      <Box display="grid" gridTemplateColumns="1fr" gridGap={8} height="100%">
        <Box type="row" flexDirection="column" justifyContent="center">
          <Box type="heading" textAlign="center">
            <Span type="heading">Create New Table </Span>
            {/* <Box my={2} borderBottom="4px solid" borderColor="orange"></Box> */}
          </Box>

          <Box
            type="row"
            justifyContent="center"
            m={6}
            mt={"50px"}
            mb={"500px"}
          >
            <form
              onSubmit={handleSubmit(handleSignup)}
              style={{ width: "35vw" }}
            >
              <Label>Table Name </Label>
              <Box type="relative">
                <Input
                  name="tableName"
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

export default CreateTableName;
