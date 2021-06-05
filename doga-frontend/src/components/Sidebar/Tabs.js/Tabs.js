import React from "react";
import { Icon } from "@chakra-ui/react";
import { NavLink } from "react-router-dom";
import { Box, Para } from "../../../styles";

export default function Tabs({ name, page, icon, location, subTab }) {
  return (
    <NavLink to={page}>
      {" "}
      <Box
        type="row"
        style={{
          paddingLeft: "30px",
          height: "35px",
          margin: "5px",
          paddingLeft: subTab ? "30px" : "10px",
          height: subTab ? "35px" : "45px",
          boxShadow:
            location === page
              ? "rgb(10 10 10) 0px 2px 4px -1px"
              : "rgb(0 0 0 / 7%) 0px 2px 4px 0px",
          background: location === page ? "#80808045" : "none",
          borderRadius: location === page ? "10px" : "0px",
        }}
        justifyContent="start"
      >
        <i
          style={{
            minWidth: "14px",
            marginRight: "5px",
          }}
        >
          {<Icon as={icon} w={5} h={5} mr={3} mb={1} color={"#ffffff"} />}
        </i>

        <Para
          style={{
            fontWeight: "500",
            lineHeight: "none",
            color: "#ffffff",
          }}
        >
          {name}
        </Para>
      </Box>
    </NavLink>
  );
}
