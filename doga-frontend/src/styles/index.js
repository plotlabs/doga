import styled from "@emotion/styled";
import { height, variant } from "styled-system";
import { motion } from "framer-motion";
import theme from "./theme";

import {
  space,
  layout,
  color,
  flexbox,
  border,
  typography,
  background,
  grid,
  shadow,
  position,
  backgroundImage,
} from "styled-system";

export const Box = styled.div(
  variant({
    prop: "type",
    variants: {
      row: {
        display: "flex",
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-between",
      },
      column: {
        display: "flex",
        flexDirection: "column",
      },
      center: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
      },
      relative: {
        boxSizing: "border-box",
        clear: "both",
        fontSize: "1rem",
        position: "relative",
        textAlign: "inherit",
      },
      tableView: {
        marginTop: "1.25rem",
        padding: "0.75rem",
        borderWidth: "1px",

        background: "white",
        margin: "1.5rem 2.5rem",
      },
      loader: {
        position: "fixed",
        zIndex: "999",
        overflow: "show",
        margin: "auto",
        top: "0",
        left: "200px",
        bottom: "0",
        right: "0",
        width: "60px",
        height: "60px",
        color: " #ffffff",
        boxShadow: "#382e6c 0px 2px 4px 1px",
        background: "#8071b3",
        borderRadius: "50%",
        padding: "3px",
      },
      loaderText: {
        position: "fixed",
        zIndex: "999",
        overflow: "show",
        margin: "auto",
        top: "150px",
        left: "200px",
        bottom: "0",
        right: "0",
        width: "100px",
        height: "50px",

        padding: "13px",
      },
      loaderCentered: {
        position: "fixed",
        zIndex: "999",
        overflow: "show",
        margin: "auto",
        left: "0",
        top: "0",
        bottom: "0",
        right: "0",
        width: "60px",
        height: "60px",
        color: " #ffffff",
        boxShadow: "#382e6c 0px 2px 4px 1px",
        background: "#8071b3",
        borderRadius: "50%",
        padding: "3px",
      },
      heading: {
        width: "100%",
        marginLeft: "0",
        marginRight: "0",
        padding: "12px 20px 10px",
        minHeight: "63px",
        marginTop: "2px",
        borderBottom: "2px solid #8071b399",
        backgroundColor: "#f7f8fb",
        padding: "20px",
      },
    },
  }),
  space,
  color,
  grid,
  layout,
  flexbox,
  border,
  typography,
  shadow,
  position,
  background
);
export const MotionBox = styled(motion.div)(
  variant({
    prop: "type",
    variants: {
      row: {
        display: "flex",
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-between",
      },
      column: {
        display: "flex",
        flexDirection: "column",
      },
      center: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
      },
      rowSidebar: {
        display: "flex",
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-between",
        "&:hover": {
          color: "purple",
        },
      },
    },
  }),
  space,
  color,
  grid,
  layout,
  flexbox,
  border,
  typography,
  shadow,
  position,
  background
);

export const Button = styled("button")(
  {
    appearance: "none",
    fontFamily: theme.fonts.DM,
    fontWeight: theme.fontWeights.semiBold,
    fontSize: "15px",

    cursor: "pointer",
    width: "fit-content",

    outline: "none",
    border: "none",

    userSelect: "none",
    padding: "0.75em 1.75em",
    borderRadius: "5px",
    display: "inline-block",
    color: "#ffffff",
    boxShadow: "#382e6c 0px 2px 4px 1px",
    background: "#8071b3",
    "&:hover": {
      opacity: ".8",
    },
  },
  variant({
    prop: "type",
    variants: {
      primary: {
        width: "110px",
      },
      secondary: {},
      tableAdd: {
        borderRadius: "4px 0 4px 0",
        color: "purple",
        backgroundColor: "rgb(241 218 249)",
        width: "-webkit-fill-available",

        backgroundImage: "none",
      },
      toggleTable: {
        color: "purple",
        backgroundColor: "rgb(255 255 255)",
        borderRadius: "0px",
        backgroundImage: "none",
        "&:hover": {
          opacity: "1",
        },
      },
    },
  }),
  space,
  color,
  typography,
  layout,
  flexbox,
  border
);
export const Tab = styled("button")(
  {
    appearance: "none",
    fontFamily: theme.fonts.DM,
    fontWeight: theme.fontWeights.normal,
    fontSize: "16px",
    padding: "8px 13px",
    color: "#191919",
    backgroundColor: "#f2f2f2",
    cursor: "pointer",
    borderRadius: "15px",
    width: "100%",
    borderColor: "#e8e8e8",
  },
  variant({
    prop: "type",
    variants: {
      active: {
        color: "white",
        bg: "orange",
        boxShadow: "0px 4px 14px rgba(237, 107, 101, 0.9)",
      },
    },
  }),
  space,
  color,
  typography,
  layout,
  flexbox,
  border
);

export const Para = styled.p(
  {
    fontSize: "0.91rem",
    color: theme.colors.grey,
    lineHeight: "24px",
  },
  variant({
    prop: "type",
    variants: {
      info: {
        fontSize: "0.70rem",
        color: theme.colors.grey,
        lineHeight: "inherit",
      },
    },
  }),
  space,
  color,
  typography,
  position,
  border,
  layout
);

