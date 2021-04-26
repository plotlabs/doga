import { useState } from "react";
import { Box, H2, Button, Para } from "../../styles";
import { Redirect } from "react-router-dom";
import ApplicationNext from "./ApplicationNext";
import CreateTable from "./CreateTable";
import CreateAppName from "./CreateAppName";
import CreateDatabase from "../CreateDatabase/CreateDatabase";
import { useQuery, useQueryClient } from "react-query";
import ClipLoader from "react-spinners/ClipLoader";
import { useEffect } from "reactn";
import { useIsFetching } from "react-query";
import CreateTableName from "./CreateTableName";

const Application = ({ isOpen, onOpen, onClose }) => {
  const [step, setStep] = useState(1);
  const [dash, setDash] = useState(false);
  const [fetch, setFetch] = useState();
  const queryClient = useQueryClient();
  const [connectionSelected, setConnectionSelected] = useState();
  const [appName, setAppName] = useState();
  const [tableName, setTableName] = useState();
  const [onLoading, setOnLoading] = useState(false);
  const isFetching = useIsFetching();

  const onCloseHandler = () => {};

  return (
    <>
      {/* <Modal isOpen={isOpen} onClose={onCloseHandler} size={"full"}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader></ModalHeader>
          <ModalCloseButton />
          <ModalBody> */}
      <Box width="100%">
        {step === 1 && (
          <CreateAppName setStep={setStep} setAppName={setAppName} />
        )}
        {step === 2 && <CreateDatabase setStep={setStep} appName={appName} />}
        {step === 3 && (
          <CreateTableName
            setStep={setStep}
            step={step}
            setTableName={setTableName}
          />
        )}
        {step === 4 && (
          <>
            {" "}
            <CreateTable
              step={step}
              setStep={setStep}
              connectionSelected={connectionSelected}
              appName={appName}
              onCloseHandler={onCloseHandler}
              tableName={tableName}
            />
          </>
        )}
        {step === 5 && (
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
      </Box>
      {/* </ModalBody>
        </ModalContent>
      </Modal> */}
    </>
  );
};

export default Application;
