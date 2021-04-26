import React, { useEffect } from "react";
import { useGlobal } from "reactn";

import { Icon } from "@chakra-ui/react";
import { FaUserAlt, FaServer, FaDatabase } from "react-icons/fa";
import { IoAppsSharp } from "react-icons/io5";
import { AiFillHome, AiFillCaretDown } from "react-icons/ai";
import { GrMysql } from "react-icons/gr";
import { SiPostgresql } from "react-icons/si";
import { NavLink } from "react-router-dom";
import { Wrap, WrapItem } from "@chakra-ui/react";
import { Avatar, AvatarBadge } from "@chakra-ui/react";
import { SiAmazonaws, SiHeroku } from "react-icons/si";
import { useLocation } from "react-router-dom";
import { BsAppIndicator, BsTable } from "react-icons/bs";
import { MdEmail, MdTextsms } from "react-icons/md";
import { AiOutlineCaretDown, AiOutlineCaretUp } from "react-icons/ai";
import { SiMinutemailer } from "react-icons/si";
import { IoRocketSharp } from "react-icons/io5";
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
import { useQuery, useQueryClient } from "react-query";
import { margin, marginTop } from "styled-system";
import Api, { APIURLS } from "../../Api";
import ClipLoader from "react-spinners/ClipLoader";

