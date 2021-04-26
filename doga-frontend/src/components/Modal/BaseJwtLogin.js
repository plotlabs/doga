import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
// import { useGlobal } from "reactn";
import { NavLink } from "react-router-dom";
import { useGlobal } from "reactn";
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
import { useQuery, useQueryClient } from "react-query";
import { useToast, createStandaloneToast } from "@chakra-ui/react";
import Api, { setJwtHeader, APIURLS } from "../../Api";
import Select from "react-select";

const BaseJwtLogin = ({ isOpen, onOpen, onClose, app, table, basejwt }) => {
  const [token] = useGlobal("token");
  const { handleSubmit, register, errors } = useForm();
  const [selectedFieldType, setSelectedFieldType] = useState();
  const [jwtToken, setJwtToken] = useGlobal("jwtToken");
  const queryClient = useQueryClient();
  const toast = createStandaloneToast();
  let fields = null;
  if (basejwt) {
    fields = Object.entries(basejwt?.filter_keys).map(([prop, val]) => {
      return (
        <>
          <Label>{val}</Label>
          <Box type="relative">
            <Input
              name={val}
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
          </Box>{" "}
        </>
      );
    });
  }

  async function handleSignup(params) {
    console.log(params);
    try {
      console.log("Here");
      let { data } = await Api.post(
        APIURLS.baseJwtLogin({ app, table }),
        params
      );
      console.log(data);
      let jwtToken = data?.access_token;

      localStorage.setItem("jwtToken", jwtToken);

      setJwtHeader(jwtToken);
      setJwtToken(jwtToken);

      toast({
        title: "Success",
        description: data?.result,
        status: "success",
        duration: 9000,
        isClosable: false,
      });
      await queryClient.refetchQueries([
        APIURLS.getTableContent({ app, table }),
        "jwt_info",
      ]);
      onClose();
      console.log("there", data);
    } catch ({ response }) {
      toast({
        title: "An error occurred.",
        description: response?.data?.result,
        status: "error",
        duration: 9000,
        isClosable: true,
      });
      console.log(response);
    }
  }

  return (
    <>
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>
            {" "}
            <Label>Login </Label>
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Box type="row" justifyContent="center" m={6}>
              <form
                onSubmit={handleSubmit(handleSignup)}
                style={{ width: "35vw" }}
              >
                {fields}
                <Button mt={4} width="100%" fontSize={18} type="submit">
                  {"Login"}
                </Button>
              </form>
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

export default BaseJwtLogin;
