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
import Select from "react-select";
import CreateTable from "../../containers/Application/CreateTable";
import CreateDatabase from "../../containers/CreateDatabase/CreateDatabase";

const EditDatabase = ({ isOpen, onOpen, onClose, edit }) => {
  const [token] = useGlobal("token");
  const { handleSubmit, register, errors } = useForm();
  const [selectedFieldType, setSelectedFieldType] = useState();

  const queryClient = useQueryClient();

  const onCloseHandler = () => {
    onClose();
  };

  return (
    <>
      <Modal isOpen={isOpen} onClose={onCloseHandler}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>
            {" "}
            <Label>EDIT</Label>
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <CreateDatabase edit={edit} />
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};

// const CARD_ELEMENT_OPTIONS = {
//   style: {
//     base: {
//       color: "#32325d",
//       fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
//       fontSmoothing: "antialiased",
//       fontSize: "18px",
//       "::placeholder": {
//         color: "#aab7c4",
//       },
//     },
//     invalid: {
//       color: "#fa755a",
//       iconColor: "#fa755a",
//     },
//   },
// };

export default EditDatabase;
