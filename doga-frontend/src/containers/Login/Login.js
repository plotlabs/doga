import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { useGlobal } from "reactn";
import { NavLink } from "react-router-dom";
import { Redirect } from "react-router-dom";
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
} from "../../styles";
import Api, { setHeader, APIURLS } from "../../Api";
import { Icon } from "@chakra-ui/react";
import { FaUserAlt } from "react-icons/fa";
import { MdEmail } from "react-icons/md";
import { RiLockPasswordFill } from "react-icons/ri";
import ClipLoader from "react-spinners/ClipLoader";
import { useToast, createStandaloneToast } from "@chakra-ui/react";
import { useQuery, useQueryClient } from "react-query";

const Login = () => {
  // const router = useRouter();
  const [token, setToken] = useGlobal("token");
  // const [, setForgotPassword] = useGlobal("forgotPassword");
  // const [oldVersionModal, setOldVersionModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [apiErr, setApiErr] = useState(null);
  // const [token] = useGlobal("token");
  const { handleSubmit, register, errors } = useForm();
  const toast = createStandaloneToast();
  let authRedirect = null;
  if (token) {
    authRedirect = <Redirect to="/dashboard" />;
  }

  // useEffect(() => {
  //   // router.prefetch("/dashboard");
  // }, []);

  async function handleSignup(params) {
    try {
      setApiErr(null);
      setLoading(true);
      let { data } = await Api.post(APIURLS.login, params);
      // let version = data?.data.version;

      let token = data?.access_token;
      let userId = data?.id;
      let userEmail = data?.email;
      let userName = data?.name;
      localStorage.setItem("token", token);
      localStorage.setItem("userId", userId);
      localStorage.setItem("userEmail", userEmail);
      localStorage.setItem("userName", userName);
      setHeader(token);
      setToken(token);
      toast({
        title: "Login Successful",
        description: data?.result,
        status: "success",
        duration: 9000,
        isClosable: false,
      });
      setLoading(false);
    } catch ({ response }) {
      toast({
        title: "An error occurred.",
        description: response?.data?.result,
        status: "error",
        duration: 9000,
        isClosable: true,
      });
      setApiErr(response?.result);
      setLoading(false);
    }
  }

  return (
    <>
      {authRedirect}
      <Box
        style={{
          height: "100vh",

          backgroundColor: "#382e6c",
        }}
      >
        <MotionBox
          display="flex"
          initial={{ y: 50, opacity: 0 }}
          animate={{
            y: 0,
            opacity: 1,
          }}
          style={{
            height: "100vh",
            justifyContent: "center",
            display: "flex",
            backgroundColor: "#382e6c",
            alignItems: "center",
          }}
        >
          <Box
            display="flex"
            flexDirection="column"
            justifyContent="center"
            style={{
              width: "30%",
              // padding: "50px",
              borderRadius: "10px",
              boxShadow: "#161617 0px 2px 4px -1px",
              backgroundColor: "#ffffff",
            }}
          >
            <Box
              type="row"
              alignItems="center"
              width="100%"
              style={{ padding: "50px 30px 30px 50px" }}
            >
              <H2 color={"#8071b3"}>Login</H2>
            </Box>

            <Box style={{ padding: "0px 50px 30px 50px" }}>
              <form onSubmit={handleSubmit(handleSignup)}>
                <Label>Email</Label>
                <Box type="relative">
                  <Input
                    name="email"
                    type="email"
                    color="grey"
                    required
                    fontSize={3}
                    p={2}
                    //   placeholder=""
                    width="100%"
                    ref={register}
                    mb={2}
                    inputType="auth"
                  />
                  <Span type="icon">
                    <i>
                      <Icon as={MdEmail} w={5} h={6} />
                    </i>
                  </Span>

                  {errors?.email && (
                    <Span color="orange" mb={4}>
                      {errors?.email?.message}
                    </Span>
                  )}
                </Box>
                <Label>Password</Label>
                <Box type="relative">
                  <Input
                    name="password"
                    type="password"
                    color="grey"
                    fontSize={3}
                    required
                    p={2}
                    //   placeholder=""
                    ref={register}
                    width="100%"
                    mb={2}
                    inputType="auth"
                  />

                  <Span type="icon">
                    <i>
                      <Icon as={RiLockPasswordFill} w={5} h={6} />
                    </i>
                  </Span>

                  {errors?.password && (
                    <Span color="#8071b3" mb={4}>
                      {errors?.password?.message}
                    </Span>
                  )}
                </Box>

                {apiErr && (
                  <Span color="#8071b3" mb={4}>
                    {apiErr}
                  </Span>
                )}

                <Button mt={4} width="100%" fontSize={18}>
                  {loading ? (
                    <ClipLoader color={"#ffffff"} size={25} />
                  ) : (
                    "Login"
                  )}
                </Button>
              </form>
            </Box>
            <Box
              type="row-reverse"
              width="100%"
              style={{
                padding: "30px 0px 30px 0px",

                backgroundColor: "#f5f5f5",
                borderTop: "1px solid #ddd",
                textAlign: "center",
                borderRadius: "10px",
              }}
            >
              <Span>
                {"New to Doga?               "}
                <NavLink to={`/signup`}>
                  {" "}
                  <Span color="#8071b3" style={{ cursor: "pointer" }}>
                    {" "}
                    Sign Up
                  </Span>{" "}
                </NavLink>
              </Span>
            </Box>
          </Box>
        </MotionBox>
      </Box>
    </>
  );
};

export default Login;
