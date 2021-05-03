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

const ImageView = ({ isOpen, onOpen, onClose, imageView }) => {
  const [token] = useGlobal("token");
  const { handleSubmit, register, errors } = useForm();
  const [selectedFieldType, setSelectedFieldType] = useState();

  const queryClient = useQueryClient();

  const onCloseHandler = () => {
    onClose();
  };
  console.log("iamgesrc", imageView);

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
            <Box>
              {" "}
              <Image
                src={`data:image/png;base64, ${imageView}`}

                // src="/Users/nishantrana/Desktop/doga/doga-frontend/public/uploads/654fdb5dc9eab375a46bdd1c17f4f051.jpg"
              ></Image>
            </Box>
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};

export default ImageView;