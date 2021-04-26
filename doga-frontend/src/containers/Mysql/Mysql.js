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
import { useQuery } from "react-query";
import Api, { setHeader, APIURLS } from "../../Api";
const Mysql = () => {
  const dbConnections = useQuery(APIURLS.getDbConnections);
  console.log(dbConnections);
  return (
    <>
      <Table
        variant="striped"
        colorScheme="teal"
        style={{
          background: "white",
          margin: "10px",
          width: "98%",
          border: "2px solid gray",
        }}
      >
        <Thead>
          <Tr>
            <Th>To convert</Th>
            <Th>into</Th>
            <Th isNumeric>multiply by</Th>
          </Tr>
        </Thead>
        <Tbody>
          <Tr>
            <Td>inches</Td>
            <Td>millimetres (mm)</Td>
            <Td isNumeric>25.4</Td>
          </Tr>
          <Tr>
            <Td>feet</Td>
            <Td>centimetres (cm)</Td>
            <Td isNumeric>30.48</Td>
          </Tr>
          <Tr>
            <Td>yards</Td>
            <Td>metres (m)</Td>
            <Td isNumeric>0.91444</Td>
          </Tr>
        </Tbody>
      </Table>
    </>
  );
};

export default Mysql;
