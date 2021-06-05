import { useState } from "react";
import { Box, H2, Para } from "../../styles";
import { Redirect } from "react-router-dom";
import UserCredentials from "./UserCredentials";
import UserConfig from "./UserConfig";
import { useGlobal } from "reactn";
import ClipLoader from "react-spinners/ClipLoader";
import { useEffect } from "reactn";
import RdsConfig from "./RdsConfig";
import Aws from "./Aws";

const Deploy = () => {
  const [step, setStep] = useState(1);
  const [deployProcessStatus, setdeployProcessStatus] = useGlobal("deploy");
  const [userConfig, setUserConfig] = useState();
  const [userCredential, setUserCredential] = useState();
  const [rdsConfig, setRdsConfig] = useState();
  const [ec2Config, setEc2Config] = useState();
  const [onLoading, setOnLoading] = useState(false);

  useEffect(() => {
    if (deployProcessStatus?.status === "COMPLETED") setdeployProcessStatus();
  }, [deployProcessStatus]);

  return (
    <>
      <Box width="100%">
        {step === 1 && (
          <UserCredentials
            setStep={setStep}
            setUserConfig={setUserConfig}
            setUserCredential={setUserCredential}
          />
        )}
        {step === 2 && (
          <UserConfig
            setStep={setStep}
            userConfig={userConfig}
            setUserCredential={setUserCredential}
            setRdsConfig={setRdsConfig}
            userCredential={userCredential}
          />
        )}
        {step === 3 && (
          <>
            <RdsConfig
              setStep={setStep}
              userConfig={userConfig}
              setUserCredential={setUserCredential}
              setEc2Config={setEc2Config}
              rdsConfig={rdsConfig}
              userCredential={userCredential}
            />
          </>
        )}
        {step === 4 && (
          <>
            <Aws
              setStep={setStep}
              userConfig={userConfig}
              ec2Config={ec2Config}
              setUserCredential={setUserCredential}
              rdsConfig={rdsConfig}
              userCredential={userCredential}
            />
          </>
        )}

        {step === 5 ? (
          <>
            {deployProcessStatus?.status === "INITIATED" ||
            deployProcessStatus?.status === "PROCESSING" ? (
              <>
                <Box type="heading" textAlign="center">
                  <H2>Status: {deployProcessStatus?.status.toLowerCase()}</H2>
                  <br />
                  <Para>{deployProcessStatus?.message}</Para>
                </Box>
                <Box type="loader">
                  <ClipLoader color={"#ffffff"} size={55} />
                </Box>
              </>
            ) : deployProcessStatus?.status === "COMPLETED" ? (
              <Redirect to="/dashboard" />
            ) : deployProcessStatus?.status === "ERROR" ? (
              <>
                <Box type="heading" textAlign="center">
                  <H2>Status: {deployProcessStatus?.status.toLowerCase()}</H2>
                  <br />
                  <Para>{deployProcessStatus?.message}</Para>
                </Box>
              </>
            ) : (
              <Box type="loader">
                <ClipLoader color={"#ffffff"} size={55} />
              </Box>
            )}
          </>
        ) : null}
      </Box>
    </>
  );
};

export default Deploy;
