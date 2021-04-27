import React, { useEffect } from "react";
import { useGlobal } from "reactn";
import {
  NavLink,
  Link,
  useLocation,
  useParams,
  useRouteMatch,
} from "react-router-dom";
import {
  Box,
  ResponsiveImage,
  Image,
  Button,
  StyledLink,
  Span,
  H1,
  H2,
  Para,
  MotionBox,
  H5,
} from "../../styles";
import { useDisclosure } from "@chakra-ui/react";
import { FaUserAlt, FaBell } from "react-icons/fa";
import { AiFillHome, AiFillCaretDown } from "react-icons/ai";
import { Tooltip } from "@chakra-ui/react";
import Trigger from "rc-trigger";
import { Icon, ChevronDownIcon } from "@chakra-ui/react";
import AdminProfile from "./AdminProfile";
import Sidebar from "../Sidebar/Sidebar";
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
import { useQuery, useQueryClient } from "react-query";
import { useToast, createStandaloneToast } from "@chakra-ui/react";
import Api, { setHeader, APIURLS } from "../../Api";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbSeparator,
} from "@chakra-ui/react";

const Header = () => {
  const location = useLocation();
  let match = useRouteMatch();
  console.log(match);

  const [token, setToken] = useGlobal("token");
  const { isOpen, onOpen, onClose } = useDisclosure();
  const queryClient = useQueryClient();
  const toast = createStandaloneToast();

  const { data, loading } = useQuery(APIURLS.getNotifications, {
    enabled: !!token,
  });
  async function notificationRefreshHandler() {
    try {
      await queryClient.refetchQueries(APIURLS.getNotifications());
      console.log(data);
    } catch ({ response }) {}
  }

  // console.log(refreshNotifications);
  async function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("userId");
    localStorage.removeItem("userEmail");
    localStorage.removeItem("userName");
    setToken(null);
    console.log("tokie");
  }

  async function markAllHandler() {
    try {
      let { data } = await Api.post(APIURLS.markAllNotifications);
      await queryClient.refetchQueries(APIURLS.getNotifications());
      console.log(data);
    } catch ({ response }) {}
  }
  async function markIndividualHandler(id) {
    console.log(id);
    try {
      let { data } = await Api.post(APIURLS.markIndividualNotifications(), {
        id: id,
      });
      await queryClient.refetchQueries(APIURLS.getNotifications());
      toast({
        title: "Notification Marked Read.",
        description: data?.result,
        status: "success",
        duration: 9000,
        isClosable: false,
      });
      console.log();
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

  return (
    <>
      {/* <Sidebar isOpen={isOpen} onOpen={onOpen} onClose={onClose} /> */}
      <Box
        gridColumn={2}
        px={4}
        display={["flex"]}
        flexDirection={["column", "row"]}
        justifyContent="space-between"
        height={50}
        background="white"
        boxShadow="0 2px 4px 0 rgba(0,0,0,.07)"
      >
        {location.pathname === "/dashboard" ? (
          <Breadcrumb
            style={{ padding: "25px", paddingLeft: "0px", color: "#8071b3" }}
          >
            <BreadcrumbItem>
              <Tooltip label="Dashboard" placement="top-start" bg="#8071b399">
                <BreadcrumbLink as={Link} to="/dashboard">
                  {" "}
                  <Icon
                    as={AiFillHome}
                    w={5}
                    h={5}
                    // mr={3}
                    mb={1}
                    color={"#8071b3"}
                  />
                </BreadcrumbLink>
              </Tooltip>
            </BreadcrumbItem>
          </Breadcrumb>
        ) : location.pathname === "/database" ? (
          <Breadcrumb
            style={{ padding: "25px", paddingLeft: "0px", color: "#8071b3" }}
          >
            <BreadcrumbItem>
              <BreadcrumbLink as={Link} to="/dashboard">
                {" "}
                <Icon
                  as={AiFillHome}
                  w={5}
                  h={5}
                  // mr={3}
                  mb={1}
                  color={"#8071b3"}
                />
              </BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbItem>
              <BreadcrumbLink as={Link} to="/database">
                Database
              </BreadcrumbLink>
            </BreadcrumbItem>
          </Breadcrumb>
        ) : location.pathname === "/deploy/aws" ? (
          <Breadcrumb
            style={{ padding: "25px", paddingLeft: "0px", color: "#8071b3" }}
          >
            <BreadcrumbItem>
              <BreadcrumbLink as={Link} to="/dashboard">
                {" "}
                <Icon
                  as={AiFillHome}
                  w={5}
                  h={5}
                  // mr={3}
                  mb={1}
                  color={"#8071b3"}
                />
              </BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbItem>
              <BreadcrumbLink as={Link} to="/deploy/aws">
                AWS
              </BreadcrumbLink>
            </BreadcrumbItem>
          </Breadcrumb>
        ) : location.pathname === "/deploy/heroku" ? (
          <Breadcrumb
            style={{ padding: "25px", paddingLeft: "0px", color: "#8071b3" }}
          >
            <BreadcrumbItem>
              <BreadcrumbLink as={Link} to="/dashboard">
                {" "}
                <Icon
                  as={AiFillHome}
                  w={5}
                  h={5}
                  // mr={3}
                  mb={1}
                  color={"#8071b3"}
                />
              </BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbItem>
              <BreadcrumbLink as={Link} to="/deploy/heroku">
                Heroku
              </BreadcrumbLink>
            </BreadcrumbItem>
          </Breadcrumb>
        ) : location.pathname === "/plugin/sendgrid" ? (
          <Breadcrumb
            style={{ padding: "25px", paddingLeft: "0px", color: "#8071b3" }}
          >
            <BreadcrumbItem>
              <BreadcrumbLink as={Link} to="/dashboard">
                {" "}
                <Icon
                  as={AiFillHome}
                  w={5}
                  h={5}
                  // mr={3}
                  mb={1}
                  color={"#8071b3"}
                />
              </BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbItem>
              <BreadcrumbLink as={Link} to="/plugin/sendgrid">
                Sendgrid
              </BreadcrumbLink>
            </BreadcrumbItem>
          </Breadcrumb>
        ) : location.pathname === "/plugin/Twilio" ? (
          <Breadcrumb
            style={{ padding: "25px", paddingLeft: "0px", color: "#8071b3" }}
          >
            <BreadcrumbItem>
              <BreadcrumbLink as={Link} to="/dashboard">
                {" "}
                <Icon
                  as={AiFillHome}
                  w={5}
                  h={5}
                  // mr={3}
                  mb={1}
                  color={"#8071b3"}
                />
              </BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbItem>
              <BreadcrumbLink as={Link} to="/plugin/Twilio">
                Twilio
              </BreadcrumbLink>
            </BreadcrumbItem>
          </Breadcrumb>
        ) : (
          <Breadcrumb
            style={{ padding: "25px", paddingLeft: "0px", color: "#8071b3" }}
          >
            <BreadcrumbItem>
              <BreadcrumbLink as={Link} to="/dashboard">
                {" "}
                <Icon
                  as={AiFillHome}
                  w={5}
                  h={5}
                  // mr={3}
                  mb={1}
                  color={"#8071b3"}
                />
              </BreadcrumbLink>
            </BreadcrumbItem>
          </Breadcrumb>
        )}
        <Box type={["column", "row"]} textAlign="center">
          {!token ? (
            <>
              {" "}
              <NavLink to="/signup">
                <Button mr={4}>Sign up </Button>
              </NavLink>
              <NavLink to="/login">
                <Button mb={[4, 0]}>Log in</Button>
              </NavLink>{" "}
            </>
          ) : (
            // <Button mb={[4, 0]} onClick={handleLogout}>
            //   Sign out
            // </Button>
            <>
              <Box type="row" justifyContent="start" mt={2} mb={2}>
                <Menu
                  style={{
                    marginRight: "3px",
                  }}
                >
                  <Box
                    style={{
                      backgroundColor: "#372e6c",
                      borderRadius: "50px",
                    }}
                  >
                    <Box>
                      <Box
                        style={{
                          borderRadius: "50px",
                          boxShadow: "rgb(10 10 10) 0px 2px 4px -1px",
                          background: "#80808045",
                          height: "40px",
                          width: "40px",
                        }}
                      >
                        {" "}
                        <Tooltip
                          label="Click to view notifications"
                          placement="top-start"
                          bg="#8071b399"
                        >
                          <MenuButton
                            style={{ color: "#ffffff", padding: "8px" }}
                          >
                            {" "}
                            <Icon
                              as={FaBell}
                              w={5}
                              h={5}
                              onClick={() => notificationRefreshHandler()}
                            />
                          </MenuButton>
                        </Tooltip>
                      </Box>
                    </Box>
                  </Box>

                  <MenuList>
                    <MotionBox
                      bg="white"
                      boxShadow="invisionHover"
                      width="fit-content"
                      initial={{ y: -50, opacity: 0 }}
                      animate={{
                        y: 0,
                        opacity: 1,
                      }}
                      p={4}
                      type="column"
                      width={["90vw", 350]}
                      maxHeight="600px"
                      overflowX="scroll"
                    >
                      <Para fontSize={6} mb={1}>
                        Notifications
                      </Para>
                      <Box
                        borderBottom="4px solid"
                        borderColor="purple"
                        mb={2}
                      ></Box>

                      {data?.length ? (
                        data?.reverse()?.map((key) => (
                          <Box
                            borderBottom="1px solid #e1e1e1"
                            py={4}
                            bg={key.mark_read ? "white" : "#80808017"}
                            pl={1}
                            textAlign={"left"}
                            onClick={() =>
                              key.mark_read
                                ? markIndividualHandler(key.id)
                                : null
                            }
                          >
                            {/* <H5 fontSize={5}>{"heading"}</H5> */}
                            <H5 color="grey" fontSize={3} fontWeight="normal">
                              {key.message}
                            </H5>
                            <H5
                              color="grey"
                              fontSize={1}
                              fontWeight="normal"
                              mb={0}
                            >
                              {key.received_at}
                            </H5>
                          </Box>
                        ))
                      ) : (
                        <Box
                          borderBottom="1px solid #e1e1e1"
                          py={4}
                          bg={"#80808017"}
                          pl={1}
                          textAlign={"left"}
                        >
                          <H5 color="grey" fontSize={3} fontWeight="normal">
                            {"No Notifications"}.
                          </H5>
                        </Box>
                      )}
                      {data?.length ? (
                        <Button width={"100%"} mt={2} onClick={markAllHandler}>
                          Mark All Read
                        </Button>
                      ) : null}
                    </MotionBox>
                  </MenuList>
                </Menu>

                <Menu>
                  <Box
                    style={{
                      backgroundColor: "#372e6c",
                      borderRadius: "50px",
                      marginLeft: "5px",
                    }}
                  >
                    <Box>
                      <Box
                        style={{
                          borderRadius: "50px",
                          boxShadow: "rgb(10 10 10) 0px 2px 4px -1px",
                          background: "#80808045",
                          height: "40px",
                          width: "40px",
                        }}
                      >
                        <Tooltip
                          label="Profile & Help"
                          placement="top-start"
                          bg="#8071b399"
                        >
                          <MenuButton
                            style={{ color: "#ffffff", padding: "8px" }}
                          >
                            <Icon as={AiFillCaretDown} w={5} h={5} />
                          </MenuButton>
                        </Tooltip>
                      </Box>
                    </Box>
                  </Box>

                  <MenuList>
                    <MenuGroup title={<Para>Profile</Para>}>
                      <MenuItem>
                        <Para>My Account</Para>
                      </MenuItem>
                      <MenuItem onClick={handleLogout}>
                        <Para>Log out</Para>
                      </MenuItem>
                    </MenuGroup>
                    <MenuDivider />
                    <MenuGroup title={<Para>Help</Para>}>
                      <MenuItem>
                        <Para>Docs</Para>
                      </MenuItem>
                      <MenuItem>
                        <Para>FAQ</Para>
                      </MenuItem>
                    </MenuGroup>
                  </MenuList>
                </Menu>
              </Box>
            </>
          )}
        </Box>
      </Box>
    </>
  );
};

function UserMenu() {
  // const router = useRouter();
  const [token, setToken] = useGlobal("token");
  // const queryCache = useQueryCache();

  // const userProfile = useQuery(APIURLS.getUserDetails, {
  //   enabled: !!token,
  // });

  // let user = userProfile?.data?.data?.user || {};

  async function handleLogout() {
    try {
      localStorage.clear();
      setToken(null);
    } catch (error) {}
  }

  // useEffect(() => {
  //   let userId = localStorage.getItem("userId");
  //   if (userId) {
  //     connectToPusher(userId);
  //   }
  // }, []);

  return (
    <Box
      display="flex"
      flexDirection={["column", "row"]}
      justifyContent="space-between"
      alignItems={["flex-end", "center"]}
      ml={[0]}
    >
      <Box>
        <Trigger
          action={["click", "focus"]}
          destroyPopupOnHide
          popup={
            <AdminProfile
              // user={user}
              handleLogout={handleLogout}
            />
          }
          popupAlign={{
            points: ["tl", "tl"],
            // offset: [10, 3],
          }}
          alignPoint
        >
          <Icon as={FaUserAlt} />
        </Trigger>
      </Box>
    </Box>
  );
}

export default Header;