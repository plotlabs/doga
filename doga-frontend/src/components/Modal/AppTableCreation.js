import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { Box, Label } from "../../styles";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
} from "@chakra-ui/react";
import { Redirect } from "react-router-dom";
import ClipLoader from "react-spinners/ClipLoader";
import { useIsFetching } from "react-query";
import CreateTable from "../../containers/Application/CreateTable";
import CreateTableName from "../../containers/Application/CreateTableName";

const AppTableCreation = ({
  isOpen,
  onOpen,
  onClose,
  appName,
  columns,
  basejwtPresent,
  tableNamePassed,
  edit,
}) => {
  const { handleSubmit, register, errors } = useForm();
  const [tableName, setTableName] = useState(tableNamePassed || null);
  const [newStep, setNewStep] = useState();
  const isFetching = useIsFetching();
  useEffect(() => {
    if (edit) {
      setNewStep(2);
    } else {
      setNewStep(1);
    }
  }, [edit]);

  async function onCloseHandler() {
    setTableName();

    if (edit) {
      setNewStep(2);
    } else {
      setNewStep(1);
    }
    onClose();
  }

  return (
    <>
      <Modal isOpen={isOpen} onClose={onCloseHandler} size={"10xl"}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>
            <Label>Create New Table </Label>
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            {newStep === 1 && (
              <CreateTableName
                setNewStep={setNewStep}
                setTableName={setTableName}
              />
            )}
            {newStep === 2 && (
              <>
                <CreateTable
                  appName={appName}
                  onCloseHandler={onCloseHandler}
                  columnsData={columns}
                  basejwtPresent={basejwtPresent}
                  setNewStep={setNewStep}
                  tableName={tableName}
                />
              </>
            )}
            {newStep === 3 && (
              <>
                <Box type="loader">
                  {isFetching ? (
                    <ClipLoader color={"#ffffff"} size={55} />
                  ) : (
                    <Redirect to="/dashboard" />
                  )}
                </Box>
              </>
            )}
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};

export default AppTableCreation;