export const Span = styled.span(
  {
    fontSize: "theme.fontSizes[4]",
    color: theme.colors.grey,
    lineHeight: "24px",
  },
  space,
  color,
  typography,
  layout,
  variant({
    prop: "type",
    variants: {
      icon: {
        left: "12px",

        color: "#dbdbdb",

        pointerEvents: "none",
        position: "absolute",
        top: "8px",
        width: "2.5em",
        zIndex: "4",
      },
      heading: {
        color: "#5d6c84",
        fontSize: "1.2rem",
      },
    },
  })
);
export const Tag = styled.span(
  {
    fontSize: theme.fontSizes[4],

    borderRadius: "4px 0 4px 0",
  },
  space,
  color,
  typography,
  layout
);
export const Tags = styled.div(
  {
    fontSize: theme.fontSizes[4],
    borderRadius: "4px 0 4px 0",
    fontSize: "xx-large",
    border: "none",
  },
  space,
  color,
  typography,
  layout,
  height,
  border
);

export const H1 = styled.h1(
  {
    fontSize: theme.fontSizes[10],
    color: theme.colors.lightPurple,
    fontFamily: theme.fonts.DM,
    fontWeight: theme.fontWeights.light,
    lineHeight: "64px",
  },

  space,
  color,
  typography,
  position,
  border,
  layout,
  variant({
    prop: "type",
    variants: {
      fullBorder: {
        paddingBottom: 12,
        borderBottom: "4px solid",
        borderColor: "rgb(127, 0, 255)",
      },
      centerBorder: {
        paddingBottom: 12,
        borderBottom: "4px solid",
        borderColor: "rgb(127, 0, 255)",
        width: "fit-content",
        textAlign: "center",
      },
    },
  })
);
export const H2 = styled.h2(
  {
    fontSize: "2rem",
    color: "#8071b3",
    fontWeight: "500",
    lineHeight: "18px",
    marginBottom: "0.5rem",
  },
  space,
  color,
  typography,
  position,
  border,
  layout,
  variant({
    prop: "type",
    variants: {
      fullBorder: {
        paddingBottom: 12,
        borderBottom: "4px solid",
        borderColor: "#4B0082",
      },
      centerBorder: {
        paddingBottom: 12,
        borderBottom: "4px solid",
        borderColor: "#4B0082",
        width: "fit-content",
        textAlign: "center",
      },
    },
  })
);
export const H3 = styled.h3(
  {
    fontSize: theme.fontSizes[8],
    color: theme.colors.lightPurple,
    fontFamily: theme.fonts.DM,
    fontWeight: theme.fontWeights.normal,
    lineHeight: "36px",
  },
  space,
  color,
  typography,
  position,
  border,
  layout,
  variant({
    prop: "type",
    variants: {
      fullBorder: {
        paddingBottom: 12,
        borderBottom: "4px solid",
        borderColor: "orange",
      },
      centerBorder: {
        paddingBottom: 12,
        borderBottom: "4px solid",
        borderColor: "orange",
        width: "fit-content",
        textAlign: "center",
      },
    },
  })
);
export const H5 = styled.h5(
  {
    fontSize: theme.fontSizes[6],
    color: theme.colors.purple,
    fontFamily: theme.fonts.DM,
    fontWeight: theme.fontWeights.normal,
    lineHeight: "26px",
  },
  space,
  color,
  typography,
  position,
  border,
  layout
);
export const H6 = styled.h6(
  {
    fontSize: theme.fontSizes[4],
    color: theme.colors.purple,
    fontFamily: theme.fonts.DM,
    fontWeight: theme.fontWeights.normal,
    marginBottom: 0,
  },
  space,
  color,
  typography,
  position,
  border,
  layout
);

export const StyledLink = styled("a")(
  {
    fontSize: theme.fontSizes[5],
    color: theme.colors.grey,
    lineHeight: "24px",
    cursor: "pointer",
  },
  space,
  color,
  typography,
  position,
  border,
  layout
);

export const Image = styled.img`
  ${space}
  ${color}
  ${typography}
  ${position}
  ${border}
  ${shadow}
`;
export const ResponsiveImage = styled.img`
  ${space}
  ${color}
  ${typography}
  ${position}
  ${border}
  ${shadow}
  ${layout}
`;

export const Input = styled("input")(
  {
    border: "1px solid #d3d3d3",
    borderRadius: 5,
  },
  space,
  color,
  typography,
  layout,
  position,
  border,
  shadow,
  variant({
    prop: "inputType",
    variants: {
      auth: {
        paddingLeft: 42,
      },
    },
  })
);
export const Label = styled("label")(
  {
    display: "inline-block",
    fontSize: "1rem",
    fontWeight: "700",
    fontFamily: theme.fonts.DM,
    marginBottom: "6px",
    padding: "0",
    color: "#5d6c84",
  },
  space,
  color,
  typography,
  layout,
  position,
  border,
  shadow,
  variant({
    prop: "type",
    variants: {
      auth: {
        paddingLeft: 42,
      },
    },
  })
);
export const TextArea = styled("textArea")(
  {
    border: "1px solid #d3d3d3",
  },
  space,
  color,
  typography,
  layout,
  position,
  border,
  shadow
);
