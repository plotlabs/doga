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
import { Redirect } from "react-router-dom";
import { Icon } from "@chakra-ui/react";
import { useQuery, useQueryClient } from "react-query";
import { useToast, createStandaloneToast } from "@chakra-ui/react";
import Api, { setHeader, APIURLS } from "../../Api";
import Select from "react-select";
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
  const [token] = useGlobal("token");
  const { handleSubmit, register, errors } = useForm();
  const [selectedFieldType, setSelectedFieldType] = useState();
  const [tableName, setTableName] = useState(tableNamePassed || null);
  const [newStep, setNewStep] = useState();
  const queryClient = useQueryClient();
  // const isFetching = useIsFetching();
  const isFetching = useIsFetching();
  // const isFetchingApps = useIsFetching([APIURLS.getContentType]);
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
  console.log(
    "step",
    newStep,
    "tableNmae",
    tableName,
    "tableNamePassed",
    tableNamePassed
  );
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

export default AppTableCreation;
