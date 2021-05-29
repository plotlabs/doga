import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { useGlobal } from "reactn";
import { NavLink } from "react-router-dom";
import Api, { setHeader, APIURLS, setDefaultBaseUrl } from "../../Api";
import { useQuery, useQueryClient } from "react-query";
import {
  Box,
  ResponsiveImage,
  Image,
  Button,
  StyledLink,
  Span,
  MotionBox,
  H2,
  H6,
  H3,
  Input,
  Label,
  H5,
  Para,
} from "../../styles";
import {
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuItemOption,
  MenuGroup,
  MenuOptionGroup,
  MenuIcon,
  MenuCommand,
  MenuDivider,
} from "@chakra-ui/react";
import { Icon } from "@chakra-ui/react";
import { FaUserAlt, FaDatabase } from "react-icons/fa";
import { FcAcceptDatabase } from "react-icons/fc";
import { IoAppsSharp } from "react-icons/io5";
import { SiAmazonaws } from "react-icons/si";
import { BsFillLockFill } from "react-icons/bs";
import { BsAppIndicator, BsTable } from "react-icons/bs";
import { TiExport } from "react-icons/ti";
import { useToast, createStandaloneToast } from "@chakra-ui/react";
import { AiOutlineCloudServer } from "react-icons/ai";
import { useDisclosure } from "@chakra-ui/react";
import CreateDatabase from "../CreateDatabase/CreateDatabase";
import Application from "../Application/Application";
import AwsDeploy from "../../components/Modal/AwsDeploy";

