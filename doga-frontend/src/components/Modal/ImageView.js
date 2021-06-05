import React from "react";
import { Box, Image, Label } from "../../styles";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
} from "@chakra-ui/react";

const ImageView = ({ isOpen, onOpen, onClose, imageView }) => {
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
            <Box>
              {" "}
              <Image src={`data:image/png;base64, ${imageView}`}></Image>
            </Box>
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};

export default ImageView;
