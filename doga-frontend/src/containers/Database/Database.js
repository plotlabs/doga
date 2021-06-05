import React, { useState } from "react";
import { Table, Thead, Tbody, Tr, Th, Td } from "@chakra-ui/react";
import { Box, H2, Para } from "../../styles";
import { Menu, MenuButton, MenuList, MenuItem } from "@chakra-ui/react";
import ClipLoader from "react-spinners/ClipLoader";
import { useQuery } from "react-query";
import { APIURLS } from "../../Api";

const Database = () => {
  const [typeSelected, setTypeSelected] = useState();
  const { data, isLoading } = useQuery(APIURLS.getDbConnections);
  const db = data;

  return isLoading ? (
    <Box type="loader">
      <ClipLoader color={"#ffffff"} size={55} />
    </Box>
  ) : (
    <>
      <Box type="heading" textAlign="center">
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
            {db?.map((key, index) => {
              if (typeSelected && key.database_type != typeSelected) {
                return true;
              }
              return (
                <Tr style={{ color: "#4A5568" }} key={index}>
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
