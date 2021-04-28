import React, { useState, useEffect } from "react";
import {
  Box,
  ResponsiveImage,
  Image,
  Button,
  StyledLink,
  Span,
  H1,
  H2,
  H5,
  MotionBox,
  Para,
} from "../../styles";
import { Tooltip } from "@chakra-ui/react";
import { Redirect } from "react-router-dom";
import { Icon } from "@chakra-ui/react";
import { FaEdit } from "react-icons/fa";
import { AiOutlineDelete } from "react-icons/ai";
import { useParams } from "react-router";
import Api, { ApiJwt, APIURLS } from "../../Api";
import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableCaption,
} from "@chakra-ui/react";
import { useQuery, useQueryClient } from "react-query";
import { useDisclosure } from "@chakra-ui/react";
import ContentField from "../../components/Modal/ContentField";
import AppTableCreation from "../../components/Modal/AppTableCreation";
import AppTableData from "../../components/Modal/AppTableData";
import BaseJwtLogin from "../../components/Modal/BaseJwtLogin";
import { useToast, createStandaloneToast } from "@chakra-ui/react";
import { useIsFetching } from "react-query";
import ClipLoader from "react-spinners/ClipLoader";
import RichTextView from "../../components/Modal/RichTextView";

const Content = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [toggle, setToggle] = useState(true);
  const [loading, setLoading] = useState(false);
  const [editDataId, setEditDataId] = useState();
  const [deleteTableToggle, setDeleteTableToggle] = useState(false);
  const [openModal, setOpenModal] = useState();
  const [richText, setRichText] = useState();
  let { app, table } = useParams();
  const queryClient = useQueryClient();
  const toast = createStandaloneToast();
  const { data, isLoading } = useQuery(APIURLS.getContentType);
  const isFetchingApps = useIsFetching([APIURLS.getContentType]);
  let contentTypeApps = null;
  let richTextFields = [];
  let tableFieldShow = null;
  let sendGetTableContent = null;
  if (data != null && data[app]["jwt_info"]) {
    console.log("Sendhing...", localStorage.getItem("jwtToken"));
    sendGetTableContent = [APIURLS.getTableContent({ app, table }), "jwt_info"];
  } else {
    sendGetTableContent = APIURLS.getTableContent({ app, table });
  }

  const fieldData = useQuery(sendGetTableContent);
  let fieldDataBodyArray = [];

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

  if (data != null && data[app][table]) {
    // const formElementsArray = [];
    // for (let key in data[id]) {
    //   formElementsArray.push({
    //     id: key,
    //     config: data[id][key],
    //   });
    // }
    // console.log(formElementsArray[0]);
    // let table = Object.entries(data[id]);
    contentTypeApps = Object.entries(data[app][table]).map(([prop, val]) => {
      console.log(prop, val);
      console.log("CHECK", val.type === "VARCHAR(123)");
      if (val.type === "VARCHAR(123)") {
        console.log(val.type, "inside");
        richTextFields.push(val.name);
        console.log(richTextFields);
      }
      return (
        <Tr style={{ color: "#4A5568" }}>
          <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
            {val.name}
          </Td>
          <Td
            style={{
              color: "#4A5568",
              borderColor: "#EDF2F7",
              textAlign: "center",
            }}
          >
            {val.type}
          </Td>
          <Td
            style={{
              color: "#4A5568",
              borderColor: "#EDF2F7",
              textAlign: "center",
            }}
          >
            {val.foreign_key}
          </Td>

          {/* <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
              {val.unique}
            </Td>
            <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
              {val.nullable}
            </Td>
            <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
              {val.default}
            </Td>
             */}
          <Td
            style={{
              color: "#4A5568",
              borderColor: "#EDF2F7",
              textAlign: "right",
            }}
          ></Td>
        </Tr>
      );
    });
    tableFieldShow = Object.entries(data[app][table]).map(([prop, val]) => {
      fieldDataBodyArray.push(val.name);
      return (
        <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>{val.name}</Th>
      );
    });
  }

  const editHandler = (id) => {
    setEditDataId(id);
    setOpenModal(1);

    onOpen();
  };

  async function deleteHandler(editDataId) {
    let deleteRow = null;
    setLoading(true);
    try {
      if (data != null && data[app]["jwt_info"]) {
        let { data } = await ApiJwt.delete(
          APIURLS.getTableContentById({ app, table, editDataId })
        );
      } else {
        let { data } = await Api.delete(
          APIURLS.getTableContentById({ app, table, editDataId })
        );
      }

      await queryClient.refetchQueries([
        APIURLS.getTableContent({ app, table }),
      ]);
      // setSuccess(true);

      toast({
        title: "Deleted.",
        description: data?.result,
        status: "success",
        duration: 9000,
        isClosable: false,
      });
      onClose();
      setLoading(false);
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
      setLoading(false);
    }
  }
  async function deleteTableHandler() {
    setLoading(true);
    try {
      let { data } = await Api.delete(APIURLS.deleteTable({ app, table }));
      await setTimeout(() => {
        queryClient.refetchQueries(APIURLS.getContentType);

        toast({
          title: "Deleted.",
          description: data?.result,
          status: "success",
          duration: 9000,
          isClosable: false,
        });

        setDeleteTableToggle(true);
        setLoading(false);
      }, 15000);
    } catch ({ response }) {
      toast({
        title: "An error occurred.",
        description: response?.data?.result,
        status: "error",
        duration: 9000,
        isClosable: true,
      });
      console.log(response);
      setLoading(false);
    }
  }

  let fieldDataBody = null;
  if (fieldData?.data?.result) {
    fieldDataBody = Object.entries(fieldData?.data?.result).map(
      ([prop, val]) => {
        return (
          <Tr style={{ color: "#4A5568" }}>
            <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
              {val["id"]}
            </Td>
            {Object.entries(fieldDataBodyArray).map(([prop, value]) => {
              console.log(prop, value, "here", val[value]);
              return richTextFields.includes(value) ? (
                <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                  <Button onClick={() => richTextViewHandler(val[value])}>
                    View
                  </Button>
                </Td>
              ) : (
                <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                  {val[value] === true
                    ? "true"
                    : val[value] === false
                    ? "false"
                    : val[value]}
                </Td>
              );
            })}

            <Td
              style={{
                color: "#4A5568",
                borderColor: "#EDF2F7",
                textAlign: "center",
              }}
            >
              {val["create_dt"]}
            </Td>
            <Td
              style={{
                color: "#4A5568",
                borderColor: "#EDF2F7",
                textAlign: "center",
              }}
            >
              {
                // <i onClick={() => {setEditDbConnection(key) &&onOpen }}>
                <i>
                  <Tooltip label="Edit Field" bg="#8071b399" placement="top">
                    <spam>
                      {" "}
                      <Icon
                        as={FaEdit}
                        w={5}
                        h={5}
                        cursor={"pointer"}
                        color={"#4B0082"}
                        onClick={() => editHandler(val["id"])}
                      ></Icon>
                    </spam>
                  </Tooltip>
                  <Tooltip label="Delete Field" placement="top" bg="#8071b399">
                    <spam>
                      <Icon
                        as={AiOutlineDelete}
                        w={5}
                        h={5}
                        cursor={"pointer"}
                        color={"red"}
                        onClick={() => deleteHandler(val["id"])}
                      />
                    </spam>
                  </Tooltip>
                </i>
              }
            </Td>
          </Tr>
        );
      }
    );
  }
  let captionButtonData = null;
  if (data) {
    captionButtonData = (
      <Box type="row">
        {data[app]["jwt_info"]?.base_table === table ? (
          <Button width={"100%"} mr={4} onClick={() => openModalHandler(5)}>
            Login
          </Button>
        ) : null}
        <Button width={"100%"} onClick={() => openModalHandler(1)}>
          Add Values to {data ? table : null}{" "}
        </Button>
      </Box>
    );
  }
  let captionButtonField = null;
  if (data) {
    captionButtonField = (
      <Button width={"100%"} onClick={() => openModalHandler(4)}>
        Add Fields to {data ? table : null}{" "}
      </Button>
    );
  }
  let CreateTable,
    exportTable = null;
  // if (data) {
  //   CreateTable = (
  //     <Button onClick={() => openModalHandler(3)} mr={6}>
  //       Create New Table
  //     </Button>
  //   );
  //   exportTable = (
  //     <Button onClick={() => exportAppHandler()}>Export App</Button>
  //   );
  // }
  let editTable = null;
  // if (data) {
  //   editTable = (
  //     <Button }>Create New Table</Button>
  //   );
  // }
  let modal = null;
  const openModalHandler = (key) => {
    setOpenModal(key);

    onOpen();
  };
  const richTextViewHandler = (value) => {
    setOpenModal(6);
    onOpen();
    setRichText(value);
  };

  // let modal = null;
  // if (data) {
  //   modal = (
  //
  //   );
  // }

  // let createTableModal = null;
  // if (data) {

  // }

  return loading || isLoading ? (
    <Box width="100%" height="100vh">
      <Box type={"loaderCentered"}>
        <ClipLoader color={"#ffffff"} size={55} />
      </Box>
    </Box>
  ) : (
    <>
      {deleteTableToggle ? <Redirect to="/dashboard" /> : null}
      {openModal === 3 ? (
        <AppTableCreation
          isOpen={isOpen}
          onOpen={onOpen}
          onClose={onClose}
          appName={app}
          basejwtPresent={
            data != null && data[app]["jwt_info"] && data[app]["jwt_info"]
              ? data[app]["jwt_info"]
              : null
          }

          // connectionSelected={data[id].connection_name}
          // columns={data[id].columns}
        />
      ) : openModal === 2 ? (
        <ContentField
          isOpen={isOpen}
          onOpen={onOpen}
          onClose={onClose}
          appName={app}
          tablename={table}
          columns={data[app][table]}
        />
      ) : openModal === 1 ? (
        <AppTableData
          isOpen={isOpen}
          onOpen={onOpen}
          onClose={onClose}
          app={app}
          table={table}
          columns={data[app][table]}
          basejwt={data[app]["jwt_info"] ? data[app]["jwt_info"] : null}
          editDataId={editDataId}
          restrictByJwt={
            data != null &&
            data[app]["jwt_info"] &&
            data[app]["jwt_info"]["restricted_tables"]
              ? data[app]["jwt_info"]["restricted_tables"].includes(table)
              : null
          }
        />
      ) : openModal === 4 ? (
        <AppTableCreation
          isOpen={isOpen}
          onOpen={onOpen}
          onClose={onClose}
          appName={app}
          columns={data[app][table]}
          tableNamePassed={table}
          edit={true}
        />
      ) : openModal === 5 ? (
        <BaseJwtLogin
          isOpen={isOpen}
          onOpen={onOpen}
          onClose={onClose}
          app={app}
          table={table}
          basejwt={data[app]["jwt_info"] ? data[app]["jwt_info"] : null}
        />
      ) : openModal === 6 ? (
        <RichTextView
          isOpen={isOpen}
          onOpen={onOpen}
          onClose={onClose}
          richText={richText}
        />
      ) : null}
      {/* <Box type="row" justifyContent="spacing-around" margin={6}>
        {data ? <H2>{table}</H2> : null}
        <Box type="row">
          {CreateTable}
          {exportTable}
        </Box>
      </Box> */}
      <Box type="heading" textAlign="center">
        <Span type="heading">{table}</Span>
      </Box>
      <Box type="row" justifyContent="center" mt={8}>
        <Button
          type="toggleTable"
          style={{
            width: "20vw",
            color: toggle ? "white" : "#392e6c",
            backgroundImage: toggle
              ? "linear-gradient(to right, rgb(56 46 108), rgb(56 46 108)"
              : "none",
          }}
          onClick={() => {
            setToggle(true);
          }}
        >
          Data
        </Button>
        <Button
          type="toggleTable"
          style={{
            width: "20vw",
            color: !toggle ? "white" : "#392e6c",
            backgroundImage: !toggle
              ? "linear-gradient(to right, rgb(56 46 108), rgb(56 46 108))"
              : "none",
          }}
          onClick={() => {
            setToggle(false);
          }}
        >
          Fields
        </Button>{" "}
      </Box>
      {!toggle ? (
        <Box
          type="tableView"
          //   m={6}
          style={{
            width: "80%",
            margin: "7rem",
            marginTop: "1.5rem",
          }}
        >
          <Table
            variant="striped"
            colorScheme="teal"
            style={{
              width: "98%",
            }}
          >
            <TableCaption>{captionButtonField}</TableCaption>
            <Thead>
              <Tr style={{ color: "#4A5568" }}>
                <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                  Fields
                </Th>
                <Th
                  style={{
                    color: "#4A5568",
                    borderColor: "#EDF2F7",
                    textAlign: "center",
                  }}
                >
                  Type
                </Th>
                <Th
                  style={{
                    color: "#4A5568",
                    borderColor: "#EDF2F7",
                    textAlign: "center",
                  }}
                >
                  Foreign Key
                </Th>
                <Th
                  style={{
                    color: "#4A5568",
                    borderColor: "#EDF2F7",
                    textAlign: "center",
                  }}
                >
                  {
                    // <i onClick={() => {setEditDbConnection(key) &&onOpen }}>
                    <i>
                      <Tooltip
                        label="Edit Table"
                        bg="#8071b399"
                        placement="top"
                      >
                        <spam>
                          <Icon
                            as={FaEdit}
                            w={5}
                            h={5}
                            cursor={"pointer"}
                            color={"#4B0082"}
                            onClick={() => openModalHandler(4)}
                          ></Icon>
                        </spam>
                      </Tooltip>
                      <Tooltip
                        label="Delete Table"
                        bg="#8071b399"
                        placement="top"
                      >
                        <spam>
                          <Icon
                            as={AiOutlineDelete}
                            w={5}
                            h={5}
                            cursor={"pointer"}
                            color={"red"}
                            onClick={() => deleteTableHandler()}
                          />
                        </spam>
                      </Tooltip>
                    </i>
                  }
                </Th>
                {/* <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>type</Th>
              <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                unique
              </Th>
              <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                nullable
              </Th>
              <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                default
              </Th>
              <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                Foreign Key
              </Th>

              <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}></Th> */}
              </Tr>
            </Thead>
            <Tbody>{contentTypeApps}</Tbody>
          </Table>
        </Box>
      ) : (
        <Box type="tableView" m={6}>
          {" "}
          <Table
            variant="striped"
            colorScheme="teal"
            style={{
              width: "98%",
            }}
          >
            <TableCaption>{captionButtonData}</TableCaption>
            <Thead>
              <Tr style={{ color: "#4A5568" }}>
                <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>Id</Th>
                {tableFieldShow}

                <Th
                  style={{
                    color: "#4A5568",
                    borderColor: "#EDF2F7",
                    textAlign: "center",
                  }}
                >
                  Created_at
                </Th>
              </Tr>
            </Thead>
            <Tbody>{fieldDataBody}</Tbody>
          </Table>
        </Box>
      )}
    </>
  );
};

export default Content;
