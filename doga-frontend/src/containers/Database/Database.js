import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { useGlobal } from "reactn";
import { NavLink } from "react-router-dom";
import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableCaption,
} from "@chakra-ui/react";
import {
  Box,
  ResponsiveImage,
  Image,
  Button,
  StyledLink,
  Span,
  H1,
  H2,
  H5,
  MotionBox,
  Para,
} from "../../styles";
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
import { useDisclosure } from "@chakra-ui/react";
import CreateDatabase from "../CreateDatabase/CreateDatabase";
import { Icon } from "@chakra-ui/react";
import { FaEdit } from "react-icons/fa";
import ClipLoader from "react-spinners/ClipLoader";
import { useQuery } from "react-query";
import Api, { setHeader, APIURLS } from "../../Api";
import EditDatabase from "../../components/Modal/EditDatabase";

const Database = () => {
  const [typeSelected, setTypeSelected] = useState();
  const [editDbConnection, setEditDbConnection] = useState();
  const { isOpen, onOpen, onClose } = useDisclosure();

  const { data, isLoading } = useQuery(APIURLS.getDbConnections);
  const db = data;

  const editDbHandler = (key) => {
    setEditDbConnection(key);
    onOpen();
  };
  const onCloseHandler = () => {
    setEditDbConnection();
    onClose();
  };

  return isLoading ? (
    <Box type="loader">
      <ClipLoader color={"#ffffff"} size={55} />
    </Box>
  ) : (
    <>
      {/* <EditDatabase
        isOpen={isOpen}
        onOpen={onOpen}
        onClose={onCloseHandler}
        edit={editDbConnection}
      /> */}

      <Box type="heading" textAlign="center">
        {/* <Span type="heading">{table}</Span> */}
        <H2>Database</H2>
      </Box>
      <Box type="row" flexDirection="row-reverse" m={6}>
        <Box
          style={{
            backgroundColor: "white",
            border: "2px solid rgb(226, 232, 240)",
            padding: "8px",
            borderRadius: "10px",
            width: "fit-content",
          }}
        >
          <Menu>
            <MenuButton style={{ color: "#6E798C" }}>
              {typeSelected || "DB Type"}
            </MenuButton>
            <MenuList>
              <MenuItem onClick={() => setTypeSelected("mysql")}>
                <Para>MySQL</Para>
              </MenuItem>
              <MenuItem onClick={() => setTypeSelected("sqlite")}>
                <Para>SQLite</Para>
              </MenuItem>
              <MenuItem onClick={() => setTypeSelected("postgresql")}>
                <Para>PostgreSQL</Para>
              </MenuItem>
              <MenuItem onClick={() => setTypeSelected()}>
                <Para>All</Para>
              </MenuItem>
            </MenuList>
          </Menu>
        </Box>
      </Box>
      <Box type="tableView" m={6}>
        {" "}
        <Table
          variant="striped"
          colorScheme="teal"
          style={{
            width: "98%",
          }}
        >
          {/* <TableCaption>
            <Button type="tableAdd" onClick={onOpen}>
              Create A DB Connection
            </Button>
          </TableCaption> */}
          <Thead>
            <Tr style={{ color: "#4A5568" }}>
              <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                connection
              </Th>
              <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                database type
              </Th>
              <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                database
              </Th>
              <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>host</Th>
              <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>port</Th>
              <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                username
              </Th>
              <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                password
              </Th>
              <Th style={{ color: "#4A5568", borderColor: "#EDF2F7" }}></Th>
            </Tr>
          </Thead>
          <Tbody>
            {db?.map((key) => {
              if (typeSelected && key.database_type != typeSelected) {
                return true;
              }
              return (
                <Tr style={{ color: "#4A5568" }}>
                  <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                    {key.connection_name}
                  </Td>
                  <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                    {key.database_type}
                  </Td>
                  <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                    {key.database_name}
                  </Td>
                  <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                    {key.host}
                  </Td>
                  <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                    {key.host}
                  </Td>
                  <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                    {key.port}
                  </Td>
                  <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                    {key.username}
                  </Td>
                  <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                    {key.password}
                  </Td>
                  {/* <Td style={{ color: "#4A5568", borderColor: "#EDF2F7" }}>
                    {
                      // <i onClick={() => {setEditDbConnection(key) &&onOpen }}>
                      <i onClick={() => editDbHandler(key)}>
                        <Icon as={FaEdit} w={5} h={5} color={"#4B0082"} />
                      </i>
                    }
                  </Td> */}
                </Tr>
              );
            })}
          </Tbody>
        </Table>
      </Box>
    </>
  );
};

export default Database;
