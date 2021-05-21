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
import { useGlobal } from "reactn";
import {
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
} from "@chakra-ui/react";
import { Avatar, AvatarBadge, AvatarGroup } from "@chakra-ui/react";
import { Tooltip } from "@chakra-ui/react";
import { Redirect } from "react-router-dom";
import { Icon } from "@chakra-ui/react";
import { FaEdit } from "react-icons/fa";
import { AiOutlineDelete } from "react-icons/ai";
import { AiOutlineCaretDown, AiOutlineCaretUp } from "react-icons/ai";
import { useParams } from "react-router";
import Api, { ApiJwt, APIURLS, setDefaultBaseUrl } from "../../Api";
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
import ImageView from "../../components/Modal/ImageView";

const Content = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [baseURL, setBaseURL] = useGlobal("baseURL");

  const [toggle, setToggle] = useState(true);
  const [loading, setLoading] = useState(false);
  const [editDataId, setEditDataId] = useState();
  const [deleteTableToggle, setDeleteTableToggle] = useState(false);
  const [openModal, setOpenModal] = useState();
  const [richText, setRichText] = useState();
  const [imageView, setImageView] = useState();
  const [relationDropView, setRelationDropView] = useState([]);
  let { app, table } = useParams();
  const queryClient = useQueryClient();
  const toast = createStandaloneToast();

  useEffect(() => {
    !baseURL[app] &&
      setBaseURL({
        ...baseURL,
        [app]: {
          options: ["http://0.0.0.0:8080/"],
          selected: "http://0.0.0.0:8080/",
        },
      });
  }, [app]);

  setDefaultBaseUrl(baseURL[app]?.selected || "http://0.0.0.0:8080/");
  useEffect(() => {
    console.log("baseURL[app]?.", baseURL[app]?.selected);
    baseURL[app]
      ? setDefaultBaseUrl(baseURL[app]?.selected)
      : setDefaultBaseUrl("http://0.0.0.0:8080/");
  }, [app, baseURL]);
  console.log(baseURL);
  const { data, isLoading } = useQuery(APIURLS.getContentType);
  const isFetchingApps = useIsFetching([APIURLS.getContentType]);
  let contentTypeApps = null;
  let richTextFields = [];
  let imageColumnFields = [];
  let tableFieldShow = null;
  let sendGetTableContent = null;
  if (data != null && data[app]["jwt_info"]) {
    sendGetTableContent = [APIURLS.getTableContent({ app, table }), "jwt_info"];
  } else {
    sendGetTableContent = [APIURLS.getTableContent({ app, table }), "baseURL"];
  }
  useEffect(() => {
    setRelationDropView([]);
  }, [table, app]);

  const fieldData = useQuery(sendGetTableContent);
  let fieldDataBodyArray = [];

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

  if (data != null && data[app][table]) {
    contentTypeApps = Object.entries(data[app][table]).map(([prop, val]) => {
      if (val.type === "VARCHAR(123)") {
        richTextFields.push(val.name);
      }
      if (val.type === "ImageType") {
        imageColumnFields.push(val.name);
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
    } catch ({ response }) {
      toast({
        title: "An error occurred.",
        description: response?.data?.result,
        status: "error",
        duration: 9000,
        isClosable: true,
      });

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

      setLoading(false);
    }
  }

  let fieldDataBody = null;
  if (fieldData?.data?.result) {
    fieldDataBody = Object.entries(fieldData?.data?.result).map(
      ([index, val]) => {
        return (
          <>
            <Tr style={{ color: "#4A5568" }}>
              <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                {val["id"]}
              </Td>
              {Object.entries(fieldDataBodyArray).map(([prop, value]) => {
                return richTextFields.includes(value) ? (
                  <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                    <Button onClick={() => richTextViewHandler(val[value])}>
                      View
                    </Button>
                  </Td>
                ) : imageColumnFields.includes(value) ? (
                  <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                    <Box>
                      {" "}
                      <Avatar
                        size="lg"
                        name="Doga"
                        borderRadius="50px"
                        onClick={() => imageViewHandler(val[value])}
                        src={`data:image/png;base64, ${val[value]}`}
                        cursor="pointer"
                      />
                    </Box>
                  </Td>
                ) : (
                  <Td
                    style={{
                      color: "#4A5568",
                      borderColor: "#EDF2F7",
                      textAlign: "center",
                    }}
                  >
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
                    {relationDropView.includes(parseInt(index))
                      ? val["related_content"] && (
                          <Tooltip
                            label="Collapse relationship view"
                            bg="#8071b399"
                            placement="top"
                          >
                            <spam>
                              <Icon
                                as={AiOutlineCaretUp}
                                w={5}
                                h={5}
                                cursor={"pointer"}
                                color={"#4B0082"}
                                onClick={() => accIndexHandler(index)}
                              ></Icon>
                            </spam>
                          </Tooltip>
                        )
                      : val["related_content"] && (
                          <Tooltip
                            label="View Relationship"
                            placement="top"
                            bg="#8071b399"
                          >
                            <spam>
                              <Icon
                                as={AiOutlineCaretDown}
                                w={5}
                                h={5}
                                cursor={"pointer"}
                                color={"#4B0082"}
                                onClick={() =>
                                  setRelationDropView([
                                    ...relationDropView,
                                    parseInt(index),
                                  ])
                                }
                              />
                            </spam>
                          </Tooltip>
                        )}

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
                    <Tooltip
                      label="Delete Field"
                      placement="top"
                      bg="#8071b399"
                    >
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

              {/* <AccordionPanel>yeahhhh</AccordionPanel> */}
            </Tr>
            {/* <> */}
            <tr>
              <td colspan="100">
                <AccordionItem style={{}}>
                  {" "}
                  <AccordionButton> </AccordionButton>
                  <AccordionPanel
                    pb={4}
                    style={{ backgroundColor: "#f7f8fb", width: "100%" }}
                  >
                    <Box width="100%">
                      <>
                        {val["related_content"] &&
                          Object.entries(val["related_content"]).map(
                            ([i, v]) => {
                              return (
                                <>
                                  <Box>
                                    <H5 fontSize="1.1rem" m={2}>
                                      {"Relationship with "}
                                      {v["realted_table"]} (
                                      {v["relation_name"][0].toLowerCase()}
                                      {"-"}
                                      {v["relation_name"][1].toLowerCase()}
                                      {"-"}
                                      {v["relation_name"][2].toLowerCase()})
                                    </H5>
                                  </Box>
                                  <Box type="column">
                                    {val["related_content"] &&
                                      Object.entries(v["realted_values"]).map(
                                        ([i, values]) => {
                                          return (
                                            <>
                                              <Box
                                                style={{
                                                  borderBottom:
                                                    "2px solid rgb(226 232 240)",
                                                }}
                                                m={4}
                                                mt={0}
                                              >
                                                {Object.entries(values).map(
                                                  ([key, value]) => {
                                                    return (
                                                      <>
                                                        <Para>
                                                          {key} : {value}
                                                        </Para>
                                                      </>
                                                    );
                                                  }
                                                )}
                                              </Box>
                                            </>
                                          );
                                        }
                                      )}
                                  </Box>
                                </>
                              );
                            }
                          )}
                      </>
                    </Box>
                  </AccordionPanel>
                </AccordionItem>
              </td>
            </tr>
            {/* </> */}
            {/* <Tr style={{ position: "relative" }}>
              <Td
                style={{
                  position: "absolute",
                  top: "0",
                  bottom: "0",
                  width: "100%",
                }}
              >
               
              </Td>
            </Tr> */}
          </>
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
  const imageViewHandler = (value) => {
    setOpenModal(7);
    onOpen();
    setImageView(value);
  };

  const accIndexHandler = (index) => {
    let array = [];
    array = relationDropView.filter((num) => num != index);
    setRelationDropView(array);
  };
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
      ) : openModal === 7 && imageView ? (
        <ImageView
          isOpen={isOpen}
          onOpen={onOpen}
          onClose={onClose}
          imageView={imageView}
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
          <Accordion index={[...relationDropView]}>
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
                  <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                    Id
                  </Th>
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
          </Accordion>
        </Box>
      )}
    </>
  );
};

export default Content;
