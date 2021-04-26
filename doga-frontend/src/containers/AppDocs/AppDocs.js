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
import {
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
} from "@chakra-ui/react";
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
const AppDocs = () => {
  let { app } = useParams();
  const queryClient = useQueryClient();
  const userProfile = useQuery(APIURLS.userInfo);
  const toast = createStandaloneToast();
  //   const appsCreated = useQuery(APIURLS.dashboardInfo(app, all));

  const { data, isLoading } = useQuery(APIURLS.appDocs(app));
  console.log(data?.locked_tables[0]);

  const isFetching = useIsFetching();

  return isLoading ? (
    <Box type="loader">
      <ClipLoader color={"#ffffff"} size={55} />
    </Box>
  ) : (
    <>
      <Box type="heading" textAlign="center">
        <Span type="heading">App Docs </Span>
      </Box>
      {/* <H5 type="heading" style={{ padding: "20px", marginTop: "5px" }}>
        Unrestricted Tables
      </H5> */}
      <Accordion allowToggle style={{ padding: "20px" }}>
        {data.app_type == "JWT Authenticated" ? (
          <>
            {/* <H5 type="heading" style={{ padding: "20px", marginTop: "5px" }}>
              Base Table
            </H5> */}

            {data?.base_table.map((key) => {
              console.log(key.end_points);
              return (
                <>
                  <Para fontSize={"1.2rem"} m={3}>
                    {key?.name}
                  </Para>
                  {key?.end_points.map((api) => {
                    console.log("aoi", api.request_body);
                    return (
                      <AccordionItem>
                        <h2>
                          <AccordionButton>
                            <Box type="row" justifyContent="start" width="100%">
                              {" "}
                              <Button
                                type="primary"
                                backgroundColor={
                                  api.request_type === "GET"
                                    ? "#7bbef3"
                                    : api.request_type === "POST"
                                    ? "#48a58d"
                                    : api.request_type === "PUT"
                                    ? "#da9a5a"
                                    : api.request_type === "DELETE"
                                    ? "#c36666"
                                    : null
                                }
                              >
                                {api.request_type}
                              </Button>
                              <Para ml={4} color={"#2a3950"}>
                                {api.end_point}
                              </Para>
                            </Box>

                            <AccordionIcon />
                          </AccordionButton>
                        </h2>
                        <AccordionPanel
                          pb={4}
                          style={{ backgroundColor: "#f7f8fb" }}
                        >
                          <Box mb={2}>
                            <H5 fontSize="1.1rem">{"Request Body"}</H5>
                          </Box>
                          <Box type="column">
                            {key.request_body}
                            {api?.request_body?.map((body) => {
                              return (
                                <>
                                  <Box
                                    style={{
                                      borderBottom:
                                        "2px solid rgb(226 232 240)",
                                    }}
                                  >
                                    {" "}
                                    <Para>Name: {body.prop_name}</Para>
                                    <Para>Type: {body.prop_type}</Para>
                                    <Para>
                                      default: {body.prop_default || "null"}
                                    </Para>
                                  </Box>
                                </>
                              );
                            })}
                          </Box>
                          <Box mb={2} mt={5}>
                            <H5 fontSize="1.1rem">{"Response Body"}</H5>
                          </Box>
                          <Box
                            type="row"
                            justifyContent="start"
                            style={{ borderBottom: "2px solid #8071b399" }}
                          >
                            {" "}
                            <Para>Code</Para>
                            <Para ml={10}>Description</Para>
                          </Box>
                          <Box type="column">
                            {" "}
                            {api?.response_body?.map((res) => {
                              return (
                                <>
                                  <Box type="row" justifyContent="start">
                                    <Para>{res.code}</Para>
                                    {res.code == 200 &&
                                    api.request_type == "DELETE" ? (
                                      <Para ml={11}>{res.body}</Para>
                                    ) : res.code == 200 &&
                                      api.request_type != "DELETE" ? (
                                      <Box type="coumn">
                                        <Box ml={11}>
                                          <Para>
                                            {" "}
                                            Result: {res.body.result}
                                          </Para>
                                          <Para>id: {res.body.id}</Para>
                                          <Para>
                                            access_token:{" "}
                                            {res.body.access_token}
                                          </Para>
                                          <Para>
                                            refresh_token:{" "}
                                            {res.body.refresh_token}
                                          </Para>
                                        </Box>
                                      </Box>
                                    ) : res.code === 400 ? (
                                      <Para ml={11}> Error </Para>
                                    ) : res.code === 500 ? (
                                      <Para ml={11}> Server Error </Para>
                                    ) : null}
                                  </Box>
                                </>
                              );
                            })}
                          </Box>
                        </AccordionPanel>
                      </AccordionItem>
                    );
                  })}
                </>
              );
            })}
          </>
        ) : null}
        {/* <H5 type="heading" style={{ padding: "20px", marginTop: "5px" }}>
          Unrestricted Tables
        </H5> */}

        {data?.unrestricted_tables[0].map((key) => {
          return (
            <>
              <Para fontSize={"1.2rem"} m={3}>
                {key?.table_name}
              </Para>
              {key?.end_points.map((api) => {
                console.log("aoi", api);
                return (
                  <AccordionItem>
                    <h2>
                      <AccordionButton>
                        <Box type="row" justifyContent="start" width="100%">
                          {" "}
                          <Button
                            type="primary"
                            backgroundColor={
                              api.request_type === "GET"
                                ? "#7bbef3"
                                : api.request_type === "POST"
                                ? "#48a58d"
                                : api.request_type === "PUT"
                                ? "#da9a5a"
                                : api.request_type === "DELETE"
                                ? "#c36666"
                                : null
                            }
                          >
                            {api.request_type}
                          </Button>
                          <Para ml={4} color={"#2a3950"}>
                            {api.end_point}
                          </Para>
                        </Box>

                        <AccordionIcon />
                      </AccordionButton>
                    </h2>
                    <AccordionPanel
                      pb={4}
                      style={{ backgroundColor: "#f7f8fb" }}
                    >
                      <Box mb={2}>
                        <H5 fontSize="1.1rem">{"Request Body"}</H5>
                      </Box>
                      <Box type="column">
                        {" "}
                        {api.request_body.map((body) => {
                          return (
                            <>
                              <Box
                                style={{
                                  borderBottom: "2px solid rgb(226 232 240)",
                                }}
                              >
                                {" "}
                                <Para>Name: {body.prop_name}</Para>
                                <Para>Type: {body.prop_type}</Para>
                                <Para>
                                  default: {body.prop_default || "null"}
                                </Para>
                              </Box>
                            </>
                          );
                        })}
                      </Box>
                      <Box mb={2} mt={5}>
                        <H5 fontSize="1.1rem">{"Response Body"}</H5>
                      </Box>
                      <Box
                        type="row"
                        justifyContent="start"
                        style={{ borderBottom: "2px solid #8071b399" }}
                      >
                        {" "}
                        <Para>Code</Para>
                        <Para ml={10}>Description</Para>
                      </Box>
                      <Box type="column">
                        {" "}
                        {api.response_body.map((res) => {
                          return (
                            <>
                              <Box type="row" justifyContent="start">
                                <Para>{res.code}</Para>
                                {res.code == 200 &&
                                api.request_type == "DELETE" ? (
                                  <Para ml={11}>{res.body}</Para>
                                ) : res.code == 200 &&
                                  api.request_type != "DELETE" ? (
                                  <Box type="coumn">
                                    {res?.body?.map((body) => {
                                      return (
                                        <>
                                          <Box ml={11}>
                                            <Para>Name: {body.prop_name}</Para>
                                            <Para>Type: {body.prop_type}</Para>
                                            <Para>
                                              default:{" "}
                                              {body.prop_default || "null"}
                                            </Para>
                                          </Box>
                                        </>
                                      );
                                    })}
                                  </Box>
                                ) : res.code === 400 ? (
                                  <Para ml={11}> Error </Para>
                                ) : res.code === 500 ? (
                                  <Para ml={11}> Server Error </Para>
                                ) : null}
                              </Box>
                            </>
                          );
                        })}
                      </Box>
                    </AccordionPanel>
                  </AccordionItem>
                );
              })}
            </>
          );
        })}
        {data.app_type == "JWT Authenticated" ? (
          <>
            {" "}
            {/* <H5 type="heading" style={{ padding: "20px", marginTop: "5px" }}>
              Locked Tables
            </H5> */}
            {data?.locked_tables[0].map((key) => {
              return (
                <>
                  <Para fontSize={"1.2rem"} m={3} ml={4}>
                    {key?.table_name}
                  </Para>
                  {key?.end_points.map((api) => {
                    console.log("aoi", api);
                    return (
                      <AccordionItem>
                        <h2>
                          <AccordionButton>
                            <Box type="row" justifyContent="start" width="100%">
                              {" "}
                              <Button
                                type="primary"
                                backgroundColor={
                                  api.request_type === "GET"
                                    ? "#7bbef3"
                                    : api.request_type === "POST"
                                    ? "#48a58d"
                                    : api.request_type === "PUT"
                                    ? "#da9a5a"
                                    : api.request_type === "DELETE"
                                    ? "#c36666"
                                    : null
                                }
                              >
                                {api.request_type}
                              </Button>
                              <Para ml={4} color={"#2a3950"}>
                                {api.end_point}
                              </Para>
                            </Box>

                            <AccordionIcon />
                          </AccordionButton>
                        </h2>
                        <AccordionPanel
                          pb={4}
                          style={{ backgroundColor: "#f7f8fb" }}
                        >
                          <Box mb={2}>
                            <H5 fontSize="1.1rem">{"Request Body"}</H5>
                          </Box>
                          <Box type="column">
                            {" "}
                            {api.request_body.map((body) => {
                              return (
                                <>
                                  <Box
                                    style={{
                                      borderBottom:
                                        "2px solid rgb(226 232 240)",
                                    }}
                                  >
                                    {" "}
                                    <Para>Name: {body.prop_name}</Para>
                                    <Para>Type: {body.prop_type}</Para>
                                    <Para>
                                      default: {body.prop_default || "null"}
                                    </Para>
                                  </Box>
                                </>
                              );
                            })}
                          </Box>
                          <Box mb={2} mt={5}>
                            <H5 fontSize="1.1rem">{"Response Body"}</H5>
                          </Box>
                          <Box
                            type="row"
                            justifyContent="start"
                            style={{ borderBottom: "2px solid #8071b399" }}
                          >
                            {" "}
                            <Para>Code</Para>
                            <Para ml={10}>Description</Para>
                          </Box>
                          <Box type="column">
                            {" "}
                            {api.response_body.map((res) => {
                              return (
                                <>
                                  <Box type="row" justifyContent="start">
                                    <Para>{res.code}</Para>
                                    {res.code == 200 &&
                                    api.request_type == "DELETE" ? (
                                      <Para ml={11}>{res.body}</Para>
                                    ) : res.code == 200 &&
                                      api.request_type != "DELETE" ? (
                                      <Box type="coumn">
                                        {res?.body?.map((body) => {
                                          return (
                                            <>
                                              <Box ml={11}>
                                                <Para>
                                                  Name: {body.prop_name}
                                                </Para>
                                                <Para>
                                                  Type: {body.prop_type}
                                                </Para>
                                                <Para>
                                                  default:{" "}
                                                  {body.prop_default || "null"}
                                                </Para>
                                              </Box>
                                            </>
                                          );
                                        })}
                                      </Box>
                                    ) : res.code === 400 ? (
                                      <Para ml={11}> Error </Para>
                                    ) : res.code === 500 ? (
                                      <Para ml={11}> Server Error </Para>
                                    ) : null}
                                  </Box>
                                </>
                              );
                            })}
                          </Box>
                        </AccordionPanel>
                      </AccordionItem>
                    );
                  })}
                </>
              );
            })}
          </>
        ) : null}
      </Accordion>
    </>
  );
};

export default AppDocs;
