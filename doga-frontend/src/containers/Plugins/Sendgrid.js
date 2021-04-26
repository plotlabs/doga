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
  H5,
  Input,
  Label,
  Para,
} from "../../styles";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
} from "@chakra-ui/react";
import { Icon } from "@chakra-ui/react";
import { MdEmail, MdTextsms } from "react-icons/md";
import { BsPlusCircleFill } from "react-icons/bs";
import { FaUser } from "react-icons/fa";
import { AiOutlineDelete } from "react-icons/ai";
import { useQuery, useQueryClient } from "react-query";
import { useToast, createStandaloneToast } from "@chakra-ui/react";
import Api, { setHeader, APIURLS, ApiJwt } from "../../Api";
import Select from "react-select";

const Sendgrid = (props) => {
  const [token] = useGlobal("token");
  const { handleSubmit, register, errors } = useForm();
  const [toggle, setToggle] = useState(true);
  const [username, setUsername] = useState();
  const [userEmail, setUserEmail] = useState();
  const [userList, setUserList] = useState([]);
  // const queryClient = useQueryClient();
  const toast = createStandaloneToast();
  const queryClient = useQueryClient();
  const { data } = useQuery([APIURLS.getContentType], {
    enabled: !!token,
  });
  console.log(username, "user", userEmail);
  //   let contentTypeApps = null;
  let selectAppName = [];
  if (data) {
    for (let key in data) {
      selectAppName.push({
        value: key,
        label: key,
      });
    }
  }

  async function handleSignup(params) {
    try {
      if (toggle) {
        let obj = {
          _from: params._from,
          api_key: params.api_key,
          to_emails: userList,
          template_key: params.template_key,
          subject: params.subject,
          content: params.content,
        };
        let { data } = await Api.post(APIURLS.emailNotify(), obj);
      } else {
        let obj = {
          account_sid: params.account_sid,
          auth_token: params.auth_token,
          _from: params._from,
          to_emails: userList,
          message: params.message,
          // "tier": "hobby-dev"
        };
        let { data } = await Api.post(APIURLS.smsNotify(), obj);
      }

      toast({
        title: "Success",
        description: data?.result,
        status: "success",
        duration: 9000,
        isClosable: false,
      });
      //   await queryClient.refetchQueries([
      //     APIURLS.getTableContent({ app, table }),
      //     "jwt_info",
      //   ]);

      //   onClose();
    } catch ({ response }) {}
  }
  const addUserHandler = () => {
    setUserList([...userList, { [username]: userEmail }]);
    setUsername();
    setUserEmail();
  };
  const removeUserHandler = (index) => {
    let newUserList = [];
    for (let key in userList) {
      console.log(userList[key], "key", key);
      if (key != index) {
        newUserList.push(userList[key]);
      }
    }
    //  userList.slice(0, index).concat(userList.slice(-index));
    console.log(newUserList);
    setUserList(newUserList);
    // console.log(userList.splice(index, 1))
  };

  console.log("list", userList);
  return (
    <>
      <Box type="heading" textAlign="center">
        <Span type="heading">SENDGRID</Span>
      </Box>
      <Box
        display="grid"
        gridTemplateColumns={["1fr", "1fr 1fr"]}
        // mb={8}
        gridGap={4}
        style={{
          padding: "40px",
        }}
      >
        <Box type="row" justifyContent="center" m={6}>
          <form onSubmit={handleSubmit(handleSignup)} style={{ width: "35vw" }}>
            <Label>Sendgrid's Email ID</Label>
            <Box type="relative">
              <Input
                name={"_from"}
                color="grey"
                required
                fontSize={3}
                p={2}
                width="100%"
                ref={register}
                mb={2}
              />

              {errors?.name && (
                <Span color="orange" mb={4}>
                  {errors?.name?.message}
                </Span>
              )}
            </Box>
            <Label>Sendgrid's Api key</Label>
            <Box type="relative">
              <Input
                name={"api_key"}
                color="grey"
                required
                fontSize={3}
                p={2}
                width="100%"
                ref={register}
                mb={2}
              />

              {errors?.name && (
                <Span color="orange" mb={4}>
                  {errors?.name?.message}
                </Span>
              )}
            </Box>
            <Label>Sendgrid's Template key</Label>
            <Box type="relative">
              <Input
                name={"template_key"}
                color="grey"
                required
                fontSize={3}
                p={2}
                // defaultValue={editDataId ? data?.result[val.name] : null}
                width="100%"
                ref={register}
                mb={2}
              />

              {errors?.name && (
                <Span color="orange" mb={4}>
                  {errors?.name?.message}
                </Span>
              )}
            </Box>

            <Label>Subject</Label>
            <Box type="relative">
              <Input
                name={"region_name"}
                color="grey"
                fontSize={3}
                p={2}
                width="100%"
                ref={register}
                mb={2}
              />

              {errors?.name && (
                <Span color="orange" mb={4}>
                  {errors?.name?.message}
                </Span>
              )}
            </Box>
            <Label>Content</Label>
            <Box type="relative">
              <Input
                name={"content"}
                color="grey"
                fontSize={3}
                p={2}
                // defaultValue={editDataId ? data?.result[val.name] : null}
                width="100%"
                ref={register}
                mb={2}
              />

              {errors?.name && (
                <Span color="orange" mb={4}>
                  {errors?.name?.message}
                </Span>
              )}
            </Box>

            <Button mt={4} width="100%" fontSize={18} type="submit">
              {"Send"}
            </Button>
          </form>
        </Box>

        <Box>
          <Label mt={6}>Username</Label>
          <Box type="relative">
            <Input
              name={"_from"}
              color="grey"
              fontSize={3}
              p={2}
              required
              width="100%"
              ref={register}
              mb={2}
              onChange={(e) => setUsername(e.target.value)}
            />

            {errors?.name && (
              <Span color="orange" mb={4}>
                {errors?.name?.message}
              </Span>
            )}
          </Box>
          <Label>User Email ID</Label>
          <Box type="relative">
            <Input
              name={"message"}
              color="grey"
              fontSize={3}
              p={2}
              required
              width="100%"
              ref={register}
              mb={2}
              onChange={(e) => setUserEmail(e.target.value)}
            />

            {errors?.name && (
              <Span color="orange" mb={4}>
                {errors?.name?.message}
              </Span>
            )}
          </Box>
          <Box style={{ textAlign: "center" }}>
            <Icon
              as={BsPlusCircleFill}
              w={"3.5rem"}
              h={"3.5rem"}
              color={"rgb(56 46 108 / 92%)"}
              mt={5}
              onClick={addUserHandler}
            />
          </Box>
          <Box>
            {userList.map((key, index) => {
              let user = Object.keys(key)[0];
              console.log(index);
              return (
                <Box
                  boxShadow="card"
                  type="row"
                  justifyContent="space-between"
                  style={{
                    height: "50px",
                    backgroundColor: "rgb(241 218 249)",
                  }}
                  m={4}
                  p={2}
                >
                  <Box type="row" justifyContent="flex-start">
                    <Icon
                      as={FaUser}
                      w={"1.5rem"}
                      h={"1.5rem"}
                      color={"rgb(157 57 160 / 87%)"}
                    />
                    {/* <Para ml={2}> {user}</Para> */}
                    <Para ml={2}> {key[user]}</Para>
                  </Box>
                  <Box>
                    <Icon
                      as={AiOutlineDelete}
                      w={"1.5rem"}
                      h={"1.5rem"}
                      color={"red"}
                      onClick={() => removeUserHandler(index)}
                    />
                  </Box>
                </Box>
              );
            })}
          </Box>
        </Box>
      </Box>
    </>
  );
};

const CARD_ELEMENT_OPTIONS = {
  style: {
    base: {
      color: "#32325d",
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: "antialiased",
      fontSize: "18px",
      "::placeholder": {
        color: "#aab7c4",
      },
    },
    invalid: {
      color: "#fa755a",
      iconColor: "#fa755a",
    },
  },
};

export default Sendgrid;
