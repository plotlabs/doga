import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useGlobal } from "reactn";
import { Box, Button, Span, Input, Label } from "../../styles";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
} from "@chakra-ui/react";
import { useQueryClient } from "react-query";
import { createStandaloneToast } from "@chakra-ui/react";
import Api, { setJwtHeader, APIURLS } from "../../Api";

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
    try {
      let { data } = await Api.post(
        APIURLS.baseJwtLogin({ app, table }),
        params
      );

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
    } catch ({ response }) {
      toast({
        title: "An error occurred.",
        description: response?.data?.result,
        status: "error",
        duration: 9000,
        isClosable: true,
      });
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

export default BaseJwtLogin;
