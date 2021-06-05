import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useGlobal } from "reactn";
import { Redirect } from "react-router-dom";
import { Box, Button, Span, Input, Label, Para } from "../../styles";
import {
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
} from "@chakra-ui/react";
import { Icon } from "@chakra-ui/react";
import { BsPlusCircleFill } from "react-icons/bs";
import { FaUser } from "react-icons/fa";
import { AiOutlineDelete } from "react-icons/ai";
import { useQuery, useQueryClient } from "react-query";
import { createStandaloneToast } from "@chakra-ui/react";
import Api, { APIURLS } from "../../Api";

const Notify = (props) => {
  const [token] = useGlobal("token");
  const { handleSubmit, register, errors } = useForm();
  const [userNumber, setUserNumber] = useState();
  const [success, setSuccess] = useState(false);
  let authRedirect = null;
  if (success) {
    authRedirect = <Redirect to="/dashboard" />;
  }
  const [userList, setUserList] = useState([]);
  const toast = createStandaloneToast();
  const { data } = useQuery([APIURLS.getContentType], {
    enabled: !!token,
  });
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
      let obj = {
        account_sid: params.account_sid,
        auth_token: params.auth_token,
        _from: params._from,
        to: userList,
        message: params.message,
      };
      let { data } = await Api.post(APIURLS.smsNotify(), obj);

      toast({
        title: "Success",
        description: data?.result,
        status: "success",
        duration: 9000,
        isClosable: false,
      });
      setSuccess(true);
    } catch ({ response }) {
      setSuccess(false);
    }
  }
  const addUserHandler = () => {
    setUserList([...userList, userNumber]);
    setUserNumber("");
  };
  const removeUserHandler = (index) => {
    let newUserList = [];
    for (let key in userList) {
      if (key != index) {
        newUserList.push(userList[key]);
      }
    }

    setUserList(newUserList);
  };

  return (
    <>
      {authRedirect}
      <Box type="heading" textAlign="center">
        <Span type="heading">TWILIO</Span>
      </Box>

      <Box
        display="grid"
        gridTemplateColumns={["1fr", "1fr 1fr"]}
        gridGap={4}
        style={{
          padding: "40px",
        }}
      >
        <Box type="row" justifyContent="center" m={6}>
          <form onSubmit={handleSubmit(handleSignup)} style={{ width: "35vw" }}>
            <Label>Twilio's Account Sid</Label>
            <Box type="relative">
              <Input
                name={"account_sid"}
                color="grey"
                fontSize={3}
                p={2}
                required
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
            <Label>Twilio's Auth Token</Label>
            <Box type="relative">
              <Input
                name={"auth_token"}
                color="grey"
                fontSize={3}
                p={2}
                required
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
            <Label>SMS From</Label>
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
              />

              {errors?.name && (
                <Span color="orange" mb={4}>
                  {errors?.name?.message}
                </Span>
              )}
            </Box>
            <Label>Message</Label>
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
        <Accordion allowToggle mt={8} p={4}>
          <AccordionItem>
            <AccordionButton>
              <Box type="row" justifyContent="start" width="100%">
                <Para ml={4} color={"#2a3950"}>
                  {"Add phone number of users you want to send SMS"}
                </Para>
              </Box>

              <AccordionIcon />
            </AccordionButton>
            <AccordionPanel pb={4} style={{ backgroundColor: "#f7f8fb" }}>
              <Box>
                <Label mt={6}>Username Phone Number</Label>
                <Box type="relative">
                  <Input
                    name={"to"}
                    color="grey"
                    fontSize={3}
                    p={2}
                    required
                    width="100%"
                    ref={register}
                    mb={2}
                    value={userNumber}
                    onChange={(e) => setUserNumber(e.target.value)}
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
                    return (
                      <Box
                        key={index}
                        boxShadow="card"
                        type="row"
                        justifyContent="space-between"
                        style={{
                          height: "50px",
                          backgroundColor: "rgb(75 78 114 / 22%)",
                        }}
                        m={4}
                        p={2}
                      >
                        <Box type="row" justifyContent="flex-start">
                          <Icon
                            as={FaUser}
                            w={"1.5rem"}
                            h={"1.5rem"}
                            color={"rgb(72 62 120)"}
                          />
                          {/* <Para ml={2}> {user}</Para> */}
                          <Para ml={2}> {key}</Para>
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
            </AccordionPanel>
          </AccordionItem>
        </Accordion>
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

export default Notify;