import { IoRocketSharp } from "react-icons/io5";
import { useIsFetching } from "react-query";
import ClipLoader from "react-spinners/ClipLoader";
import { Chart } from "chart.js";
import { Doughnut, Line } from "react-chartjs-2";
import { useParams } from "react-router";
import AppTableCreation from "../../components/Modal/AppTableCreation";
import DoughnutChart from "./DoughnutChart";
const AppHome = () => {
  let { app } = useParams();
  const [baseURL, setBaseURL] = useGlobal("baseURL");
  // const [selectedBaseUrl, setSelectedBaseUrl] = useState(
  //   baseURL[app]?.selected || "http://0.0.0.0:8080/"
  // );
  const queryClient = useQueryClient();
  const userProfile = useQuery(APIURLS.userInfo);
  const toast = createStandaloneToast();
  //   const appsCreated = useQuery(APIURLS.dashboardInfo(app, all));
  const { data, isLoading } = useQuery(APIURLS.appStats(app));

  useEffect(() => {
    setDefaultBaseUrl(baseURL[app]?.selected || "http://0.0.0.0:8080/");
  }, [app, baseURL]);
  useEffect(() => {
    setBaseURL({
      ...baseURL,
      [app]: {
        options: [
          "http://0.0.0.0:8080/",
          data?.deployment_info?.deployment_url?.[0],
        ],
        selected: baseURL[app]?.selected || "http://0.0.0.0:8080/",
      },
    });
  }, [app, data]);
  console.log(baseURL, "outBASEURL");
  const appDocs = useQuery(APIURLS.appDocs(app));

  const appData = useQuery(APIURLS.getContentType);

  const dbConnections = useQuery(APIURLS.getDbConnections);
  const { isOpen, onOpen, onClose } = useDisclosure();

  const [openModal, setOpenModal] = useState();
  const openModalHandler = (key) => {
    setOpenModal(key);
    onOpen();
  };
  const isFetching = useIsFetching();

  async function exportAppHandler() {
    try {
      let { data } = await Api.post(APIURLS.exportApp(), {
        app_name: app,
      });

      toast({
        title: "Data Added.",
        description: data?.result,
        status: "success",
        duration: 9000,
        isClosable: false,
      });
    } catch ({ response }) {
      toast({
        title: "An error occurred.",
        description: response?.data?.result,
        status: "error",
        duration: 9000,
        isClosable: true,
      });
    }
  }

  let relation = null;

  if (data != null && data.relationships) {
    relation = data?.relationships.map((key) => {
      return (
        <>
          <Box
            type="row"
            style={{ borderRight: "1px solid gray", paddingRight: "30px" }}
          >
            <Box
              type="column"
              style={{
                textAlign: "center",
                padding: "12px",
              }}
            >
              <H5 color={"#6E798C"} style={{ fontSize: "1.15rem" }}>
                {/* {"table Name: "} */}
                {key.relation_from.table_name}
              </H5>
              <H5 color={"#6E798C"} style={{ fontSize: "1.15rem" }}>
                {/* {"Field: "} */}
                {key.relation_from.column_name}
              </H5>
              <Para
                color={"#6E798C"}
                style={{
                  fontWeight: "600",
                  color: "purple",
                  whiteSpace: "nowrap",
                  fontSize: "1.15rem",
                }}
              >
                {"Relation From"}
              </Para>
            </Box>
            <Box type="column" style={{ alignItems: "center" }}>
              <Para style={{ paddinLeft: "45px" }}>{key.relation_type}</Para>
              <Image src={`/${key.relation_type}.png`}></Image>
            </Box>
            <Box
              type="column"
              style={{
                textAlign: "center",
              }}
            >
              <H5 color={"#6E798C"} style={{ fontSize: "1.15rem" }}>
                {/* {"table Name: "} */}
                {key.relation_to.table_name}
              </H5>
              <H5 color={"#6E798C"} style={{ fontSize: "1.15rem" }}>
                {/* {"Field: "} */}
                {key.relation_to.column_name}
              </H5>
              <Para
                color={"#6E798C"}
                style={{
                  fontWeight: "600",
                  color: "purple",
                  whiteSpace: "nowrap",
                  fontSize: "1.15rem",
                }}
              >
                {"Relation To"}
              </Para>
            </Box>
          </Box>
        </>
      );
    });
  }

  const urlChangeHandler = (value) => {
    setBaseURL({
      ...baseURL,
      [app]: {
        options: [
          "http://0.0.0.0:8080/",
          data?.deployment_info?.deployment_url?.[0],
        ],
        selected: value,
      },
    });
  };
  return false ? (
    <Box type="loader">
      <ClipLoader color={"#ffffff"} size={55} />
    </Box>
  ) : (
    <>
      {openModal === 3 ? (
        <AppTableCreation
          isOpen={isOpen}
          onOpen={onOpen}
          onClose={onClose}
          appName={app}
          basejwtPresent={
            appData.data != null &&
            appData.data[app]["jwt_info"] &&
            appData.data[app]["jwt_info"]
              ? appData.data[app]["jwt_info"]
              : null
          }
          // connectionSelected={data[id].connection_name}
          // columns={data[id].columns}
        />
      ) : null}
      <Box type="heading" textAlign="center">
        <Box type="row" justifyContent="spacing-around">
          <H2> {app}</H2>
          <Box type="row" width={"45%"}>
            <Button onClick={() => openModalHandler(3)}>
              Create New Table
            </Button>
            <Button onClick={() => exportAppHandler()}>Export Your App</Button>
            {/* <Button>Deploy Your App</Button> */}
            <NavLink to={`/application/docs/${app}`}>
              <Button>App Docs</Button>
            </NavLink>
          </Box>
        </Box>
      </Box>
      <Box type="row" flexDirection="row-reverse" m={6}>
        <Box
          style={{
            backgroundColor: "white",
            border: "2px solid rgb(226, 232, 240)",
            padding: "8px",
            borderRadius: "10px",
            width: "fit-content",
          }}
        >
          <Menu>
            <MenuButton style={{ color: "#6E798C" }}>
              {baseURL[app]?.selected || "Server"}
            </MenuButton>
            <MenuList>
              {baseURL[app]?.options?.map((value) => {
                return (
                  <MenuItem onClick={() => urlChangeHandler(value)}>
                    <Para>{value}</Para>
                  </MenuItem>
                );
              })}
            </MenuList>
          </Menu>
        </Box>
      </Box>
      <Box
        display="grid"
        gridTemplateColumns={["1fr", null, "1fr 1fr 1fr"]}
        gridGap={[4, 6]}
        my={[2, 0, 0]}
        p={" 0 2.5rem 1.5rem 2.5rem"}
      >
        <Box boxShadow="invision" p={[6, 4, 3]} type="column">
          <Box type="row" flexDirection="row-reverse">
            <Box
              style={{
                borderRadius: "50px",
                boxShadow: "#382e6c 0px 2px 4px 1px",
                background: "#8071b3",
                height: "40px",
                width: "40px",
                padding: "3px",
              }}
            >
              <Icon
                as={BsTable}
                viewBox="0 0 200 200"
                w={6}
                h={6}
                color={"white"}
                p={"1px"}
                m={"5px"}
              />
            </Box>
          </Box>
          <Box type="column" flexDirection="column-reverse" pt={[2, 4, 4]}>
            <H6 fontWeight="500" my={0}>
              Tables
            </H6>
            <H3 color={"#6e798c"} mb={[4, 2, 0]}>
              {data?.number_of_tables || 0}
            </H3>
          </Box>
        </Box>
        <Box boxShadow="invision" p={[6, 4, 3]} type="column">
          <Box type="row" flexDirection="row-reverse">
            <Box
              style={{
                borderRadius: "50px",
                boxShadow: "#382e6c 0px 2px 4px 1px",
                background: "#8071b3",
                height: "40px",
                width: "40px",
                padding: "5px",
              }}
            >
              <Icon
                as={BsFillLockFill}
                viewBox="0 0 200 200"
                w={7}
                h={7}
                color={"white"}
                p={"1px"}
                m={"1px"}
              />
            </Box>
          </Box>
          <Box type="column" flexDirection="column-reverse" pt={[2, 4, 4]}>
            <H6 fontWeight="500" my={0}>
              Relations
            </H6>
            <H3 color={"#6e798c"} mb={[4, 2, 0]}>
              {data?.relationships?.length || 0}
            </H3>
          </Box>
        </Box>
        <Box boxShadow="invision" p={[6, 4, 3]} type="column">
          <Box type="row" flexDirection="row-reverse">
            <Box
              style={{
                borderRadius: "50px",
                boxShadow: "#382e6c 0px 2px 4px 1px",
                background: "#8071b3",
                height: "40px",
                width: "40px",
                padding: "5px",
              }}
            >
              <Icon
                as={IoRocketSharp}
                viewBox="0 0 200 200"
                w={7}
                h={7}
                color={"white"}
                p={"1px"}
                m={"1px"}
              />
            </Box>
          </Box>
          <Box type="column" flexDirection="column-reverse" pt={[2, 4, 4]}>
            <H6 fontWeight="500" my={0}>
              Deployed
            </H6>
            <H3 color={"#6e798c"} mb={[4, 2, 0]}>
              {data?.deployment_info?.total_no_exports || 0}
            </H3>
          </Box>
        </Box>
      </Box>
      <Box
        display="grid"
        gridTemplateColumns={["1fr", null, "1fr 1fr"]}
        gridGap={[4, 6]}
        my={[2, 0, 0]}
        p={"0rem 2.5rem"}
      >
        <Box type="column">
          <Box mb={[2, 2, 4]}>
            <H5 my={0} color="#6e798c">
              Statistics
            </H5>
          </Box>
          <Box type="column">
            <Box
              boxShadow="invision"
              p={[2, 4, 2]}
              type="column"
              mb={[0, 2, 4]}
            >
              <Box height={["240px"]} width={["316px"]} ml={11}>
                <DoughnutChart data={data} />
              </Box>
            </Box>
          </Box>
        </Box>
        <Box type="column">
          <Box mb={[2, 2, 4]}>
            <H5 my={0} color="#6e798c">
              App Info
            </H5>
          </Box>
          <Box boxShadow="invision" p={[6, 4, 3]} type="column">
            <Box
              type="row"
              style={{
                justifyContent: "flex-start",
                margin: "10px",
                width: "100%",
              }}
            >
              <H5 my={0} color="lightPurple">
                Type Of Application:{" "}
              </H5>
              <H5
                ml={2}
                style={{
                  color: "#6E798C",
                }}
              >
                {data?.type}
              </H5>
            </Box>
            <Box
              type="row"
              style={{
                justifyContent: "flex-start",
                margin: "10px",
                width: "100%",
              }}
            >
              <H5 my={0} color="lightPurple">
                Database Type:{" "}
              </H5>
              <H5
                ml={2}
                style={{
                  color: "#6E798C",
                }}
              >
                {data?.db_type}
              </H5>
            </Box>

            <Box
              type="row"
              style={{
                justifyContent: "flex-start",
                margin: "10px",
                width: "100%",
              }}
            >
              <H5 my={0} color="lightPurple">
                Exported At:{" "}
              </H5>
              <H5
                ml={2}
                style={{
                  color: "#6E798C",
                }}
              >
                {data?.deployment_info?.most_recent_deployment ||
                  "Not exported Yet!"}
              </H5>
            </Box>
            <Box
              type="row"
              style={{
                justifyContent: "flex-start",
                margin: "10px",
                width: "100%",
              }}
            >
              <H5 my={0} color="lightPurple">
                {" "}
                Deployed At:{" "}
              </H5>
              <H5
                ml={2}
                style={{
                  color: "#6E798C",
                }}
              >
                {data?.deployment_info?.most_recent_deployment ||
                  "Not deployed yet!"}
              </H5>
            </Box>
            <Box
              type="row"
              style={{
                justifyContent: "flex-start",
                margin: "10px",
                width: "100%",
              }}
            >
              <H5 my={0} color="lightPurple">
                {" "}
                Deployment Platform:{" "}
              </H5>
              <H5
                ml={2}
                style={{
                  color: "#6E798C",
                }}
              >
                {data?.deployment_info?.platform || "Not deployed yet!"}
              </H5>
            </Box>
          </Box>
        </Box>
      </Box>
      <Box type="column" p={"0.5rem 2.5rem"}>
        <Box mb={[2, 2, 4]}>
          <H5 my={0} color="#6e798c">
            {app} {"Relationships"}
          </H5>
        </Box>
        <Box type="column">
          <Box boxShadow="invision" p={[2, 4, 2]} type="column" mb={[0, 2, 4]}>
            {data?.relationships?.length ? (
              <Box
                display="grid"
                gridTemplateColumns={["1fr", "1fr 1fr"]}
                // mb={8}
                gridGap={4}
                style={{}}
              >
                {relation}
              </Box>
            ) : (
              <Para>
                {" "}
                Relationships have not defined between any tables yet!
              </Para>
            )}
          </Box>
        </Box>
      </Box>
    </>
  );
};

export default AppHome;
