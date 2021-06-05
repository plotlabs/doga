import React from "react";
import { Box, H2, Label } from "../../styles";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
} from "@chakra-ui/react";

const RichTextView = ({ isOpen, onOpen, onClose, richText }) => {
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
