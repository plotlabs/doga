import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useGlobal } from "reactn";
import { Label } from "../../styles";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
} from "@chakra-ui/react";
import { useQueryClient } from "react-query";
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

export default EditDatabase;
