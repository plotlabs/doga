import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { NavLink } from "react-router-dom";
import { useGlobal } from "reactn";
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
  Para,
} from "../../styles";
import {
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
} from "@chakra-ui/react";
import { Icon } from "@chakra-ui/react";
import { useQuery, useQueryClient } from "react-query";
import { useToast, createStandaloneToast } from "@chakra-ui/react";
import Api, { setJwtHeader, APIURLS, ApiUpload } from "../../Api";
import Select from "react-select";

const ImageUploadSelect = ({ setMarkedImage, markedImage }) => {
  const [token] = useGlobal("token");
  const { handleSubmit, register, errors } = useForm();
  const [selectedImage, setSelectedImage] = useState();

  const queryClient = useQueryClient();
  const toast = createStandaloneToast();
  const { data, isLoading } = useQuery(APIURLS.getUserImages);
  console.log("here are our images", data);
  async function fileUpload() {
    // e.preventDefault();
    try {
      const formData = new FormData();
      formData.append("image", selectedImage);
      let { data } = await ApiUpload.post(APIURLS.uploadImage(), formData);
      console.log(data);
      toast({
        title: "Success",
        description: data?.result,
        status: "success",
        duration: 9000,
        isClosable: false,
      });
      await queryClient.refetchQueries(APIURLS.getUserImages);
    } catch ({ response }) {
      toast({
        title: "An error occurred.",
        // description: response?.data?.result,
        status: "error",
        duration: 9000,
        isClosable: true,
      });
      console.log(response);
    }
  }

  const fileSelectHandler = (event) => {
    setSelectedImage(event.target.files[0]);
  };

  return (
    <>
      <Box type="row">
        {/* <Button ></Button> */}
        <Box type="relative">
          <Input
            id="fileButton"
            color="grey"
            type="file"
            accept=".jpeg, .png, .jpg"
            fontSize={3}
            p={2}
            // defaultValue={editDataId ? data?.result[val.name] : null}
            onChange={fileSelectHandler}
            width="100%"
            mb={2}
          />
        </Box>
        <Button type="button" onClick={fileUpload} mb={"10px"}>
          Add
        </Button>
        {/* <Button onClick={fileUploadButton}>Image Upload</Button> */}
      </Box>
      <Accordion allowToggle style={{ padding: "20px" }}>
        <AccordionItem>
          <AccordionButton>
            <Box type="row" justifyContent="start" width="100%">
              {" "}
              <Para ml={4} color={"#2a3950"}>
                {"Select Image"}
              </Para>
            </Box>
            <AccordionIcon />
          </AccordionButton>
          <AccordionPanel pb={4} style={{ backgroundColor: "#f7f8fb" }}>
            <Box
              display="grid"
              gridTemplateColumns={["1fr 1fr", "1fr 1fr 1fr "]}
              // mb={8}
              gridGap={4}
              style={{
                height: "245px",
                overflowY: "scroll",
              }}
            >
              {data &&
                Object.entries(data).map(([index, val]) => {
                  console.log(index, val);
                  console.log(val["image"]);
                  return (
                    <Box>
                      {" "}
                      <Image
                        src={`data:image/png;base64, ${val["image"]}`}
                        onClick={() => setMarkedImage(val["image"])}
                        style={{
                          border:
                            markedImage == val["image"]
                              ? "3px solid #8071b3"
                              : null,
                          padding: "2px",
                        }}
                        // src="/Users/nishantrana/Desktop/doga/doga-frontend/public/uploads/654fdb5dc9eab375a46bdd1c17f4f051.jpg"
                      ></Image>
                    </Box>
                  );
                })}
            </Box>
          </AccordionPanel>
        </AccordionItem>
      </Accordion>

      {/* <Box type="row" justifyContent="center" m={6}>
              <form
                onSubmit={handleSubmit(handleSignup)}
                style={{ width: "35vw" }}
              >
                 //   <Label>{val}</Label>
          <Box type="relative">
          <Input
              name={val}
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
                <Button mt={4} width="100%" fontSize={18} type="submit">
                  {"Login"}
                </Button>
              </form>
            </Box>
          */}
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

export default ImageUploadSelect;
