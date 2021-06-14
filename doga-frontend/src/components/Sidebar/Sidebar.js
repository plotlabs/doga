import React from "react";
import { useGlobal } from "reactn";
import { Icon } from "@chakra-ui/react";
import { FaDatabase } from "react-icons/fa";
import { IoAppsSharp } from "react-icons/io5";
import { AiFillHome } from "react-icons/ai";
import { NavLink } from "react-router-dom";
import { SiAmazonaws, SiHeroku } from "react-icons/si";
import { useLocation } from "react-router-dom";
import { BsTable } from "react-icons/bs";
import { MdEmail, MdTextsms } from "react-icons/md";
import { AiOutlineCaretDown, AiOutlineCaretUp } from "react-icons/ai";
import { SiMinutemailer } from "react-icons/si";
import { IoRocketSharp } from "react-icons/io5";
import { Box, Image, MotionBox, Para } from "../../styles";
import { useQuery } from "react-query";
import { APIURLS } from "../../Api";
import ClipLoader from "react-spinners/ClipLoader";
import Tabs from "./Tabs.js/Tabs";
import DropableTabs from "./Tabs.js/DropableTabs";

function Sidebar(props) {
  const [token] = useGlobal("token");
  const [dropMenu, setDropMenu] = React.useState([]);
  const [deployMenu, setDeployMenu] = React.useState(false);
  const [pluginsMenu, setPluginsMenu] = React.useState(false);
  let contentTypeApps = null;
  const location = useLocation();

  const { data, isLoading } = useQuery([APIURLS.getContentType], {
    enabled: !!token,
  });

  const dropMenuHandler = (appName) => {
    let newDropMenuArray = [...dropMenu];
    newDropMenuArray.push(appName);
    setDropMenu(newDropMenuArray);
  };

  const RemovedropMenuHandler = (appName) => {
    const newDropMenuArray = dropMenu.filter((index) => index != appName);
    setDropMenu(newDropMenuArray);
  };

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

    contentTypeApps = Object.entries(formElementsArray).map(
      ([index, value]) => {
        return (
          <React.Fragment key={`${value.app_name}-${index}`}>
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
                      color={"#ffffff"}
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
                      color={"#ffffff"}
                      onClick={() => dropMenuHandler(index)}
                    />
                  )}
                </i>
              </Box>
            </Box>
            {Object.entries(value.tables).map(([prop, val]) => {
              if (prop === "jwt_info") return true;
              return dropMenu.includes(index) ? (
                <NavLink
                  to={`/application/${value.app_name}/${prop}`}
                  key={`${prop}-table`}
                >
                  <MotionBox
                    transition={{ ease: "easeOut", duration: 0.3 }}
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
                        {prop}
                      </Para>
                    </Box>
                  </MotionBox>
                </NavLink>
              ) : null;
            })}
          </React.Fragment>
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
              }}
            >
              {localStorage.getItem("userName")}
            </Para>
            <Para
              style={{
                fontWeight: "400",
                lineHeight: "normal",
                color: "#gray",
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
          }}
          justifyContent="start"
        >
          <Para
            style={{
              fontWeight: "500",
              lineHeight: "none",
              color: "#6E798C",
            }}
          >
            Menu
          </Para>
        </Box>
        <Tabs
          name={"Dashboard"}
          page={"/dashboard"}
          icon={AiFillHome}
          location={location.pathname}
          subTab={false}
        />
        <Tabs
          name={"Database"}
          page={"/database"}
          icon={FaDatabase}
          location={location.pathname}
          subTab={false}
        />
        <DropableTabs
          name={"Deploy"}
          page={"/deploy"}
          setValue={setDeployMenu}
          value={deployMenu}
          icon={IoRocketSharp}
          location={location.pathname}
        />
        {deployMenu ? (
          <MotionBox
            transition={{ ease: "easeOut", duration: 0.3 }}
            initial={{ y: -50, opacity: 0 }}
            animate={{
              y: 0,
              opacity: 1,
            }}
          >
            <Tabs
              name={"AWS"}
              page={"/deploy/aws"}
              icon={SiAmazonaws}
              location={location.pathname}
              subTab={true}
            />
            <Tabs
              name={"Heroku"}
              page={"/deploy/heroku"}
              icon={SiHeroku}
              location={location.pathname}
              subTab={true}
            />
          </MotionBox>
        ) : null}
        <DropableTabs
          name={"Plugins"}
          page={"/notify"}
          setValue={setPluginsMenu}
          value={pluginsMenu}
          icon={SiMinutemailer}
          location={location.pathname}
        />

        {pluginsMenu ? (
          <MotionBox
            transition={{ ease: "easeOut", duration: 0.3 }}
            initial={{ y: -50, opacity: 0 }}
            animate={{
              y: 0,
              opacity: 1,
            }}
          >
            <Tabs
              name={"Sendgrid"}
              page={"/plugin/sendgrid"}
              icon={MdEmail}
              location={location.pathname}
              subTab={true}
            />
            <Tabs
              name={"Twilio"}
              page={"/plugin/Twilio"}
              icon={MdTextsms}
              location={location.pathname}
              subTab={true}
            />
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
              color: "#6E798C",
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

export default Sidebar;
