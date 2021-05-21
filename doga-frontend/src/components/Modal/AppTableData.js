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
import DateTimePicker from "react-datetime-picker";
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
import { useQuery, useQueryClient } from "react-query";
import { useToast, createStandaloneToast } from "@chakra-ui/react";
import Api, {
  setHeader,
  setJwtHeader,
  APIURLS,
  ApiJwt,
  ApiApp,
} from "../../Api";
import Select from "react-select";
import { CKEditor } from "@ckeditor/ckeditor5-react";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import ImageUploadSelect from "../ImageUploadSelect/ImageUploadSelect";

const AppTableData = ({
  isOpen,
  onOpen,
  onClose,
  app,
  columns,
  table,
  editDataId,
  basejwt,
  restrictByJwt,
}) => {
  const [token] = useGlobal("token");
  const { handleSubmit, register, errors } = useForm();
  const [selectedFieldType, setSelectedFieldType] = useState();
  const [value, setValue] = useState({});
  const [selectedBooleanType, setSelectedBooleanType] = useState({});
  const [selectedBinaryType, setSelectedBinaryType] = useState({});
  const [jwtToken, setJwtToken] = useGlobal("jwtToken");
  const [markedImage, setMarkedImage] = useState();
  const [html, setHtml] = useState();
  const toast = createStandaloneToast();
  const queryClient = useQueryClient();
  const columnTypes = useQuery(APIURLS.getColumnTypes);
  const contentType = useQuery([APIURLS.getContentType], {
    enabled: !!token,
  });
  const { data, isFetching } = useQuery(
    [APIURLS.getTableContentById({ app, table, editDataId }), basejwt],
    {
      enabled: !!token,
    }
  );
  console.log(data?.result);
  //   const [loading, setLoading] = useState(false);
  //   const [success, setSuccess] = useState(false);
  //   const [apiErr, setApiErr] = useState(null);
  //   const queryClient = useQueryClient();
  //   const toast = createStandaloneToast();
  console.log(markedImage, "Hereeeeeee");
  useEffect(() => {
    let token = Object.entries(columns).map(([prop, val]) => {
      console.log(val);
      console.log("here", value, [val?.type], val?.name);
      if (
        val.type === "DATETIME" ||
        val.type === "TIME" ||
        val.type === "DATE"
      ) {
        let obj = value;
        obj[val?.name] = new Date();
        setValue(obj);
      }
      if (val.type === "BOOLEAN") {
        let obj = selectedBooleanType;
        obj[val?.name] = "";

        setSelectedBooleanType(obj);
      }
      if (val.type === "BLOB") {
        let obj = selectedBinaryType;
        obj[val?.name] = "";
        console.log(obj, "setSelectedBinaryType");
        setSelectedBinaryType(obj);
      }
    });
  }, []);

  console.log(selectedBooleanType, "selectedBooleanType");
  const richTextHandler = (event, editor) => {
    const data = editor.getData();
    console.log(data);
    setHtml(data);
  };

  let booleanTypesOptions = [
    {
      value: "true",
      label: "true",
    },
    {
      value: "false",
      label: "false",
    },
    {
      value: 1,
      label: 1,
    },
    {
      value: 0,
      label: 0,
    },
  ];
  let binaryTypesOptions = [
    {
      value: 1,
      label: 1,
    },
    {
      value: 0,
      label: 0,
    },
  ];
  const setValueHandler = (e, name) => {
    let obj = value;
    obj[name] = e;
    setValue(obj);

    console.log(name);
    console.log(obj);
    console.log(e);
  };
  console.log(value);
  let fields = null;
  fields = Object.entries(columns).map(([prop, val]) => {
    console.log(val);
    console.log("here", val.name);

    // if (val.type === "DATETIME" || val.type === "TIME" || val.type === "DATE") {
    //   setValue({ ...value, [val?.type]: val?.name });
    // }
    return (
      <>
        <Label>{val.name}</Label>
        <Box type="relative">
          {val.type === "INTEGER" ||
          val.type === "Integer" ||
          val.type === "INT" ? (
            <Input
              type="number"
              name={val.name}
              color="grey"
              required
              fontSize={3}
              p={2}
              defaultValue={editDataId ? data?.result[val.name] : null}
              width="100%"
              ref={register}
              mb={2}
            />
          ) : val.type === "Enum" ? (
            <>
              {/* <Box
                    style={{
                      marginBottom: "1.5rem",
                      color: "#6E798C",
                      fontSize: "1.25rem",
                      paddingTop: "10px",
                    }}
                  >
                    <Select
                      key={0}
                      // value={edit ? `${columns[edit]?.type}` : selectedFieldType}
                      value={arrayDefaultList.filter((option) =>
                        edit
                          ? option.label === selectedEnumTypeEdit
                          : option.label === selectedEnumType
                      )}
                      onChange={({ value }) =>
                        edit
                          ? setSelectedEnumTypeEdit(value)
                          : setSelectedEnumType(value)
                      }
                      defaultValue={edit ? `${columns[edit]?.default}` : null}
                      required
                      theme={CARD_ELEMENT_OPTIONS}
                      placeholder="Select Type"
                      options={arrayDefaultList}
                    />
                  </Box> */}
            </>
          ) : val.type === "DATE" ? (
            <Box
              style={{
                marginBottom: "1.5rem",
                color: "#6E798C",
                fontSize: "1.25rem",
                paddingTop: "10px",
              }}
            >
              {" "}
              <DateTimePicker
                value={value[val.name]}
                onChange={(e) => setValue({ ...value, [val.name]: e })}
                // parseDate={(str) => new Date(str)}
                format={"y-MM-d"}
              />{" "}
            </Box>
          ) : val.type === "DATETIME" ? (
            <Box
              style={{
                marginBottom: "1.5rem",
                color: "#6E798C",
                fontSize: "1.25rem",
                paddingTop: "10px",
              }}
            >
              {" "}
              <DateTimePicker
                value={value[val.name]}
                onChange={(e) => setValue({ ...value, [val.name]: e })}
                format={"y-MM-dd h:m:s"}
                parseDate={(str) => new Date(str)}
              />{" "}
            </Box>
          ) : val.type === "TIME" ? (
            <Box
              style={{
                marginBottom: "1.5rem",
                color: "#6E798C",
                fontSize: "1.25rem",
                paddingTop: "10px",
              }}
            >
              {" "}
              <DateTimePicker
                value={value[val.name]}
                onChange={(e) => setValue({ ...value, [val.name]: e })}
                // parseDate={(str) => new Date(str)}
                format={"y-MM-dd h:m:s"}
              />{" "}
            </Box>
          ) : val.type === "BIGINT" ? (
            <Box type="relative">
              <Input
                name={val.name}
                color="grey"
                required
                pattern="^[1-9][0-9]*$"
                fontSize={3}
                p={2}
                width="100%"
                // defaultValue={edit ? `${columns[edit]?.default}` : null}
                ref={register}
                mb={2}
              />

              {errors?.name && (
                <Span color="orange" mb={4}>
                  {errors?.name?.message}
                </Span>
              )}
            </Box>
          ) : val.type === "NUMERIC" ? (
            <Box type="relative">
              <Input
                name={val.name}
                color="grey"
                required
                pattern="^[0-9]+$"
                fontSize={3}
                p={2}
                width="100%"
                // defaultValue={edit ? `${columns[edit]?.default}` : null}
                ref={register}
                mb={2}
              />

              {errors?.name && (
                <Span color="orange" mb={4}>
                  {errors?.name?.message}
                </Span>
              )}
            </Box>
          ) : val.type === "DECIMAL" ? (
            <Box type="relative">
              <Input
                name={val.name}
                color="grey"
                required
                pattern="^(\d+\.?\d*|\.\d+)$"
                fontSize={3}
                p={2}
                width="100%"
                // defaultValue={edit ? `${columns[edit]?.default}` : null}
                ref={register}
                mb={2}
              />

              {errors?.name && (
                <Span color="orange" mb={4}>
                  {errors?.name?.message}
                </Span>
              )}
            </Box>
          ) : val.type === "FLOAT" ? (
            <Box type="relative">
              <Input
                name={val.name}
                color="grey"
                required
                pattern="[+-]?([0-9]*[.])?[0-9]+"
                fontSize={3}
                p={2}
                width="100%"
                // defaultValue={edit ? `${columns[edit]?.default}` : null}
                ref={register}
                mb={2}
              />

              {errors?.name && (
                <Span color="orange" mb={4}>
                  {errors?.name?.message}
                </Span>
              )}
            </Box>
          ) : val.type === "BOOLEAN" ? (
            <Box
              style={{
                marginBottom: "1.5rem",
                color: "#6E798C",
                fontSize: "1.25rem",
                paddingTop: "10px",
              }}
            >
              <Select
                key={0}
                // value={selectedBooleanType[val.name]}
                // onChange={(e) => setValue()}
                // value={selectedBooleanType}
                value={booleanTypesOptions.filter(
                  (option) => option.label === selectedBooleanType[val.name]
                )}
                onChange={({ value }) =>
                  setSelectedBooleanType({
                    ...selectedBooleanType,
                    [val.name]: value,
                  })
                }
                required
                theme={CARD_ELEMENT_OPTIONS}
                placeholder="Select Type"
                options={booleanTypesOptions}
              />
            </Box>
          ) : val.type === "BLOB" ? (
            <Box
              style={{
                marginBottom: "1.5rem",
                color: "#6E798C",
                fontSize: "1.25rem",
                paddingTop: "10px",
              }}
            >
              <Select
                key={0}
                value={binaryTypesOptions.filter(
                  (option) => option.label === selectedBinaryType[val.name]
                )}
                onChange={({ value }) =>
                  setSelectedBinaryType({
                    ...selectedBinaryType,
                    [val.name]: value,
                  })
                }
                required
                theme={CARD_ELEMENT_OPTIONS}
                placeholder="Select Type"
                options={binaryTypesOptions}
              />
            </Box>
          ) : val.type === "VARCHAR(123)" ? (
            <Box
              style={{
                marginBottom: "1.5rem",
                color: "#6E798C",
                fontSize: "1.25rem",
                paddingTop: "10px",
              }}
            >
              <div className="App">
                <CKEditor
                  editor={ClassicEditor}
                  onReady={(editor) => {
                    // You can store the "editor" and use when it is needed.
                    console.log("Editor is ready to use!", editor);
                  }}
                  onChange={richTextHandler}

                  // onBlur={(event, editor) => {
                  //   console.log("Blur.", editor);
                  // }}
                  // onFocus={(event, editor) => {
                  //   console.log("Focus.", editor);
                  // }}
                />
              </div>
            </Box>
          ) : val.type === "ImageType" ? (
            <Box
              style={{
                marginBottom: "1.5rem",
                color: "#6E798C",
                fontSize: "1.25rem",
                paddingTop: "10px",
              }}
            >
              <ImageUploadSelect
                setMarkedImage={setMarkedImage}
                markedImage={markedImage}
              />
            </Box>
          ) : (
            <Box type="relative">
              <Input
                name={val.name}
                color="grey"
                required
                fontSize={3}
                p={2}
                width="100%"
                // defaultValue={edit ? `${columns[edit]?.default}` : null}
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
          {/* {errors?.name && (
            <Span color="orange" mb={4}>
              {errors?.name?.message}
            </Span>
          )} */}
        </Box>{" "}
      </>
    );
  });

  function convert(str, type) {
    var mnths = {
        Jan: "01",
        Feb: "02",
        Mar: "03",
        Apr: "04",
        May: "05",
        Jun: "06",
        Jul: "07",
        Aug: "08",
        Sep: "09",
        Oct: "10",
        Nov: "11",
        Dec: "12",
      },
      date = str.split(" ");
    console.log(type, "inside", str);
    if (type === "DATETIME") {
      return [[date[3], mnths[date[1]], date[2]].join("-"), date[4]].join(" ");
    } else if (type === "DATE") {
      return [date[3], mnths[date[1]], date[2]].join("-");
    } else {
      return `${date[4]}`;
    }
  }

  async function handleSignup(params) {
    console.log(params);
    console.log("see1", selectedBooleanType);
    for (let key in columns) {
      console.log(key, columns, columns[key]["type"]);
      if (
        columns[key]["type"] === "INTEGER" ||
        columns[key]["type"] === "Integer" ||
        columns[key]["type"] === "INT" ||
        columns[key]["type"] === "BIGINT" ||
        columns[key]["type"] === "NUMERIC"
      ) {
        let name = columns[key]["name"];
        params[name] = parseInt(params[name]);
      } else if (
        columns[key]["type"] === "DECIMAL" ||
        columns[key]["type"] === "FLOAT"
      ) {
        let name = columns[key]["name"];
        params[name] = parseFloat(params[name]);
      } else if (columns[key]["type"] === "TIME") {
        let name = columns[key]["name"];
        params[name] = convert(`${value[name]}`, columns[key]["type"]);
      } else if (columns[key]["type"] === "DATETIME") {
        let name = columns[key]["name"];
        console.log("def1", value.name);
        params[name] = convert(`${value[name]}`, columns[key]["type"]);
      } else if (columns[key]["type"] === "DATE") {
        let name = columns[key]["name"];
        params[name] = convert(`${value[name]}`, columns[key]["type"]);
      } else if (columns[key]["type"] === "BOOLEAN") {
        let name = columns[key]["name"];
        params[name] =
          selectedBooleanType[name] === "true"
            ? true
            : selectedBooleanType[name] === "false"
            ? false
            : selectedBooleanType[name];
      } else if (columns[key]["type"] === "BLOB") {
        let name = columns[key]["name"];
        params[name] = selectedBinaryType[name];
      } else if (columns[key]["type"] === "VARCHAR(123)") {
        let name = columns[key]["name"];
        params[name] = html;
      } else if (columns[key]["type"] === "ImageType") {
        let name = columns[key]["name"];
        params[name] = markedImage;
      }
    }
    console.log(params, value);
    try {
      let { data } =
        basejwt && restrictByJwt && editDataId
          ? await ApiJwt.put(
              APIURLS.getTableContentById({ app, table, editDataId }),
              {
                ...params,
              }
            )
          : basejwt && editDataId
          ? await ApiJwt.put(
              APIURLS.getTableContentById({ app, table, editDataId }),
              {
                ...params,
              }
            )
          : basejwt && restrictByJwt
          ? await ApiJwt.post(APIURLS.getTableContent({ app, table }), {
              ...params,
            })
          : basejwt && basejwt.base_table === table
          ? await ApiApp.post(APIURLS.postRegisterTableData({ app, table }), {
              ...params,
            })
          : editDataId
          ? await ApiApp.put(
              APIURLS.getTableContentById({ app, table, editDataId }),
              {
                ...params,
              }
            )
          : await ApiApp.post(APIURLS.getTableContent({ app, table }), {
              ...params,
            });
      if (basejwt) {
        let jwtToken = data?.access_token;
        localStorage.setItem("jwtToken", jwtToken);
        setJwtHeader(jwtToken);
        setJwtToken(jwtToken);
        await queryClient.refetchQueries([
          APIURLS.getTableContent({ app, table }),
          "jwt_info",
        ]);
      } else {
        await queryClient.refetchQueries([
          APIURLS.getTableContent({ app, table }),
        ]);
      }
      console.log("see2", queryClient.isFetching());
      toast({
        title: "Data Added.",
        description: data?.result,
        status: "success",
        duration: 9000,
        isClosable: false,
      });
      setMarkedImage();
      onClose();
      console.log("there", data);
    } catch ({ response }) {
      toast({
        title: "An error occurred.",
        description: response?.data?.result,
        status: "error",
        duration: 9000,
        isClosable: true,
      });
      console.log(response);
    }
  }

  return (
    <>
      <Modal isOpen={isOpen} onClose={onClose} size={"xl"}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>
            {" "}
            <Label>Create Field </Label>
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Box type="row" justifyContent="center" m={6}>
              <form
                onSubmit={handleSubmit(handleSignup)}
                style={{ width: "35vw" }}
              >
                {fields}
                <Button mt={4} width="100%" fontSize={18} type="submit">
                  {"Create"}
                </Button>
              </form>
            </Box>
          </ModalBody>
        </ModalContent>
      </Modal>
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

export default AppTableData;
