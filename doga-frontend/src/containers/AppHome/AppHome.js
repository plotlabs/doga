import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { useGlobal } from "reactn";
import { NavLink } from "react-router-dom";
import Api, { setHeader, APIURLS } from "../../Api";
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
  H1,
  Input,
  Label,
  H5,
  Para,
} from "../../styles";
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
import { useIsFetching } from "react-query";
import ClipLoader from "react-spinners/ClipLoader";
import { Chart } from "chart.js";
import { Doughnut, Line } from "react-chartjs-2";
import { useParams } from "react-router";
import AppTableCreation from "../../components/Modal/AppTableCreation";
const AppHome = () => {
  let { app } = useParams();
  const queryClient = useQueryClient();
  const userProfile = useQuery(APIURLS.userInfo);
  const toast = createStandaloneToast();
  //   const appsCreated = useQuery(APIURLS.dashboardInfo(app, all));
  const { data, isLoading } = useQuery(APIURLS.appStats(app));
  const appDocs = useQuery(APIURLS.appDocs(app));
  console.log(appDocs?.data?.unrestricted_tables[0]);
  const appData = useQuery(APIURLS.getContentType);

  const dbConnections = useQuery(APIURLS.getDbConnections);
  const { isOpen, onOpen, onClose } = useDisclosure();

  const [openModal, setOpenModal] = useState();
  const openModalHandler = (key) => {
    setOpenModal(key);
    onOpen();
  };
  const isFetching = useIsFetching();
  let labels = [];
  let dataset = [];
  let totalFields = 0;
  for (let key in data?.tables) {
    labels.push(data?.tables[key].table_name);
    dataset.push(data?.tables[key].no_fields);
    totalFields += data?.tables[key].no_fields;
  }

  const dataDoughnut = {
    labels: ["Tables", "Relations", "Fields", "Exported"],
    datasets: [
      {
        data: [
          data?.number_of_tables,
          data?.relationships.length || 0,
          totalFields,
          data?.deployment_info?.total_no_exports,
        ],
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "purple"],
        hoverBackgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "purple"],
      },
    ],
    text: "23%",
  };
  //    dataLine = null;

  const dataLine = {
    labels: labels,
    datasets: [
      {
        label: "Number Of Fields Per Table",
        data: dataset,
        fill: true,
        backgroundColor: "rgba(75,192,192,0.2)",
        borderColor: "rgba(75,192,192,1)",
      },
      //   {
      //     label: "Fields dataset",
      //     data: [5, 7, 6, 10],
      //     fill: true,
      //     borderColor: "#742774",
      //   },
    ],
  };

  async function exportAppHandler() {
    console.log(app);
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
      // onClose();
      console.log("there", data);
    } catch ({ response }) {
      toast({
        title: "An error occurred.",
        description: response?.data?.result,
        status: "error",
        duration: 9000,
        isClosable: true,
      });
      console.log(response);
    }
  }

  let relation = null;
  //   console.log(data?.relationships);

  if (data != null && data.relationships) {
    relation = data?.relationships.map((key) => {
      console.log(key);
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
  return isLoading ? (
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

      <Box
        display="grid"
        gridTemplateColumns={["1fr 1fr", "1fr 1fr 1fr "]}
        // mb={8}
        gridGap={4}
        style={{
          margin: "30px",
          marginLeft: "70px",
          marginRight: "70px",
          marginBottom: "8px",
        }}
      >
        <MotionBox
          transition={{ ease: "easeOut", duration: 0.3 }}
          whileHover={{
            boxShadow: "0 4px 25px 0 rgba(0,0,0,.5)",
          }}
          initial={{ y: 50, opacity: 0 }}
          animate={{
            y: 0,
            opacity: 1,
          }}
          type="column"
          boxShadow="card"
          // bg={"#800080"}
          p={3}
          borderRadius="15px"
          alignItems="center"
          style={{
            cursor: "pointer",
            backgroundColor: "white",
            border: "2px solid rgb(110, 121, 140)",
          }}
          // onClick={onClick}
        >
          <Box
            display="grid"
            gridTemplateColumns={["1fr 2fr"]}
            m={"10px"}
            gridGap={"2.25rem"}
            style={{
              "&:hover": {
                opacity: ".2",
              },
            }}
          >
            <Box type="row" justifyContent="center">
              <Icon as={BsTable} w={"4rem"} h={"4rem"} color={"#4B0082"} />
            </Box>
            <Box
              style={{
                textAlign: "center",
              }}
            >
              <H5 fontSize={10} color={"#6E798C"} lineHeight={10}>
                {data?.number_of_tables}
              </H5>
              <Para
                fontSize={6}
                color={"#6E798C"}
                style={{ fontWeight: "600" }}
              >
                {"Tables"}
              </Para>
            </Box>
          </Box>
        </MotionBox>
        <MotionBox
          transition={{ ease: "easeOut", duration: 0.3 }}
          whileHover={{
            boxShadow: "0 4px 25px 0 rgba(0,0,0,.5)",
          }}
          initial={{ y: 50, opacity: 0 }}
          animate={{
            y: 0,
            opacity: 1,
          }}
          type="column"
          boxShadow="card"
          // bg={"#800080"}
          p={3}
          borderRadius="15px"
          alignItems="center"
          style={{
            cursor: "pointer",
            backgroundColor: "white",
            border: "2px solid rgb(110, 121, 140)",
          }}
          // onClick={onClick}
        >
          <Box
            display="grid"
            gridTemplateColumns={["1fr 2fr"]}
            m={"10px"}
            gridGap={"2.25rem"}
          >
            <Box type="row" justifyContent="center">
              <Icon
                as={BsFillLockFill}
                w={"4rem"}
                h={"4rem"}
                color={"#4B0082"}
              />
            </Box>
            <Box
              style={{
                textAlign: "center",
              }}
            >
              <H5 fontSize={10} color={"#6E798C"} lineHeight={10}>
                {data?.relationships.length || 0}
              </H5>
              <Para
                fontSize={6}
                color={"#6E798C"}
                style={{ fontWeight: "600" }}
              >
                {"Relations"}
              </Para>
            </Box>
          </Box>
        </MotionBox>
        <MotionBox
          transition={{ ease: "easeOut", duration: 0.3 }}
          whileHover={{
            boxShadow: "0 4px 25px 0 rgba(0,0,0,.5)",
          }}
          initial={{ y: 50, opacity: 0 }}
          animate={{
            y: 0,
            opacity: 1,
          }}
          type="column"
          boxShadow="card"
          // bg={"#800080"}
          p={3}
          borderRadius="15px"
          alignItems="center"
          style={{
            cursor: "pointer",
            backgroundColor: "white",
            border: "2px solid rgb(110, 121, 140)",
          }}
          // onClick={onClick}
        >
          <Box
            display="grid"
            gridTemplateColumns={["1fr 2fr"]}
            m={"10px"}
            gridGap={"2.25rem"}
          >
            <Box type="row" justifyContent="center">
              <Icon as={SiAmazonaws} w={"4rem"} h={"4rem"} color={"#4B0082"} />
            </Box>
            <Box
              style={{
                textAlign: "center",
              }}
            >
              <H5 fontSize={10} color={"#6E798C"} lineHeight={10}>
                {data?.deployment_info?.total_no_exports}
              </H5>
              <Para
                fontSize={6}
                color={"#6E798C"}
                style={{ fontWeight: "600" }}
              >
                {"Deployed"}
              </Para>
            </Box>
          </Box>
        </MotionBox>
      </Box>

      <Box
        display="grid"
        gridTemplateColumns={["1fr", "1fr 1fr"]}
        // mb={8}
        gridGap={4}
        style={{
          margin: "30px",
          marginLeft: "70px",
          marginRight: "70px",
          marginTop: "20px",
        }}
      >
        <MotionBox
          transition={{ ease: "easeOut", duration: 0.3 }}
          whileHover={{
            boxShadow: "0 4px 25px 0 rgba(0,0,0,.5)",
          }}
          initial={{ y: 50, opacity: 0 }}
          animate={{
            y: 0,
            opacity: 1,
          }}
          type="column"
          boxShadow="card"
          p={3}
          borderRadius="15px"
          alignItems="center"
          style={{
            cursor: "pointer",
            backgroundColor: "white",
            border: "2px solid rgb(110, 121, 140)",
          }}
          mb={5}
        >
          <H2
            type="centerBorder"
            color={"#6E798C"}
            style={{
              width: "100%",
              textAlign: "left",
            }}
          >
            {" "}
            {app}
          </H2>

          <Box
            type="row"
            style={{
              justifyContent: "flex-start",
              margin: "10px",
              width: "100%",
            }}
          >
            <H5>Type Of Application: </H5>
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
            <H5>Database Type: </H5>
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
            <H5> Exported At: </H5>
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
            <H5> Deployed At: </H5>
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
            <H5> Deployment Platform: </H5>
            <H5
              ml={2}
              style={{
                color: "#6E798C",
              }}
            >
              {data?.deployment_info?.platform || "Not deployed yet!"}
            </H5>
          </Box>
        </MotionBox>

        <MotionBox
          transition={{ ease: "easeOut", duration: 0.3 }}
          whileHover={{
            boxShadow: "0 4px 25px 0 rgba(0,0,0,.5)",
          }}
          initial={{ y: 50, opacity: 0 }}
          animate={{
            y: 0,
            opacity: 1,
          }}
          type="column"
          boxShadow="card"
          p={3}
          borderRadius="15px"
          alignItems="center"
          style={{
            cursor: "pointer",
            backgroundColor: "white",
            border: "2px solid rgb(110, 121, 140)",
          }}
          mb={5}
        >
          <Doughnut data={dataDoughnut} />
          {/* <Box type="column">
            <Box style={{ marginTop: "65px" }}>
              {" "}
             
            </Box> */}
          {/* </Box> */}
        </MotionBox>
      </Box>
      <Box
        display="grid"
        gridTemplateColumns={["1fr", "1fr"]}
        // mb={8}
        gridGap={4}
        style={{
          margin: "30px",
          marginLeft: "70px",
          marginRight: "70px",
          marginTop: "20px",
        }}
      >
        <MotionBox
          transition={{ ease: "easeOut", duration: 0.3 }}
          whileHover={{
            boxShadow: "0 4px 25px 0 rgba(0,0,0,.5)",
          }}
          initial={{ y: 50, opacity: 0 }}
          animate={{
            y: 0,
            opacity: 1,
          }}
          type="column"
          boxShadow="card"
          // bg={"#800080"}
          p={3}
          borderRadius="15px"
          alignItems="center"
          style={{
            cursor: "pointer",
            backgroundColor: "white",
            border: "2px solid rgb(110, 121, 140)",
          }}
          // onClick={onClick}
        >
          <Line data={dataLine} height={80} />
        </MotionBox>
      </Box>

      <MotionBox
        transition={{ ease: "easeOut", duration: 0.3 }}
        whileHover={{
          boxShadow: "0 4px 25px 0 rgba(0,0,0,.5)",
        }}
        initial={{ y: 50, opacity: 0 }}
        animate={{
          y: 0,
          opacity: 1,
        }}
        type="column"
        boxShadow="card"
        p={3}
        borderRadius="15px"
        alignItems="center"
        style={{
          cursor: "pointer",
          backgroundColor: "white",
          border: "2px solid rgb(110, 121, 140)",
          margin: "30px",
          marginLeft: "70px",
          marginRight: "70px",
          marginTop: "20px",
        }}
        mb={5}
      >
        <H2
          type="centerBorder"
          color={"#6E798C"}
          style={{
            width: "100%",
            textAlign: "left",
          }}
        >
          {app} {"Relationships"}
        </H2>
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
          <Para> Relationships have not defined between any tables yet!</Para>
        )}
      </MotionBox>
      {/* <Box>
       
      </Box> */}
    </>
  );
};

export default AppHome;
