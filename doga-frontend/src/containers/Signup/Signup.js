import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { useGlobal } from "reactn";
import { NavLink } from "react-router-dom";
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

const Signup = () => {
  const [token] = useGlobal("token");
  const { handleSubmit, register, errors } = useForm();
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [apiErr, setApiErr] = useState(null);

  async function handleSignup(params) {
    try {
      //   setApiErr(null);
      setLoading(true);
      let { data } = await Api.post(APIURLS.signup, {
        ...params,
      });

      //   let token = data?.data.user?.accessToken;
      //   let userId = data?.data.user?.id;
      //   localStorage.setItem("token", token);
      //   localStorage.setItem("userId", userId);
      //   setHeader(token);
      //   setToken(token);
      //   router.push("/onboarding");
      setLoading(false);
      setSuccess(true);

      console.log("data", data);
    } catch ({ response }) {
      console.log(response);
      //   setApiErr(response?.data?.message);
      setLoading(false);
    }
    console.log(params);
  }

  return (
    <>
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
            {/* <Image src="doga_login.png" width="80px"></Image> */}
            {success ? (
              <MotionBox
                mt={6}
                initial={{ y: 50, opacity: 0 }}
                animate={{
                  y: 0,
                  opacity: 1,
                }}
                transition={{ ease: "easeOut", duration: 0.3 }}
                style={{ padding: "50px" }}
              >
                <H2 fontSize={6}>Account created successfully.</H2>
                <NavLink to="/login">
                  {" "}
                  <Button mt={4} width="100%" fontSize={18}>
                    Login
                  </Button>
                </NavLink>
              </MotionBox>
            ) : (
              <>
                <Box
                  type="row"
                  alignItems="center"
                  width="100%"
                  style={{ padding: "50px 30px 30px 50px" }}
                >
                  <H2 color={"#8071b3"}>Create Account</H2>
                </Box>
                <Box style={{ padding: "0px 50px 30px 50px" }}>
                  <form onSubmit={handleSubmit(handleSignup)}>
                    <Label>Name</Label>
                    <Box type="relative">
                      <Input
                        name="name"
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
                          <Icon as={FaUserAlt} />
                        </i>
                      </Span>

                      {errors?.name && (
                        <Span color="orange" mb={4}>
                          {errors?.name?.message}
                        </Span>
                      )}
                    </Box>
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
                        <Span color="orange" mb={4}>
                          {errors?.password?.message}
                        </Span>
                      )}
                    </Box>

                    {apiErr && (
                      <Span color="orange" mb={4}>
                        {apiErr}
                      </Span>
                    )}

                    <Button mt={4} width="100%" fontSize={18}>
                      {loading ? (
                        <ClipLoader color={"#ffffff"} size={25} />
                      ) : (
                        "Sign up"
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
                    {"Already have an account?      "}
                    <NavLink to={`/login`}>
                      {" "}
                      <Span color="#8071b3" style={{ cursor: "pointer" }}>
                        {" "}
                        Log In
                      </Span>{" "}
                    </NavLink>
                  </Span>
                </Box>
              </>
            )}
          </Box>
        </MotionBox>
      </Box>
    </>
  );
};

export default Signup;
