import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { useGlobal } from "reactn";
import { NavLink } from "react-router-dom";
import { Tooltip } from "@chakra-ui/react";
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
  Para,
  Label,
} from "../../styles";
import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableCaption,
} from "@chakra-ui/react";
import { Switch } from "@chakra-ui/react";
import { Icon } from "@chakra-ui/react";
import { FaEdit } from "react-icons/fa";
import { AiOutlineDelete } from "react-icons/ai";
import { BsPlusCircleFill } from "react-icons/bs";
import DateTimePicker from "react-datetime-picker";
import { useIsFetching } from "react-query";
import { useQuery, useQueryClient } from "react-query";
import { useToast, createStandaloneToast } from "@chakra-ui/react";
import Api, { setHeader, APIURLS } from "../../Api";
import Select from "react-select";
import ClipLoader from "react-spinners/ClipLoader";
import { TiRssOutline } from "react-icons/ti";

const CreateTable = ({
  step,
  connectionSelected,
  appName,
  onCloseHandler,
  columnsData,
  basejwtPresent,
  setStep,
  setNewStep,
  table,
  tableName,
}) => {
  //   const [token] = useGlobal("token");
  const { handleSubmit, register, errors, reset } = useForm();
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [value, setValue] = useState(new Date());
  const [editValue, setEditValue] = useState(new Date());
  const [selectedFieldType, setSelectedFieldType] = useState();
  const [selectedNullableType, setSelectedNullableType] = useState();
  const [selectedBooleanType, setSelectedBooleanType] = useState();
  const [selectedBinaryType, setSelectedBinaryType] = useState();
  const [selectedUniqueType, setSelectedUniqueType] = useState();
  const [selectedFieldTypeEdit, setSelectedFieldTypeEdit] = useState();
  const [selectedNullableTypeEdit, setSelectedNullableTypeEdit] = useState();
  const [selectedBooleanTypeEdit, setSelectedBooleanTypeEdit] = useState();
  const [selectedBinaryTypeEdit, setSelectedBinaryTypeEdit] = useState();
  const [selectedUniqueTypeEdit, setSelectedUniqueTypeEdit] = useState();
  const [selectedEnumTypeEdit, setSelectedEnumTypeEdit] = useState();
  const [selectedEnumType, setSelectedEnumType] = useState();
  const [columns, setColumns] = useState(columnsData || []);
  const [arrayDefault, setArrayDefault] = useState();
  const [arrayDefaultList, setArrayDefaultList] = useState([]);
  // const [tableName, setTableName] = useState(table || null);
  const [edit, setEdit] = useState();
  const [foreignKeyOptions, setForeignKeyOptions] = useState();
  const [foreignKeyTable, setForeignKeyTable] = useState();
  const [foreignKeyColumn, setForeignKeyColumn] = useState();
  const [foreignKeyCheck, setForeignKeyCheck] = useState(false);
  const [defaultValueCheck, setDefaultValueCheck] = useState(false);
  const [relationCheck, setRelationCheck] = useState(false);
  const [relationshipType, setRelationshipType] = useState();
  const [relationOptions, setRelationOptions] = useState();
  const [relatedTable, setRelatedTable] = useState();
  const [relatedField, setRelatedField] = useState();
  const [baseJWT, setbaseJWT] = useState(false);
  const [restByJWT, setRestByJWT] = useState(false);
  const [filterOpt, setFilterOpt] = useState([]);
  //   const queryClient = useQueryClient();
  const toast = createStandaloneToast();
  const queryClient = useQueryClient();
  const columnTypes = useQuery(APIURLS.getColumnTypes);
  const isFetching = useIsFetching();

  async function foreignkeyfn() {
    try {
      let { data } = await Api.post(APIURLS.getForeignkey, {
        app_name: appName,
        type: selectedFieldType,
      });
      setForeignKeyOptions(data);
    } catch ({ response }) {
      console.log(response);
    }
  }

  async function relationshipfn(value) {
    // let relationCheckValue = relationCheck;
    // setRelationCheck(!relationCheckValue);
    try {
      let { data } = await Api.post(APIURLS.getForeignkey, {
        app_name: appName,
        type: value || selectedFieldType,
      });
      setRelationOptions(data);
    } catch ({ response }) {
      console.log(response);
    }
  }

  let relationTable = [];
  if (relationOptions) {
    {
      Object.entries(relationOptions).map(([prop, val]) => {
        // console.log(val);
        return relationTable.push({ value: prop, label: prop });
      });
    }
  }
  let relationColumns = [];
  if (relatedTable) {
    // console.log(relationOptions[relationTable]);
    for (let key in relationOptions[relatedTable]) {
      console.log(relationOptions[relatedTable][key]);
      relationColumns.push({
        value: relationOptions[relatedTable][key],
        label: relationOptions[relatedTable][key],
      });
    }
  }

  const deleteHandler = (index) => {
    let columnArray = [...columns];
    columnArray.splice(index, 1);
    setColumns(columnArray);
    setEdit();
  };
  const editHandler = (index) => {
    setEdit(index);
    setSelectedFieldTypeEdit(columns[index].type);
    setSelectedNullableTypeEdit(columns[index].nullable);
    setSelectedBooleanTypeEdit(columns[index].default);
    setSelectedUniqueTypeEdit(columns[index].unique);
    setSelectedEnumTypeEdit(columns[index].default);
    setArrayDefaultList(columns[index].enum);
    setValue(new Date());
    if (columns[index].default) {
      setDefaultValueCheck(true);
    }
  };
  console.log("CHECKKEY", value);

  function convert(str) {
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
    console.log(selectedFieldType, "inside");
    if ((selectedFieldType || selectedFieldTypeEdit) === "DateTime") {
      return [[date[3], mnths[date[1]], date[2]].join("-"), date[4]].join(" ");
    } else if ((selectedFieldType || selectedFieldTypeEdit) === "Date") {
      return [date[3], mnths[date[1]], date[2]].join("-");
    } else {
      return `${date[4]}`;
    }
  }

  const timeChangeHandler = (str) => {
    // let date = str.split(" ");
    // setValue(date[4]);
    console.log(str);
  };
  console.log("valueeeeee", value, selectedFieldType);
  async function handleSignup(params) {
    console.log(
      "inttt1",
      selectedFieldType,
      (selectedFieldType || selectedFieldTypeEdit) ===
        ("INTEGER" || "INT" || "integer" || "BigInteger")
    );
    let def;
    if (
      (selectedFieldType || selectedFieldTypeEdit) === "INTEGER" ||
      (selectedFieldType || selectedFieldTypeEdit) === "INT" ||
      (selectedFieldType || selectedFieldTypeEdit) === "Integer" ||
      (selectedFieldType || selectedFieldTypeEdit) === "BigInteger" ||
      (selectedFieldType || selectedFieldTypeEdit) === "Numeric"
    ) {
      def = parseInt(params.default);
      console.log("inttt", def);
    } else if (
      (selectedFieldType || selectedFieldTypeEdit) === "Float" ||
      (selectedFieldType || selectedFieldTypeEdit) === "DECIMAL"
    ) {
      def = parseFloat(params.default);
    } else if ((selectedFieldType || selectedFieldTypeEdit) === "Enum") {
      def = edit ? selectedEnumTypeEdit : selectedEnumType;
    } else if ((selectedFieldType || selectedFieldTypeEdit) === "Time") {
      def = convert(`${value}`);
    } else if ((selectedFieldType || selectedFieldTypeEdit) === "DateTime") {
      console.log("def1", value);
      def = convert(`${value}`);
    } else if ((selectedFieldType || selectedFieldTypeEdit) === "Date") {
      def = convert(`${value}`);
    } else if (selectedFieldType === "Boolean") {
      def = selectedBooleanType;
    } else if (selectedFieldTypeEdit === "Boolean") {
      def = selectedBooleanTypeEdit;
    } else if (selectedFieldType === "Binary") {
      def = selectedBinaryType;
    } else if (selectedFieldTypeEdit === "Binary") {
      def = selectedBinaryTypeEdit;
    } else {
      def = params.default;
    }

    console.log("def2", def);
    let column =
      (selectedFieldType || selectedFieldTypeEdit) === "Enum"
        ? {
            name: params.name,
            type: edit ? selectedFieldTypeEdit : selectedFieldType,
            nullable: edit ? selectedNullableTypeEdit : selectedNullableType,
            unique: edit ? selectedUniqueTypeEdit : selectedUniqueType,
            ...(defaultValueCheck && { default: def }),
            enum: arrayDefaultList,
          }
        : step
        ? {
            name: params.name,
            type: edit ? selectedFieldTypeEdit : selectedFieldType,
            nullable: edit ? selectedNullableTypeEdit : selectedNullableType,
            unique: edit ? selectedUniqueTypeEdit : selectedUniqueType,
            ...(defaultValueCheck && { default: def }),
          }
        : foreignkeyColumns.length != 0 &&
          foreignKeyCheck &&
          relationCheck &&
          relationColumns
        ? {
            name: params.name,
            type: edit ? selectedFieldTypeEdit : selectedFieldType,
            nullable: edit ? selectedNullableTypeEdit : selectedNullableType,
            unique: edit ? selectedUniqueTypeEdit : selectedUniqueType,
            ...(defaultValueCheck && { default: def }),
            foreign_key: `${foreignKeyTable}.${foreignKeyColumn}`,
            relationship: {
              relationship_type: relationshipType,
              related_field: relatedField,
              related_table: relatedTable,
            },
          }
        : foreignkeyColumns.length != 0 && foreignKeyCheck
        ? {
            name: params.name,
            type: edit ? selectedFieldTypeEdit : selectedFieldType,
            nullable: edit ? selectedNullableTypeEdit : selectedNullableType,
            unique: edit ? selectedUniqueTypeEdit : selectedUniqueType,
            ...(defaultValueCheck && { default: def }),
            foreign_key: `${foreignKeyTable}.${foreignKeyColumn}`,
          }
        : relationCheck && relationColumns.length != 0
        ? {
            name: params.name,
            type: edit ? selectedFieldTypeEdit : selectedFieldType,
            nullable: edit ? selectedNullableTypeEdit : selectedNullableType,
            unique: edit ? selectedUniqueTypeEdit : selectedUniqueType,
            ...(defaultValueCheck && { default: def }),
            relationship: {
              relationship_type: relationshipType,
              related_field: relatedField,
              related_table: relatedTable,
            },
          }
        : {
            name: params.name,
            type: edit ? selectedFieldTypeEdit : selectedFieldType,
            nullable: edit ? selectedNullableTypeEdit : selectedNullableType,
            unique: edit ? selectedUniqueTypeEdit : selectedUniqueType,
            ...(defaultValueCheck && { default: def }),
          };
    let columnArray = [...columns];
    // setTableName(tableName);
    if (edit) {
      columnArray[edit] = column;
      setEdit();
    } else {
      columnArray.push(column);
    }

    setColumns(columnArray);
    console.log("columnArray", columnArray);
    setSelectedFieldType();
    setSelectedNullableType();
    setSelectedBooleanType();
    setSelectedBinaryType();
    setSelectedUniqueType();
    setArrayDefault("");
    setArrayDefaultList([]);
    setRelationCheck(false);
    setForeignKeyCheck(false);
    setDefaultValueCheck(false);
    setRelationshipType();
    setRelatedField();
    setRelatedTable();

    // setValue(new Date());
    reset();
  }
  console.log("setColumns", columns);

  async function createTableRequest() {
    setLoading(true);
    try {
      let { data } =
        baseJWT && filterOpt.length !== 0 && columnsData && tableName
          ? await Api.put(APIURLS.getContentType, {
              table_name: tableName,
              app_name: appName,
              // restrict_by_jwt: false,,
              columns: columns,
              base_jwt: true,
              filter_keys: filterOpt,
              // filter_keys: ["1"],
            })
          : restByJWT && columnsData && tableName
          ? await Api.put(APIURLS.getContentType, {
              table_name: tableName,
              app_name: appName,
              restrict_by_jwt: true,
              columns: columns,
            })
          : columnsData && tableName
          ? await Api.put(APIURLS.getContentType, {
              table_name: tableName,
              app_name: appName,
              restrict_by_jwt: false,
              columns: columns,
            })
          : baseJWT && filterOpt.length !== 0
          ? await Api.post(APIURLS.getContentType, {
              table_name: tableName,
              app_name: appName,
              // restrict_by_jwt: false,,
              columns: columns,
              base_jwt: true,
              filter_keys: filterOpt,
              // filter_keys: ["1"],
            })
          : restByJWT
          ? await Api.post(APIURLS.getContentType, {
              table_name: tableName,
              app_name: appName,
              restrict_by_jwt: true,
              columns: columns,
            })
          : await Api.post(APIURLS.getContentType, {
              table_name: tableName,
              app_name: appName,
              restrict_by_jwt: false,
              columns: columns,
            });
      await setTimeout(() => {
        queryClient.refetchQueries(APIURLS.getContentType);

        toast({
          title: "App created successfully.",
          description: data?.result,
          status: "success",
          duration: 9000,
          isClosable: false,
        });
        // console.log("heretimeloop", queryClient.isFetching());
        // setOnLoading(true);

        if (step) {
          setStep(5);
        }
        if (!step) {
          setNewStep(3);
        }

        // onCloseHandler();
      }, 20000);

      // onClose();
      console.log("data", data);
    } catch ({ response }) {
      toast({
        title: "An error occurred.",
        description: response?.data?.result,
        status: "error",
        duration: 9000,
        isClosable: true,
      });
      console.log(response);
      //   setApiErr(response?.data?.message);
      setLoading(false);
      // onCloseHandler();
    }
    // setTableName(params.name);
  }

  let filterOptions = [];
  if (columns.length !== 0) {
    {
      Object.entries(columns).map(([prop, val]) => {
        return val.nullable === "false" && val.unique === "true"
          ? filterOptions.push({ value: val.name, label: val.name })
          : null;
      });
    }
  }
  let nullableTypesOptions = [
    {
      value: "true",
      label: "true",
    },
    {
      value: "false",
      label: "false",
    },
  ];
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
  let uniqueTypesOptions = [
    {
      value: "true",
      label: "true",
    },
    {
      value: "false",
      label: "false",
    },
  ];
  console.log("selectedUniqueType", selectedUniqueType);
  let columnTypesOptions = [];
  if (columnTypes?.data?.result) {
    {
      Object.entries(columnTypes?.data?.result).map(([prop, val]) => {
        // console.log(val);
        if (val === "String") {
          return columnTypesOptions.push({
            value: "String(123)",
            label: "String(123)",
          });
        }
        return columnTypesOptions.push({ value: val, label: val });
      });
    }
  }
  let foreignkeyTable = [];
  if (foreignKeyOptions) {
    {
      Object.entries(foreignKeyOptions).map(([prop, val]) => {
        // console.log(val);
        return foreignkeyTable.push({ value: prop, label: prop });
      });
    }
  }
  let foreignkeyColumns = [];
  if (foreignKeyTable) {
    console.log(foreignKeyOptions[foreignKeyTable]);
    for (let key in foreignKeyOptions[foreignKeyTable]) {
      console.log(foreignKeyOptions[foreignKeyTable][key]);
      foreignkeyColumns.push({
        value: foreignKeyOptions[foreignKeyTable][key],
        label: foreignKeyOptions[foreignKeyTable][key],
      });
    }
  }

  console.log("foreignkeyTable", foreignkeyTable);
  console.log("foreignKeyOptions", foreignKeyOptions);
  console.log("foreignkeyColumns", foreignkeyColumns);
  let contentTypeApps = Object.entries(columns).map(([prop, val]) => {
    console.log(val);
    return (
      <Tr style={{ color: "#4A5568" }}>
        <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>{val.name}</Td>
        <Td
          style={{
            color: "#4A5568",
            borderColor: "#EDF2F7",
            textAlign: "center",
          }}
        >
          {val.type}
        </Td>
        <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
          {val.unique}
        </Td>
        <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
          {val.nullable}
        </Td>
        <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
          {val.default}
        </Td>
        {/* <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
          {val.foreign_key}
        </Td> */}
        <Td
          style={{
            color: "#4A5568",
            borderColor: "#EDF2F7",
            textAlign: "right",
          }}
        >
          {
            // <i onClick={() => {setEditDbConnection(key) &&onOpen }}>
            <i>
              <Tooltip label="Edit Column" bg="#8071b399" placement="top">
                <spam>
                  <Icon
                    as={FaEdit}
                    w={5}
                    h={5}
                    color={"#4B0082"}
                    onClick={() => editHandler(prop)}
                  />{" "}
                </spam>
              </Tooltip>
              <Tooltip label="Delete Column" bg="#8071b399" placement="bottom">
                <spam>
                  <Icon
                    as={AiOutlineDelete}
                    w={5}
                    h={5}
                    color={"red"}
                    onClick={() => deleteHandler(prop)}
                  />{" "}
                </spam>
              </Tooltip>
            </i>
          }
        </Td>
      </Tr>
    );
  });

  const setbaseJWTHandler = (e) => {
    // let baseJWTvalue = !baseJWT;
    console.log("Valuejwt", e);
    // setbaseJWT(baseJWTvalue);
  };

  console.log("JWT", baseJWT);

  const handleMultiChange = (option) => {
    console.log("jndjs", option);
    let array = [];
    for (let key in option) {
      console.log(option);
      array.push(option[key].value);
    }
    console.log(array);
    setFilterOpt(array);
  };

  // const handleEnumChange = (option) => {
  //   console.log("jndjs", option);
  //   let array = [];
  //   for (let key in option) {
  //     console.log(option);
  //     array.push(option[key].value);
  //   }
  //   console.log(array);
  //   setFilterOpt(array);
  // };

  const addArrayDefaultHandler = () => {
    let newEnumList = arrayDefaultList;
    let newObj = {
      value: arrayDefault,
      label: arrayDefault,
    };
    newEnumList.push(newObj);

    setArrayDefaultList(newEnumList);
    setArrayDefault("");
    // setUserEmail();
  };
  console.log(arrayDefaultList);
  const removeArrayDefaultHandler = (index) => {
    let newArrayDefaultList = [];
    for (let key in arrayDefaultList) {
      console.log(arrayDefaultList[key], "key", key);
      if (key != index) {
        newArrayDefaultList.push(arrayDefaultList[key]);
      }
    }

    // console.log(newArrayDefaultList);
    setArrayDefaultList(newArrayDefaultList);
  };
  const relationTypeHandler = (value) => {
    console.log("INSIDDDEEEEEEEEEEEEE");
    setRelationshipType(value);

    if (relationCheck && (value === "one-one" || value === "one-many")) {
      setSelectedUniqueType("true");
    } else if (
      relationCheck &&
      (value === "many-one" || value === "many-many")
    ) {
      setSelectedUniqueType("false");
    }
  };
  const fieldTypeHandler = (value) => {
    edit ? setSelectedFieldTypeEdit(value) : setSelectedFieldType(value);
    relationshipfn(value);
  };

  console.log("arrayDefaultList", arrayDefaultList);
  return loading || isFetching > 0 ? (
    <Box width="100%" height="100vh">
      <Box type={step ? "loader" : "loaderCentered"}>
        <ClipLoader color={"#ffffff"} size={55} />
      </Box>
    </Box>
  ) : (
    <>
      {step ? (
        <Box type="heading" textAlign="center">
          <Span type="heading">Create Table for your App</Span>
        </Box>
      ) : null}
      <Box
        display="grid"
        gridTemplateColumns={"1fr 1fr"}
        // mb={8}
        // gridGap={4}
        // style={{ margin: "30px", marginLeft: "70px", marginRight: "70px" }}
      >
        {/* <Box display="grid" gridTemplateColumns="1fr" gridGap={8} height="100%"> */}

        <Box type="row" flexDirection="column" justifyContent="center">
          {/* <Box m={6} textAlign="center">
            <Span fontSize={6} mb={2}>
              Create A Collection type
            </Span>
           
          </Box> */}
          <Box type="row" justifyContent="center" m={6}>
            <form
              onSubmit={handleSubmit(handleSignup)}
              style={{ width: "28vw" }}
            >
              {/* <Box type="relative">
                <Label>Table Name</Label>
                <Input
                  name="tableName"
                  color="grey"
                  required
                  defaultValue={tableName}
                  pattern="^([a-z]+[0-9_]*)*$"
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
              </Box> */}
              <Label>Select Field type</Label>
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
                  // value={edit ? `${columns[edit]?.type}` : selectedFieldType}
                  value={columnTypesOptions.filter((option) =>
                    edit
                      ? option.label === selectedFieldTypeEdit
                      : option.label === selectedFieldType
                  )}
                  onChange={({ value }) => fieldTypeHandler(value)}
                  required
                  theme={CARD_ELEMENT_OPTIONS}
                  placeholder="Select Type"
                  options={columnTypesOptions}
                />
              </Box>
              <Label>Column Name </Label>
              <Box type="relative">
                <Input
                  name="name"
                  color="grey"
                  required
                  fontSize={3}
                  p={2}
                  width="100%"
                  pattern="^([a-z]+[0-9_]*)*$"
                  defaultValue={edit ? `${columns[edit]?.name}` : null}
                  ref={register}
                  mb={2}
                />

                {errors?.name && (
                  <Span color="orange" mb={4}>
                    {errors?.name?.message}
                  </Span>
                )}
              </Box>
              <Label>Nullable</Label>
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
                  // value={edit ? `${columns[edit]?.type}` : selectedFieldType}
                  value={nullableTypesOptions.filter((option) =>
                    edit
                      ? option.label === selectedNullableTypeEdit
                      : option.label === selectedNullableType
                  )}
                  onChange={({ value }) =>
                    edit
                      ? setSelectedNullableTypeEdit(value)
                      : setSelectedNullableType(value)
                  }
                  required
                  theme={CARD_ELEMENT_OPTIONS}
                  placeholder="Select Type"
                  options={nullableTypesOptions}
                />
              </Box>
              <Label>Unique</Label>
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
                  // value={edit ? `${columns[edit]?.type}` : selectedFieldType}
                  // menuIsOpen={false}
                  value={
                    relationCheck
                      ? {
                          value: selectedUniqueType,
                          label: selectedUniqueType,
                        }
                      : uniqueTypesOptions.filter((option) =>
                          edit
                            ? option.label === selectedUniqueTypeEdit
                            : option.label === selectedUniqueType
                        )
                  }
                  onChange={({ value }) =>
                    relationCheck
                      ? setSelectedUniqueType(selectedUniqueType)
                      : edit
                      ? setSelectedUniqueTypeEdit(value)
                      : setSelectedUniqueType(value)
                  }
                  required
                  theme={CARD_ELEMENT_OPTIONS}
                  placeholder="Select Type"
                  options={uniqueTypesOptions}
                />
                {relationCheck ? (
                  <Para>
                    If you are adding Relationship, the unique constain will be
                    True if relation is 'One to One' or 'One to Many' and False
                    if relation is 'Many to One' or 'Many to Many'.
                  </Para>
                ) : null}
              </Box>{" "}
              <Box type="row" justifyContent="start" mb={3}>
                <Tooltip
                  label={
                    !defaultValueCheck
                      ? "Click to add default value"
                      : "Click to not add default value"
                  }
                  bg="#8071b399"
                  placement="top"
                >
                  <spam>
                    <Switch
                      size="lg"
                      style={{ background: "rgb(241 218 249)" }}
                      // onClick={foreignkeyfn}
                      isChecked={defaultValueCheck}
                      onChange={(e) => setDefaultValueCheck(e.target.checked)}
                    />
                  </spam>
                </Tooltip>
                <Para ml={6}> Do you want to add Default Value</Para>{" "}
              </Box>
              <Label>Default</Label>
              {(selectedFieldType || columns[edit]?.type) === "Enum" ? (
                <>
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
                      theme={CARD_ELEMENT_OPTIONS}
                      placeholder="Select Type"
                      options={arrayDefaultList}
                    />
                  </Box>
                </>
              ) : (selectedFieldType || columns[edit]?.type) === "Date" ? (
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
                    value={value}
                    onChange={setValue}
                    // parseDate={(str) => new Date(str)}
                    format={"y-MM-d"}
                  />{" "}
                </Box>
              ) : (selectedFieldType || columns[edit]?.type) === "DateTime" ? (
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
                    value={value}
                    onChange={setValue}
                    format={"y-MM-dd h:m:s"}
                    parseDate={(str) => new Date(str)}
                  />{" "}
                </Box>
              ) : (selectedFieldType || columns[edit]?.type) === "Time" ? (
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
                    value={value}
                    onChange={setValue}
                    // parseDate={(str) => new Date(str)}
                    format={"y-MM-dd h:m:s"}
                  />{" "}
                </Box>
              ) : (selectedFieldType || columns[edit]?.type) ===
                "BigInteger" ? (
                <Box type="relative">
                  <Input
                    name="default"
                    color="grey"
                    pattern="^[1-9][0-9]*$"
                    fontSize={3}
                    p={2}
                    width="100%"
                    defaultValue={edit ? `${columns[edit]?.default}` : null}
                    ref={register}
                    mb={2}
                  />

                  {errors?.name && (
                    <Span color="orange" mb={4}>
                      {errors?.name?.message}
                    </Span>
                  )}
                </Box>
              ) : (selectedFieldType || columns[edit]?.type) === "Numeric" ? (
                <Box type="relative">
                  <Input
                    name="default"
                    color="grey"
                    pattern="^[0-9]+$"
                    fontSize={3}
                    p={2}
                    width="100%"
                    defaultValue={edit ? `${columns[edit]?.default}` : null}
                    ref={register}
                    mb={2}
                  />

                  {errors?.name && (
                    <Span color="orange" mb={4}>
                      {errors?.name?.message}
                    </Span>
                  )}
                </Box>
              ) : (selectedFieldType || columns[edit]?.type) === "Float" ? (
                <Box type="relative">
                  <Input
                    name="default"
                    color="grey"
                    pattern="[+-]?([0-9]*[.])?[0-9]+"
                    fontSize={3}
                    p={2}
                    width="100%"
                    defaultValue={edit ? `${columns[edit]?.default}` : null}
                    ref={register}
                    mb={2}
                  />

                  {errors?.name && (
                    <Span color="orange" mb={4}>
                      {errors?.name?.message}
                    </Span>
                  )}
                </Box>
              ) : (selectedFieldType || columns[edit]?.type) === "DECIMAL" ? (
                <Box type="relative">
                  <Input
                    name="default"
                    color="grey"
                    pattern="^(\d+\.?\d*|\.\d+)$"
                    fontSize={3}
                    p={2}
                    width="100%"
                    defaultValue={edit ? `${columns[edit]?.default}` : null}
                    ref={register}
                    mb={2}
                  />

                  {errors?.name && (
                    <Span color="orange" mb={4}>
                      {errors?.name?.message}
                    </Span>
                  )}
                </Box>
              ) : (selectedFieldType || columns[edit]?.type) === "Boolean" ? (
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
                    // value={edit ? `${columns[edit]?.type}` : selectedFieldType}
                    value={booleanTypesOptions.filter((option) =>
                      edit
                        ? option.label === selectedBooleanTypeEdit
                        : option.label === selectedBooleanType
                    )}
                    onChange={({ value }) =>
                      edit
                        ? setSelectedBooleanTypeEdit(value)
                        : setSelectedBooleanType(value)
                    }
                    theme={CARD_ELEMENT_OPTIONS}
                    placeholder="Select Type"
                    options={booleanTypesOptions}
                  />
                </Box>
              ) : (selectedFieldType || columns[edit]?.type) === "Binary" ? (
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
                    // value={edit ? `${columns[edit]?.type}` : selectedFieldType}
                    value={binaryTypesOptions.filter((option) =>
                      edit
                        ? option.label === selectedBinaryTypeEdit
                        : option.label === selectedBinaryType
                    )}
                    onChange={({ value }) =>
                      edit
                        ? setSelectedBinaryTypeEdit(value)
                        : setSelectedBinaryType(value)
                    }
                    theme={CARD_ELEMENT_OPTIONS}
                    placeholder="Select Type"
                    options={binaryTypesOptions}
                  />
                </Box>
              ) : (
                <Box type="relative">
                  <Input
                    name="default"
                    color="grey"
                    fontSize={3}
                    p={2}
                    width="100%"
                    defaultValue={
                      edit && columns[edit]?.default
                        ? `${columns[edit]?.default}`
                        : null
                    }
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
              {(selectedFieldType || columns[edit]?.type) === "Enum" ? (
                <>
                  {" "}
                  <Label>Add Values to Enum</Label>
                  <Box type="relative" style={{ display: "flex" }}>
                    <Box type="row" width={"85%"}>
                      <Input
                        name={"default"}
                        color="grey"
                        fontSize={3}
                        p={2}
                        //  defaultValue={edit ? `${columns[edit]?.default}` : null}
                        width="100%"
                        ref={register}
                        mb={2}
                        value={arrayDefault}
                        onChange={(e) => setArrayDefault(e.target.value)}
                      />

                      {errors?.name && (
                        <Span color="orange" mb={4}>
                          {errors?.name?.message}
                        </Span>
                      )}
                    </Box>
                    <Box type="row" justifyContent="flex-start">
                      {" "}
                      <Icon
                        as={BsPlusCircleFill}
                        w={"1.5rem"}
                        h={"3.5rem"}
                        color={"rgb(56 46 108 / 92%)"}
                        style={{ marginBottom: "5px", marginLeft: "20px" }}
                        onClick={addArrayDefaultHandler}
                      />{" "}
                    </Box>
                  </Box>
                  {edit
                    ? columns[edit]?.enum.map((key, index) => {
                        return (
                          <Box
                            type="row"
                            justifyContent="space-between"
                            m={4}
                            p={2}
                            style={{
                              height: "45px",
                              border: "2px solid #8071b3",
                              borderRadius: "5px",
                              marginLeft: "0",
                            }}
                          >
                            <Box type="row" justifyContent="flex-start">
                              <Para> {key["value"]}</Para>
                            </Box>
                            <Box>
                              <Icon
                                as={AiOutlineDelete}
                                w={"1.5rem"}
                                h={"1.5rem"}
                                color={"red"}
                                onClick={() => removeArrayDefaultHandler(index)}
                              />
                            </Box>
                          </Box>
                        );
                      })
                    : arrayDefaultList.map((key, index) => {
                        return (
                          <Box
                            type="row"
                            justifyContent="space-between"
                            m={4}
                            p={2}
                            style={{
                              height: "45px",
                              border: "2px solid #8071b3",
                              borderRadius: "5px",
                              marginLeft: "0",
                            }}
                          >
                            <Box type="row" justifyContent="flex-start">
                              <Para> {key["value"]}</Para>
                            </Box>
                            <Box>
                              <Icon
                                as={AiOutlineDelete}
                                w={"1.5rem"}
                                h={"1.5rem"}
                                color={"red"}
                                onClick={() => removeArrayDefaultHandler(index)}
                              />
                            </Box>
                          </Box>
                        );
                      })}
                </>
              ) : null}
              <br />
              {!step ? (
                <Box type="row" justifyContent="start" mb={3}>
                  <Tooltip
                    label={
                      !foreignKeyCheck
                        ? "Click to add foreign key"
                        : "Click to not add foreign key"
                    }
                    bg="#8071b399"
                    placement="top"
                  >
                    <spam>
                      <Switch
                        size="lg"
                        style={{ background: "rgb(241 218 249)" }}
                        onClick={foreignkeyfn}
                        isChecked={foreignKeyCheck}
                        onChange={(e) => setForeignKeyCheck(e.target.checked)}
                      />
                    </spam>
                  </Tooltip>
                  <Para ml={6}> Do you want to add foreign key</Para>{" "}
                </Box>
              ) : null}
              {!step ? <Label>Select Foreign Key</Label> : null}
              {!step ? (
                <Box
                  style={{
                    marginBottom: "1.5rem",
                    color: "#6E798C",
                    fontSize: "1.25rem",
                    paddingTop: "10px",
                  }}
                >
                  <Select
                    key={1}
                    // value={edit ? `${columns[edit]?.type}` : selectedFieldType}
                    // value={columnTypesOptions.filter((option) =>
                    //   edit
                    //     ? option.label === selectedFieldTypeEdit
                    //     : option.label === selectedFieldType
                    // )}
                    onChange={({ value }) => setForeignKeyTable(value)}
                    required
                    theme={CARD_ELEMENT_OPTIONS}
                    placeholder="Select Table"
                    options={foreignkeyTable}
                  />
                </Box>
              ) : null}
              {!step ? (
                <Box
                  style={{
                    marginBottom: "1.5rem",
                    color: "#6E798C",
                    fontSize: "1.25rem",
                  }}
                >
                  <Select
                    key={2}
                    onChange={({ value }) => setForeignKeyColumn(value)}
                    required
                    theme={CARD_ELEMENT_OPTIONS}
                    placeholder="Select Field"
                    options={foreignkeyColumns}
                  />
                </Box>
              ) : null}
              {!step ? (
                <Box type="row" justifyContent="start" mb={3}>
                  <Tooltip
                    label={
                      !relationCheck
                        ? "Click to add Relations"
                        : "Click to not add Relations"
                    }
                    bg="#8071b399"
                    placement="top"
                  >
                    <spam>
                      <Switch
                        size="lg"
                        style={{ background: "rgb(241 218 249)" }}
                        onClick={() => relationshipfn()}
                        isChecked={relationCheck}
                        onChange={(e) => setRelationCheck(e.target.checked)}
                      />
                    </spam>
                  </Tooltip>
                  <Para ml={6}> Do you want to add Relations</Para>
                </Box>
              ) : null}
              {!step ? <Label>Relations</Label> : null}
              {!step ? (
                <Box
                  style={{
                    marginBottom: "1.5rem",
                    color: "#6E798C",
                    fontSize: "1.25rem",
                    paddingTop: "10px",
                  }}
                >
                  <Select
                    key={1}
                    value={
                      relationshipType
                        ? {
                            value: relationshipType,
                            label: relationshipType,
                          }
                        : null
                    }
                    onChange={({ value }) => relationTypeHandler(value)}
                    required
                    theme={CARD_ELEMENT_OPTIONS}
                    placeholder="relationship_type"
                    options={[
                      {
                        value: "one-one",
                        label: "one-one",
                      },
                      {
                        value: "many-one",
                        label: "many-one",
                      },
                      {
                        value: "many-many",
                        label: "many-many",
                      },
                      {
                        value: "one-many",
                        label: "one-many",
                      },
                    ]}
                  />
                </Box>
              ) : null}
              {!step ? (
                <Box
                  style={{
                    marginBottom: "1.5rem",
                    color: "#6E798C",
                    fontSize: "1.25rem",
                  }}
                >
                  <Select
                    key={2}
                    value={
                      relatedTable
                        ? {
                            value: relatedTable,
                            label: relatedTable,
                          }
                        : null
                    }
                    onChange={({ value }) => setRelatedTable(value)}
                    required
                    theme={CARD_ELEMENT_OPTIONS}
                    placeholder="related_table"
                    options={relationTable}
                  />
                </Box>
              ) : null}
              {!step ? (
                <Box
                  style={{
                    marginBottom: "1.5rem",
                    color: "#6E798C",
                    fontSize: "1.25rem",
                  }}
                >
                  <Select
                    key={3}
                    value={
                      relatedField
                        ? {
                            value: relatedField,
                            label: relatedField,
                          }
                        : null
                    }
                    onChange={({ value }) => setRelatedField(value)}
                    required
                    theme={CARD_ELEMENT_OPTIONS}
                    placeholder="related_field"
                    options={relationColumns}
                  />
                </Box>
              ) : null}
              <Box type="relative">
                {/* <Input
                  type="file"
                  id="filepicker"
                  name="fileList"
                  webkitdirectory
                  multiple
                 
                  onChange={(event) => getfolder(event)}
                  name="dirpath"
                  webkitdirectory
                  webkitdirectory
                  mozdirectory
                  msdirectory
                  odirectory
                  directory
                  multiple
                /> */}
              </Box>
              {/* <input /> */}
              <Button mt={4} width="100%" fontSize={18} type="submit">
                {edit ? "Edit" : "Add"}
              </Button>
            </form>
          </Box>
        </Box>
        <Box>
          <Box
            type="tableView"
            //   m={6}
            // style={{
            //   width: "80%",
            //   margin: "7rem",
            //   marginTop: "1.5rem",
            // }}
          >
            <Table
              variant="striped"
              colorScheme="teal"
              // style={{
              //   width: "98%",
              // }}
            >
              <TableCaption>
                {basejwtPresent ? (
                  <Box type="row" justifyContent="start" mb={3}>
                    <Tooltip
                      label={
                        !restByJWT
                          ? "Click to restrict this table by jwt"
                          : "Click to not restrict this table by jwt"
                      }
                      bg="#8071b399"
                      placement="top"
                    >
                      <spam>
                        <Switch
                          size="lg"
                          style={{ background: "rgb(241 218 249)" }}
                          isChecked={restByJWT}
                          onChange={(e) => setRestByJWT(e.target.checked)}
                        />
                      </spam>
                    </Tooltip>
                    <Para ml={6}> restrict this table by jwt</Para>
                  </Box>
                ) : (
                  <Box type="row" justifyContent="start" mb={3}>
                    <Tooltip
                      label={
                        !baseJWT
                          ? "Click to make it authorization table"
                          : "Click to not make it authorization table"
                      }
                      bg="#8071b399"
                      placement="top"
                    >
                      <spam>
                        <Switch
                          size="lg"
                          style={{ background: "rgb(241 218 249)" }}
                          isChecked={baseJWT}
                          onChange={(e) => setbaseJWT(e.target.checked)}
                        />
                      </spam>
                    </Tooltip>
                    <Para ml={6}> Use this table as a Authorization table</Para>
                  </Box>
                )}

                {baseJWT ? (
                  <>
                    <Label>Select Filter Keys</Label>
                    <Box
                      style={{
                        marginBottom: "1.5rem",
                        marginTop: "10px",
                        color: "#6E798C",
                        fontSize: "1.25rem",
                        paddingTop: "10px",
                      }}
                    >
                      <Select
                        // value={columnTypesOptions.filter((option) =>
                        //   edit
                        //     ? option.label === selectedFieldTypeEdit
                        //     : option.label === selectedFieldType
                        // )}
                        onChange={handleMultiChange}
                        isMulti
                        theme={CARD_ELEMENT_OPTIONS}
                        placeholder="Select Filter"
                        options={filterOptions}
                      />
                    </Box>{" "}
                  </>
                ) : null}
                <Button width={"100%"} mt={4} onClick={createTableRequest}>
                  Create Table
                </Button>
              </TableCaption>
              <Thead>
                <Tr style={{ color: "#4A5568" }}>
                  <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                    name
                  </Th>
                  <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                    type
                  </Th>
                  <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                    unique
                  </Th>
                  <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                    nullable
                  </Th>
                  <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                    default
                  </Th>
                  {/* <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                    Foreign Key
                  </Th> */}

                  <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}></Th>
                </Tr>
              </Thead>
              <Tbody>{contentTypeApps}</Tbody>
            </Table>
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

export default CreateTable;
