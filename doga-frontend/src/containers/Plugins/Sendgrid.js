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
  Tooltip,
  Switch,
  Icon,
  createStandaloneToast,
} from "@chakra-ui/react";
import { BsPlusCircleFill } from "react-icons/bs";
import { FaUser } from "react-icons/fa";
import { AiOutlineDelete } from "react-icons/ai";
import { useQuery, useQueryClient } from "react-query";
import Api, { APIURLS } from "../../Api";

const Sendgrid = (props) => {
  const [token] = useGlobal("token");
  const { handleSubmit, register, errors } = useForm();
  const [toggle, setToggle] = useState(true);
  const [username, setUsername] = useState();
  const [userKey, setUserKey] = useState();
  const [templateValueCheck, setTemplateValueCheck] = useState();
  const [userEmail, setUserEmail] = useState();
  const [userList, setUserList] = useState({});
  const [userValue, setUserValue] = useState();
  const [userTemplateList, setUserTemplateList] = useState({});
  const [success, setSuccess] = useState(false);
  let authRedirect = null;
  if (success) {
    authRedirect = <Redirect to="/dashboard" />;
  }
  const toast = createStandaloneToast();
  const queryClient = useQueryClient();
  const { data } = useQuery([APIURLS.getContentType], {
    enabled: !!token,
  });
  console.log(userList, "user", userTemplateList);
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
      let obj = {
        _from: params["_from"],
        api_key: params.api_key,
        to_emails: userList,
        template_key: params.template_key,
        subject: params.subject,
        content: templateValueCheck ? userTemplateList : params.content,
      };

      let { data } = await Api.post(APIURLS.emailNotify(), obj);

      toast({
        title: "Success",
        description: data?.result,
        status: "success",
        duration: 9000,
        isClosable: false,
      });
      setSuccess(true);
    } catch ({ response }) {
      toast({
        title: "An error occurred.",
        description: response?.data?.result,
        status: "error",
        duration: 9000,
        isClosable: true,
      });
      setSuccess(false);
    }
  }
  const addUserHandler = () => {
    // setUserList(JSON.stringify({ ...userList, [username]: userEmail }));
    setUserList({ ...userList, [username]: userEmail });
    setUsername("");
    setUserEmail("");
  };
  const removeUserHandler = (index) => {
    let obj = userList;
    delete obj[index];
    setUserList({ ...obj });
  };
  const addUserTemplateHandler = () => {
    setUserTemplateList({ ...userTemplateList, [userKey]: userValue });
    setUserKey("");
    setUserValue("");
  };
  const removeUserTemplateHandler = (index) => {
    let obj = userTemplateList;
    delete obj[index];
    setUserTemplateList({ ...obj });
  };

  console.log("list", userList);
  return (
    <>
      {authRedirect}
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
            <Box type="row" justifyContent="start" my={3}>
              <Tooltip
                label={!templateValueCheck ? "Yes" : "No"}
                bg="#8071b399"
                placement="top"
              >
                <spam>
                  <Switch
                    size="lg"
                    style={{ background: "rgb(241 218 249)" }}
                    // onClick={foreignkeyfn}
                    isChecked={templateValueCheck}
                    onChange={(e) => setTemplateValueCheck(e.target.checked)}
                  />
                </spam>
              </Tooltip>
              <Para ml={6}> Do you want to add Sendgrid's Template key</Para>{" "}
            </Box>
            {templateValueCheck && <Label>Sendgrid's Template key</Label>}
            {templateValueCheck && (
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
            )}

            <Label>Subject</Label>
            <Box type="relative">
              <Input
                name={"subject"}
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
            {!templateValueCheck ? (
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
            ) : (
              <Accordion allowToggle>
                <AccordionItem>
                  <AccordionButton>
                    <Box type="row" justifyContent="start" width="100%">
                      <Para ml={4} color={"#2a3950"}>
                        {"Add content to your template"}
                      </Para>
                    </Box>

                    <AccordionIcon />
                  </AccordionButton>
                  <AccordionPanel pb={4} style={{ backgroundColor: "#f7f8fb" }}>
                    <Box>
                      <Label mt={6}>key</Label>
                      <Box type="relative">
                        <Input
                          name={"key"}
                          color="grey"
                          fontSize={3}
                          p={2}
                          width="100%"
                          ref={register}
                          mb={2}
                          value={userKey}
                          onChange={(e) => setUserKey(e.target.value)}
                        />

                        {errors?.name && (
                          <Span color="orange" mb={4}>
                            {errors?.name?.message}
                          </Span>
                        )}
                      </Box>
                      <Label>Value</Label>
                      <Box type="relative">
                        <Input
                          color="grey"
                          fontSize={3}
                          p={2}
                          width="100%"
                          ref={register}
                          mb={2}
                          value={userValue}
                          onChange={(e) => setUserValue(e.target.value)}
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
                          w={"2.5rem"}
                          h={"2.5rem"}
                          color={"rgb(56 46 108 / 92%)"}
                          mt={3}
                          onClick={addUserTemplateHandler}
                        />
                      </Box>
                      <Box>
                        {Object.keys(userTemplateList).map((key, index) => {
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
                                <Para ml={2}> {userTemplateList[key]}</Para>
                              </Box>
                              <Box>
                                <Icon
                                  as={AiOutlineDelete}
                                  w={"1.5rem"}
                                  h={"1.5rem"}
                                  color={"red"}
                                  onClick={() => removeUserTemplateHandler(key)}
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
            )}

            <Button mt={4} width="100%" fontSize={18} type="submit">
              {"Send"}
            </Button>
          </form>
        </Box>

        <Box m={6}>
          <Accordion allowToggle mt={7}>
            <AccordionItem>
              <AccordionButton>
                <Box type="row" justifyContent="start" width="100%">
                  <Para ml={4} color={"#2a3950"}>
                    {"Add Users you want to send mail to"}
                  </Para>
                </Box>

                <AccordionIcon />
              </AccordionButton>
              <AccordionPanel pb={4} style={{ backgroundColor: "#f7f8fb" }}>
                <Label mt={2}>Username</Label>
                <Box type="relative">
                  <Input
                    color="grey"
                    fontSize={3}
                    p={2}
                    width="100%"
                    ref={register}
                    mb={2}
                    value={username}
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
                    color="grey"
                    fontSize={3}
                    p={2}
                    width="100%"
                    ref={register}
                    mb={2}
                    value={userEmail}
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
                  {Object.keys(userList).map((key, index) => {
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
                          <Para ml={2}> {userList[key]}</Para>
                        </Box>
                        <Box>
                          <Icon
                            as={AiOutlineDelete}
                            w={"1.5rem"}
                            h={"1.5rem"}
                            color={"red"}
                            onClick={() => removeUserHandler(key)}
                          />
                        </Box>
                      </Box>
                    );
                  })}
                </Box>
              </AccordionPanel>
            </AccordionItem>
          </Accordion>
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
