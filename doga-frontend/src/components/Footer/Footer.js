import React, { useEffect } from "react";
import { useGlobal } from "reactn";
import {
  Box,
  ResponsiveImage,
  Image,
  Button,
  StyledLink,
  Span,
} from "../../styles";

export default function Footer() {
  const [token] = useGlobal("token");

  return (
    <Box
      gridColumn={2}
      px={4}
      display={["flex"]}
      flexDirection={["column", "row"]}
      justifyContent="space-between"
    >
      <Box type="row">Hello</Box>
      <Box type="row">Yo</Box>
    </Box>
  );
}
