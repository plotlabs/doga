import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { useGlobal } from "reactn";
import { Checkbox, CheckboxGroup } from "@chakra-ui/react";
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
import { Switch } from "@chakra-ui/react";
// import { useQueryClient } from "react-query";
// import { useToast, createStandaloneToast } from "@chakra-ui/react";
// import Api, { setHeader, APIURLS } from "../../Api";
import { Icon } from "@chakra-ui/react";
import { useQuery, useQueryClient } from "react-query";
import { useToast, createStandaloneToast } from "@chakra-ui/react";
import Api, { setHeader, APIURLS } from "../../Api";
import Select from "react-select";

const ContentField = ({
  isOpen,
  onOpen,
  onClose,
  appName,
  connectionSelected,
  columns,
  tablename,
}) => {
  const [token] = useGlobal("token");
  const { handleSubmit, register, errors } = useForm();
  const [selectedFieldType, setSelectedFieldType] = useState();
  const [foreignKeyOptions, setForeignKeyOptions] = useState();
  const [relationOptions, setRelationOptions] = useState();
  const [foreignKeyTable, setForeignKeyTable] = useState();
  const [foreignKeyColumn, setForeignKeyColumn] = useState();
  const [foreignKeyCheck, setForeignKeyCheck] = useState(false);
  const [relationCheck, setRelationCheck] = useState(false);
  const [relationshipType, setRelationshipType] = useState();
  const [relatedTable, setRelatedTable] = useState();
  const [relatedField, setRelatedField] = useState();
  const [value, setValue] = React.useState("1");
  //   const queryClient = useQueryClient();
  const toast = createStandaloneToast();
  const queryClient = useQueryClient();
  const columnTypes = useQuery(APIURLS.getColumnTypes);
  const contentType = useQuery(APIURLS.getContentType);
  //   const [loading, setLoading] = useState(false);
  //   const [success, setSuccess] = useState(false);
  //   const [apiErr, setApiErr] = useState(null);
  //   const queryClient = useQueryClient();
  //   const toast = createStandaloneToast();

  async function foreignkeyfn() {
    let foreignKeyCheckValue = foreignKeyCheck;
    setForeignKeyCheck(!foreignKeyCheckValue);
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

  async function relationshipfn() {
    let relationCheckValue = relationCheck;
    setRelationCheck(!relationCheckValue);
    try {
      let { data } = await Api.post(APIURLS.getForeignkey, {
        app_name: appName,
        type: "",
      });
      setRelationOptions(data);
    } catch ({ response }) {
      console.log(response);
    }
  }

  console.log("here", columns);
  let columnTypesOptions = [];

  if (columnTypes?.data?.result) {
    {
      Object.entries(columnTypes?.data?.result).map(([prop, val]) => {
        // console.log(val);
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

  console.log("foreignkeyTable", relationTable);
  console.log("foreignKeyOptions", relationOptions);
  console.log("foreignkeyColumns", relationColumns);
  console.log("sds", foreignKeyCheck);

  async function handleSignup(params) {
    // console.log(params);
    try {
      let def = params.default;
      if (selectedFieldType === ("INTEGER" || "INT" || "Integer")) {
        console.log("inttt");
        def = parseInt(params.default);
      }
      if (foreignkeyColumns && foreignKeyCheck) {
        columns.push({
          name: params.name,
          type: selectedFieldType,
          nullable: params.nullable,
          unique: params.unique,
          default: def,
          foreign_key: `${foreignKeyTable}.${foreignKeyColumn}`,
        });
      } else if (relationCheck && relationColumns) {
        columns.push({
          name: params.name,
          type: selectedFieldType,
          nullable: params.nullable,
          unique: params.unique,
          default: def,
          relationship: {
            relationship_type: relationshipType,
            related_field: relatedField,
            related_table: relatedTable,
          },
        });
      } else {
        columns.push({
          name: params.name,
          type: selectedFieldType,
          nullable: params.nullable,
          unique: params.unique,
          default: def,
        });
      }

      let { data } = await Api.put(APIURLS.getContentType, {
        table_name: tablename,
        app_name: appName,
        // restrict_by_jwt: false,
        columns: columns,
      });

      await queryClient.refetchQueries([APIURLS.getContentType]);
      // setSuccess(true);

      toast({
        title: "Database created successfully.",
        description: data?.result,
        status: "success",
        duration: 9000,
        isClosable: false,
      });
      onClose();
      console.log("there", columns);
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
      //   setLoading(false);`
    }
    // setTableName(params.name);
    // setStep(3);
  }

  return (
    <>
      <Modal isOpen={isOpen} onClose={onClose}>
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
                {/* <Box type="relative"> */}
                {/* <Input
                  name="tableName"
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
                )} */}
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
                    onChange={({ value }) => setSelectedFieldType(value)}
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
                    ref={register}
                    mb={2}
                  />

                  {errors?.name && (
                    <Span color="orange" mb={4}>
                      {errors?.name?.message}
                    </Span>
                  )}
                </Box>
                <Label>nullable</Label>
                <Box type="relative">
                  <Input
                    name="nullable"
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
                <Label>unique</Label>
                <Box type="relative">
                  <Input
                    name="unique"
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
                <Label>default</Label>
                <Box type="relative">
                  <Input
                    name="default"
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

                {/* <Checkbox
                  isChecked={foreignKeyCheck}
                  // isIndeterminate={foreignKeyCheck}
                  onChange={(e) => setForeignKeyCheck(e.target.checked)}
                  // value={true}
                  // isIndeterminate={isIndeterminate}
                  // onChange={(e) => setCheckedItems([e.target.checked, e.target.checked])}
                  onClick={foreignkeyfn}
                >
                  Do you want to add foreign key
                </Checkbox> */}
                <Box>
                  <Switch
                    size="lg"
                    style={{ background: "rgb(241 218 249)" }}
                    onClick={foreignkeyfn}
                  />
                  <Para> Do you want to add foreign key</Para>
                </Box>

                <br />
                <Label>foreign_key</Label>

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
                    style={{ marginBottom: "5px" }}
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
                <Box
                  style={{
                    marginBottom: "1.5rem",
                    color: "#6E798C",
                    fontSize: "1.25rem",
                  }}
                >
                  <Select
                    key={2}
                    // value={edit ? `${columns[edit]?.type}` : selectedFieldType}
                    // value={columnTypesOptions.filter((option) =>
                    //   edit
                    //     ? option.label === selectedFieldTypeEdit
                    //     : option.label === selectedFieldType
                    // )}
                    // onChange={({ value }) =>
                    //   edit
                    //     ? setSelectedFieldTypeEdit(value)
                    //     : setSelectedFieldType(value)
                    // }
                    onChange={({ value }) => setForeignKeyColumn(value)}
                    required
                    theme={CARD_ELEMENT_OPTIONS}
                    placeholder="Select Field"
                    options={foreignkeyColumns}
                  />
                </Box>
                <Box>
                  <Switch
                    size="lg"
                    style={{ background: "rgb(241 218 249)" }}
                    onClick={relationshipfn}
                  />
                  <Para> Do you want to add Relations</Para>
                </Box>
                <Label>Relations</Label>

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
                    onChange={({ value }) => setRelationshipType(value)}
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
                <Box
                  style={{
                    marginBottom: "1.5rem",
                    color: "#6E798C",
                    fontSize: "1.25rem",
                  }}
                >
                  <Select
                    key={2}
                    // value={edit ? `${columns[edit]?.type}` : selectedFieldType}
                    // value={columnTypesOptions.filter((option) =>
                    //   edit
                    //     ? option.label === selectedFieldTypeEdit
                    //     : option.label === selectedFieldType
                    // )}
                    // onChange={({ value }) =>
                    //   edit
                    //     ? setSelectedFieldTypeEdit(value)
                    //     : setSelectedFieldType(value)
                    // }
                    onChange={({ value }) => setRelatedTable(value)}
                    required
                    theme={CARD_ELEMENT_OPTIONS}
                    placeholder="related_table"
                    options={relationTable}
                  />
                </Box>
                <Box
                  style={{
                    marginBottom: "1.5rem",
                    color: "#6E798C",
                    fontSize: "1.25rem",
                  }}
                >
                  <Select
                    key={3}
                    // value={edit ? `${columns[edit]?.type}` : selectedFieldType}
                    // value={columnTypesOptions.filter((option) =>
                    //   edit
                    //     ? option.label === selectedFieldTypeEdit
                    //     : option.label === selectedFieldType
                    // )}
                    // onChange={({ value }) =>
                    //   edit
                    //     ? setSelectedFieldTypeEdit(value)
                    //     : setSelectedFieldType(value)
                    // }
                    onChange={({ value }) => setRelatedField(value)}
                    required
                    theme={CARD_ELEMENT_OPTIONS}
                    placeholder="related_field"
                    options={relationColumns}
                  />
                </Box>
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

export default ContentField;
