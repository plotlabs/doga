import React from "react";
import { Icon } from "@chakra-ui/react";
import { AiOutlineCaretDown, AiOutlineCaretUp } from "react-icons/ai";
import { Box, Para } from "../../../styles";

export default function DropableTabs({
  name,
  page,
  setValue,
  value,
  icon,
  location,
}) {
  return (
    <Box
      type="row"
      style={{
        paddingLeft: "10px",
        height: "45px",
        margin: "5px",
        boxShadow:
          location === page
            ? "rgb(10 10 10) 0px 2px 4px -1px"
            : "rgb(0 0 0 / 7%) 0px 2px 4px 0px",
        background: location === page ? "#80808045" : "none",
        borderRadius: location === page ? "10px" : "0px",
      }}
      justifyContent="space-between"
      onClick={() => setValue(!value)}
    >
      <Box type="row">
        <i
          style={{
            minWidth: "14px",
            marginRight: "5px",
          }}
        >
          <Icon as={icon} w={5} h={5} mr={3} mb={1} color={"#ffffff"} />
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

      <Box>
        <i
          style={{
            marginRight: "5px",
          }}
        >
          {value ? (
            <Icon
              as={AiOutlineCaretUp}
              w={3}
              h={3}
              mr={3}
              mb={1}
              color={"#ffffff"}
              style={{ cursor: "pointer" }}
              onClick={() => setValue(!value)}
            />
          ) : (
            <Icon
              as={AiOutlineCaretDown}
              w={3}
              h={3}
              mr={3}
              mb={1}
              color={"#ffffff"}
              style={{ cursor: "pointer" }}
              onClick={() => setValue(!value)}
            />
          )}
        </i>
      </Box>
    </Box>
  );
}
