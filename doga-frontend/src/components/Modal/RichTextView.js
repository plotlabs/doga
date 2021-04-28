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
// import { useQueryClient } from "react-query";
// import { useToast, createStandaloneToast } from "@chakra-ui/react";
// import Api, { setHeader, APIURLS } from "../../Api";
import { Icon } from "@chakra-ui/react";
import { useQuery, useQueryClient } from "react-query";
import { useToast, createStandaloneToast } from "@chakra-ui/react";
import Api, { setHeader, APIURLS } from "../../Api";

const RichTextView = ({ isOpen, onOpen, onClose, richText }) => {
  const [token] = useGlobal("token");
  const { handleSubmit, register, errors } = useForm();
  const [selectedFieldType, setSelectedFieldType] = useState();

  const queryClient = useQueryClient();

  const onCloseHandler = () => {
    onClose();
  };

  return (
    <>
      <Modal isOpen={isOpen} onClose={onCloseHandler} size={"10xl"}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>
            {" "}
            <Label></Label>
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Box type="heading" textAlign="center">
              {/* <Span type="heading">{table}</Span> */}
              <H2>Your Rich Text View</H2>
            </Box>
            <Box m={11} mt={8}>
              <div
                key="some_unique_key"
                class="ck-content"
                dangerouslySetInnerHTML={{
                  __html: richText,
                }}
              />
            </Box>
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};

export default RichTextView;