function PlacementExample(props) {
  const [token] = useGlobal("token");

  const [dropMenu, setDropMenu] = React.useState([]);
  const [deployMenu, setDeployMenu] = React.useState(false);
  const [pluginsMenu, setPluginsMenu] = React.useState(false);
  const [showDbOptions, setShowDbOptions] = React.useState(false);
  const location = useLocation();
  const { data, isLoading } = useQuery([APIURLS.getContentType], {
    enabled: !!token,
  });
  console.log(data);
  const showDbOptionsHandler = () => {
    setShowDbOptions(!showDbOptions);
  };
  const dropMenuHandler = (appName) => {
    let newDropMenuArray = [...dropMenu];
    newDropMenuArray.push(appName);
    setDropMenu(newDropMenuArray);
  };
  const RemovedropMenuHandler = (appName) => {
    const newDropMenuArray = dropMenu.filter((index) => index != appName);
    setDropMenu(newDropMenuArray);
  };
  console.log(dropMenu, "drop");
  let contentTypeApps = null;
  if (data) {
    const formElementsArray = [];
    if (data?.result === "No apps and content created yet.") {
    } else {
      for (let key in data) {
        formElementsArray.push({
          app_name: key,
          tables: data[key],
        });
      }
    }

    // console.log(formElementsArray);
    console.log("appssss");
    contentTypeApps = Object.entries(formElementsArray).map(
      ([index, value]) => {
        // console.log(prop, val);
        return (
          <>
            <Box
              type="row"
              justifyContent="space-between"
              style={{
                paddingLeft: "10px",
                height: "45px",
                margin: "5px",
                boxShadow:
                  location.pathname === `/application/${value.app_name}`
                    ? "rgb(10 10 10) 0px 2px 4px -1px"
                    : "rgb(0 0 0 / 7%) 0px 2px 4px 0px",
                background:
                  location.pathname === `/application/${value.app_name}`
                    ? "#80808045"
                    : "none",
                borderRadius:
                  location.pathname === `/application/${value.app_name}`
                    ? "10px"
                    : "0px",
              }}
            >
              <NavLink to={`/application/${value.app_name}`}>
                <Box type="row" justifyContent="start">
                  <i
                    style={{
                      marginRight: "5px",
                    }}
                  >
                    <Icon
                      as={IoAppsSharp}
                      w={5}
                      h={5}
                      mr={3}
                      mb={1}
                      color={
                        // location.pathname === `/application/${value.app_name}`
                        //   ? "#4B0082"
                        //   : "#6E798C"
                        "#ffffff"
                      }
                      // onClick={() => dropMenuHandler(index)}
                    />
                  </i>

                  <Para
                    style={{
                      fontWeight: "500",
                      lineHeight: "none",

                      whiteSpace: "nowrap",
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                    }}
                    // color={
                    //   location.pathname === `/application/${value.app_name}`
                    //     ? "#4B0082"
                    //     : "#6E798C"
                    // }
                    color={
                      // location.pathname === `/application/${value.app_name}`
                      //   ? "#4B0082"
                      //   : "#6E798C"
                      "#ffffff"
                    }
                  >
                    {value.app_name}
                  </Para>
                </Box>
              </NavLink>
              <Box>
                <i
                  style={{
                    marginRight: "5px",
                  }}
                >
                  {dropMenu.includes(index) ? (
                    <Icon
                      as={AiOutlineCaretUp}
                      w={3}
                      h={3}
                      mr={3}
                      mb={1}
                      style={{ cursor: "pointer" }}
                      // color={
                      //   location.pathname === `/application/${value.app_name}`
                      //     ? "#4B0082"
                      //     : "#6E798C"
                      // }
                      color={
                        // location.pathname === `/application/${value.app_name}`
                        //   ? "#4B0082"
                        //   : "#6E798C"
                        "#ffffff"
                      }
                      onClick={() => RemovedropMenuHandler(index)}
                    />
                  ) : (
                    <Icon
                      as={AiOutlineCaretDown}
                      w={3}
                      h={3}
                      mr={3}
                      mb={1}
                      style={{ cursor: "pointer" }}
                      // color={
                      //   location.pathname === `/application/${value.app_name}`
                      //     ? "#4B0082"
                      //     : "#6E798C"
                      // }
                      color={
                        // location.pathname === `/application/${value.app_name}`
                        //   ? "#4B0082"
                        //   : "#6E798C"
                        "#ffffff"
                      }
                      onClick={() => dropMenuHandler(index)}
                    />
                  )}
                </i>
              </Box>
            </Box>
            {Object.entries(value.tables).map(([prop, val]) => {
              if (prop === "jwt_info") return true;
              return dropMenu.includes(index) ? (
                <NavLink to={`/application/${value.app_name}/${prop}`}>
                  <MotionBox
                    transition={{ ease: "easeOut", duration: 0.3 }}
                    // whileHover={{
                    //   boxShadow: "0 4px 25px 0 rgba(0,0,0,.5)",
                    // }}
                    initial={{ y: -50, opacity: 0 }}
                    animate={{
                      y: 0,
                      opacity: 1,
                    }}
                  >
                    <Box
                      type="row"
                      style={{
                        paddingLeft: "30px",
                        height: "35px",
                        margin: "5px",
                        boxShadow:
                          location.pathname ===
                          `/application/${value.app_name}/${prop}`
                            ? "rgb(10 10 10) 0px 2px 4px -1px"
                            : "rgb(0 0 0 / 7%) 0px 2px 4px 0px",
                        background:
                          location.pathname ===
                          `/application/${value.app_name}/${prop}`
                            ? "#80808045"
                            : "none",
                        borderRadius:
                          location.pathname ===
                          `/application/${value.app_name}/${prop}`
                            ? "10px"
                            : "0px",
                      }}
                      justifyContent="start"
                    >
                      <i
                        style={{
                          marginRight: "5px",
                        }}
                      >
                        <Icon
                          as={BsTable}
                          w={4}
                          h={4}
                          mr={3}
                          mb={1}
                          // color={"#6E798C"}
                          color={
                            // location.pathname ===
                            // `/application/${value.app_name}/${prop}`
                            //   ? "#4B0082"
                            //   : "#6E798C"
                            "#ffffff"
                          }
                        />
                      </i>

                      <Para
                        style={{
                          fontWeight: "500",
                          lineHeight: "none",

                          whiteSpace: "nowrap",
                          overflow: "hidden",
                          textOverflow: "ellipsis",
                        }}
                        color={
                          // location.pathname ===
                          // `/application/${value.app_name}/${prop}`
                          //   ? "#4B0082"
                          //   : "#6E798C"
                          "#ffffff"
                        }
                      >
                        {prop}
                      </Para>
                    </Box>
                  </MotionBox>
                </NavLink>
              ) : null;
            })}
          </>
        );
      }
    );
  }

  return (
    <>
      {isLoading ? (
        <Box type="loader">
          <ClipLoader color={"#ffffff"} size={55} />
        </Box>
      ) : null}
      <Box
        type="column"
        style={{ overflowX: "scroll", backgroundColor: "#372e6c" }}
      >
        <Box
          display="grid"
          gridTemplateColumns={"1fr 3fr"}
          gridGap={"0px"}
          style={{
            paddingLeft: "5px",
            height: "60px",
            margin: "30px 15px 20px 0px",
          }}
        >
          <i
            style={{
              borderRadius: "50px",
              boxShadow: "rgb(10 10 10) 0px 2px 4px -1px",
              background: "#80808045",
              height: "50px",
            }}
          >
            <Image
              src="/maleLogo.png"
              style={{ height: "50px", padding: "5px" }}
            ></Image>
          </i>
          <Box type="column" ml={"5px"} pt={"10px"}>
            <Para
              style={{
                fontWeight: "700",
                lineHeight: "normal",
                color: "#ffffff",

                // location.pathname === "/dashboard" ? "#4B0082" : "#6E798C",
              }}
            >
              {localStorage.getItem("userName")}
            </Para>
            <Para
              style={{
                fontWeight: "400",
                lineHeight: "normal",
                color: "#gray",

                // location.pathname === "/dashboard" ? "#4B0082" : "#6E798C",
              }}
            >
              {localStorage.getItem("userEmail")}
            </Para>
          </Box>
        </Box>
        <Box
          type="row"
          style={{
            paddingLeft: "10px",
            marginLeft: "5px",
            // height: "45px",
            // margin: "5px",
          }}
          justifyContent="start"
        >
          <Para
            style={{
              fontWeight: "500",
              lineHeight: "none",
              color:
                // location.pathname === "/application" ? "#4B0082" : "#6E798C",
                "#6E798C",
            }}
          >
            Menu
          </Para>
        </Box>
        <NavLink to="/dashboard">
          {" "}
          <Box
            type="row"
            style={{
              paddingLeft: "10px",
              height: "45px",
              margin: "5px",
              boxShadow:
                location.pathname === "/dashboard"
                  ? "rgb(10 10 10) 0px 2px 4px -1px"
                  : "rgb(0 0 0 / 7%) 0px 2px 4px 0px",
              background:
                location.pathname === "/dashboard" ? "#80808045" : "none",
              borderRadius: location.pathname === "/dashboard" ? "10px" : "0px",
            }}
            justifyContent="start"
          >
            <i
              style={{
                minWidth: "14px",
                marginRight: "5px",
              }}
            >
              <Icon
                as={AiFillHome}
                w={5}
                h={5}
                mr={3}
                mb={1}
                color={"#ffffff"}
              />
            </i>

            <Para
              style={{
                fontWeight: "500",
                lineHeight: "none",
                color: "#ffffff",
              }}
            >
              Dashboard
            </Para>
          </Box>
        </NavLink>
        <NavLink to="/database">
          <Box
            type="row"
            style={{
              paddingLeft: "10px",
              height: "45px",
              margin: "5px",
              boxShadow:
                location.pathname === "/database"
                  ? "rgb(10 10 10) 0px 2px 4px -1px"
                  : "rgb(0 0 0 / 7%) 0px 2px 4px 0px",
              background:
                location.pathname === "/database" ? "#80808045" : "none",
              borderRadius: location.pathname === "/database" ? "10px" : "0px",
              // "&:hover": {
              //   boxShadow: "rgb(10 10 10) 0px 2px 4px -1px",
              //   background: "#80808045",
              //   borderRadius: "10px",
              // },
            }}
            justifyContent="start"
          >
            <i
              style={{
                minWidth: "14px",
                marginRight: "5px",
              }}
            >
              <Icon
                as={FaDatabase}
                w={5}
                h={5}
                mr={3}
                mb={1}
                color={
                  // location.pathname === "/database" ? "#4B0082" : "#6E798C"
                  "#ffffff"
                }
              />
            </i>

            <Para
              style={{
                fontWeight: "500",
                lineHeight: "none",
                // color:
                //   location.pathname === "/database" ? "#4B0082" : "#6E798C",
                color: "#ffffff",
              }}
            >
              Database
            </Para>
          </Box>
        </NavLink>

        <Box
          type="row"
          style={{
            paddingLeft: "10px",
            height: "45px",
            margin: "5px",
            boxShadow:
              location.pathname === "/deploy"
                ? "rgb(10 10 10) 0px 2px 4px -1px"
                : "rgb(0 0 0 / 7%) 0px 2px 4px 0px",
            background: location.pathname === "/deploy" ? "#80808045" : "none",
            borderRadius: location.pathname === "/deploy" ? "10px" : "0px",
          }}
          justifyContent="space-between"
          onClick={() => setDeployMenu(!deployMenu)}
        >
          <Box type="row">
            <i
              style={{
                minWidth: "14px",
                marginRight: "5px",
              }}
            >
              <Icon
                as={IoRocketSharp}
                w={5}
                h={5}
                mr={3}
                mb={1}
                color={
                  // location.pathname === "/deploy" ? "#4B0082" : "#6E798C"
                  "#ffffff"
                }
              />
            </i>

            <Para
              style={{
                fontWeight: "500",
                lineHeight: "none",
                // color:
                //   location.pathname === "/deploy" ? "#4B0082" : "#6E798C",
                color: "#ffffff",
              }}
            >
              Deploy
            </Para>
          </Box>

          <Box>
            <i
              style={{
                marginRight: "5px",
              }}
            >
              {deployMenu ? (
                <Icon
                  as={AiOutlineCaretUp}
                  w={3}
                  h={3}
                  mr={3}
                  mb={1}
                  color={"#ffffff"}
                  style={{ cursor: "pointer" }}
                  onClick={() => setDeployMenu(!deployMenu)}
                />
              ) : (
                <Icon
                  as={AiOutlineCaretDown}
                  w={3}
                  h={3}
                  mr={3}
                  mb={1}
                  color={"#ffffff"}
                  style={{ cursor: "pointer" }}
                  onClick={() => setDeployMenu(!deployMenu)}
                />
              )}
            </i>
          </Box>
        </Box>
        {deployMenu ? (
          <MotionBox
            transition={{ ease: "easeOut", duration: 0.3 }}
            // whileHover={{
            //   boxShadow: "0 4px 25px 0 rgba(0,0,0,.5)",
            // }}
            initial={{ y: -50, opacity: 0 }}
            animate={{
              y: 0,
              opacity: 1,
            }}
          >
            <NavLink to="/deploy/aws">
              <Box
                type="row"
                style={{
                  paddingLeft: "30px",
                  height: "35px",
                  margin: "5px",
                  boxShadow:
                    location.pathname === "/deploy/aws"
                      ? "rgb(10 10 10) 0px 2px 4px -1px"
                      : "rgb(0 0 0 / 7%) 0px 2px 4px 0px",
                  background:
                    location.pathname === "/deploy/aws" ? "#80808045" : "none",
                  borderRadius:
                    location.pathname === "/deploy/aws" ? "10px" : "0px",
                  cursor: "pointer",
                }}
                justifyContent="start"
              >
                <i
                  style={{
                    marginRight: "5px",
                  }}
                >
                  <Icon
                    as={SiAmazonaws}
                    w={5}
                    h={5}
                    mr={3}
                    mb={1}
                    // color={"#6E798C"}
                    color={"#ffffff"}
                  />
                </i>

                <Para
                  style={{
                    fontWeight: "500",
                    lineHeight: "none",

                    whiteSpace: "nowrap",
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                  }}
                  color={"#ffffff"}
                >
                  {"AWS"}
                </Para>
              </Box>
            </NavLink>
            <NavLink to="/deploy/heroku">
              <Box
                type="row"
                style={{
                  paddingLeft: "30px",
                  height: "35px",
                  margin: "5px",
                  boxShadow:
                    location.pathname === "/deploy/heroku"
                      ? "rgb(10 10 10) 0px 2px 4px -1px"
                      : "rgb(0 0 0 / 7%) 0px 2px 4px 0px",
                  background:
                    location.pathname === "/deploy/heroku"
                      ? "#80808045"
                      : "none",
                  borderRadius:
                    location.pathname === "/deploy/heroku" ? "10px" : "0px",
                }}
                justifyContent="start"
              >
                <i
                  style={{
                    marginRight: "5px",
                  }}
                >
                  <Icon
                    as={SiHeroku}
                    w={5}
                    h={5}
                    mr={3}
                    mb={1}
                    // color={"#6E798C"}
                    color={"#ffffff"}
                  />
                </i>

                <Para
                  style={{
                    fontWeight: "500",
                    lineHeight: "none",

                    whiteSpace: "nowrap",
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                  }}
                  color={"#ffffff"}
                >
                  {"Heroku"}
                </Para>
              </Box>
            </NavLink>
          </MotionBox>
        ) : null}

        <Box
          type="row"
          style={{
            paddingLeft: "10px",
            height: "45px",
            margin: "5px",
            boxShadow:
              location.pathname === "/notify"
                ? "rgb(10 10 10) 0px 2px 4px -1px"
                : "rgb(0 0 0 / 7%) 0px 2px 4px 0px",
            background: location.pathname === "/notify" ? "#80808045" : "none",
            borderRadius: location.pathname === "/notify" ? "10px" : "0px",
            cursor: "pointer",
          }}
          justifyContent="space-between"
          onClick={() => setPluginsMenu(!pluginsMenu)}
        >
          <Box type="row">
            <i
              style={{
                minWidth: "14px",
                marginRight: "5px",
              }}
            >
              <Icon
                as={SiMinutemailer}
                w={5}
                h={5}
                mr={3}
                mb={1}
                color={
                  // location.pathname === "/notify" ? "#4B0082" : "#6E798C"
                  "#ffffff"
                }
              />
            </i>

            <Para
              style={{
                fontWeight: "500",
                lineHeight: "none",
                // color:
                //   location.pathname === "/notify" ? "#4B0082" : "#6E798C",
                color: "#ffffff",
              }}
            >
              Plugins
            </Para>
          </Box>

          <Box>
            <i
              style={{
                marginRight: "5px",
              }}
            >
              {pluginsMenu ? (
                <Icon
                  as={AiOutlineCaretUp}
                  w={3}
                  h={3}
                  mr={3}
                  mb={1}
                  color={"#ffffff"}
                  style={{ cursor: "pointer" }}
                  onClick={() => setPluginsMenu(!pluginsMenu)}
                />
              ) : (
                <Icon
                  as={AiOutlineCaretDown}
                  w={3}
                  h={3}
                  mr={3}
                  mb={1}
                  color={"#ffffff"}
                  style={{ cursor: "pointer" }}
                  onClick={() => setPluginsMenu(!pluginsMenu)}
                />
              )}
            </i>
          </Box>
        </Box>
        {pluginsMenu ? (
          <MotionBox
            transition={{ ease: "easeOut", duration: 0.3 }}
            // whileHover={{
            //   boxShadow: "0 4px 25px 0 rgba(0,0,0,.5)",
            // }}
            initial={{ y: -50, opacity: 0 }}
            animate={{
              y: 0,
              opacity: 1,
            }}
          >
            <NavLink to="/plugin/sendgrid">
              <Box
                type="row"
                style={{
                  paddingLeft: "30px",
                  height: "35px",
                  margin: "5px",
                  boxShadow:
                    location.pathname === "/plugin/sendgrid"
                      ? "rgb(10 10 10) 0px 2px 4px -1px"
                      : "rgb(0 0 0 / 7%) 0px 2px 4px 0px",
                  background:
                    location.pathname === "/plugin/sendgrid"
                      ? "#80808045"
                      : "none",
                  borderRadius:
                    location.pathname === "/plugin/sendgrid" ? "10px" : "0px",
                }}
                justifyContent="start"
              >
                <i
                  style={{
                    marginRight: "5px",
                  }}
                >
                  <Icon
                    as={MdEmail}
                    w={5}
                    h={5}
                    mr={3}
                    mb={1}
                    // color={"#6E798C"}
                    color={"#ffffff"}
                  />
                </i>

                <Para
                  style={{
                    fontWeight: "500",
                    lineHeight: "none",

                    whiteSpace: "nowrap",
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                  }}
                  color={"#ffffff"}
                >
                  {"Sendgrid"}
                </Para>
              </Box>
            </NavLink>
            <NavLink to="/plugin/Twilio">
              <Box
                type="row"
                style={{
                  paddingLeft: "30px",
                  height: "35px",
                  margin: "5px",
                  boxShadow:
                    location.pathname === "/plugin/Twilio"
                      ? "rgb(10 10 10) 0px 2px 4px -1px"
                      : "rgb(0 0 0 / 7%) 0px 2px 4px 0px",
                  background:
                    location.pathname === "/plugin/Twilio"
                      ? "#80808045"
                      : "none",
                  borderRadius:
                    location.pathname === "/plugin/Twilio" ? "10px" : "0px",
                }}
                justifyContent="start"
              >
                <i
                  style={{
                    marginRight: "5px",
                  }}
                >
                  <Icon
                    as={MdTextsms}
                    w={5}
                    h={5}
                    mr={3}
                    mb={1}
                    // color={"#6E798C"}
                    color={"#ffffff"}
                  />
                </i>

                <Para
                  style={{
                    fontWeight: "500",
                    lineHeight: "none",

                    whiteSpace: "nowrap",
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                  }}
                  color={"#ffffff"}
                >
                  {"Twilio"}
                </Para>
              </Box>
            </NavLink>
          </MotionBox>
        ) : null}

        <Box
          type="row"
          style={{
            paddingLeft: "10px",
            marginLeft: "5px",
            marginTop: "15px",
            marginBottom: "5px",
          }}
          justifyContent="start"
        >
          <Para
            style={{
              fontWeight: "500",
              lineHeight: "none",
              color:
                // location.pathname === "/application" ? "#4B0082" : "#6E798C",
                "#6E798C",
            }}
          >
            Applications
          </Para>
        </Box>

        {contentTypeApps}
      </Box>
    </>
  );
}

export default PlacementExample;
