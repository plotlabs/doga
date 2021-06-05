import React from "react";
import { APIURLS } from "../../Api";
import { useQuery } from "react-query";
import { Box, Button, Span, H5, Para } from "../../styles";
import {
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
} from "@chakra-ui/react";
import ClipLoader from "react-spinners/ClipLoader";
import { useParams } from "react-router";

const AppDocs = () => {
  let { app } = useParams();
  const { data, isLoading } = useQuery(APIURLS.appDocs(app));

  return isLoading ? (
    <Box type="loader">
      <ClipLoader color={"#ffffff"} size={55} />
    </Box>
  ) : (
    <>
      <Box type="heading" textAlign="center">
        <Span type="heading">App Docs </Span>
      </Box>
      <Accordion allowToggle style={{ padding: "20px" }}>
        {data.app_type == "JWT Authenticated" ? (
          <>
            {data?.base_table.map((key) => {
              return (
                <>
                  <Para fontSize={"1.2rem"} m={3}>
                    {key?.name}
                  </Para>
                  {key?.end_points.map((api) => {
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

        {data?.unrestricted_tables[0].map((key) => {
          return (
            <>
              <Para fontSize={"1.2rem"} m={3}>
                {key?.table_name}
              </Para>
              {key?.end_points.map((api) => {
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
            {data?.locked_tables[0].map((key) => {
              return (
                <>
                  <Para fontSize={"1.2rem"} m={3} ml={4}>
                    {key?.table_name}
                  </Para>
                  {key?.end_points.map((api) => {
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
