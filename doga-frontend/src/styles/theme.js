const breakpoints = ["768px", "1200px", "1500px"];

breakpoints.sm = breakpoints[0];
breakpoints.md = breakpoints[1];
breakpoints.lg = breakpoints[2];

export const colors = {
  black: "#081F32",
  grey: "#6E798C",
  orange: "#ED6B65",
  blue: "#1D487B",
  white: "#fff",
  lightGrey: "#f2f2f2",
  purple: "#492897",
};

const fonts = {
  OP: "Open SANS",
  DM: "DM SANS",
};

const space = [
  "0",
  "0.25rem",
  "0.5rem",
  "0.75rem",
  "1rem",
  "1.25rem",
  "1.5rem",
  "2rem",
  "2.5rem",
  "3rem",
  "4rem",
  "5rem",
];

const fontWeights = {
  light: 300,
  normal: 400,
  medium: 500,
  semiBold: 600,
  bold: 700,
};

const fontSizes = [
  ".5rem",
  ".75rem",
  ".875rem",
  "1rem",
  "1.125rem",
  "1.25rem",
  "1.5rem",
  "1.875rem",
  "2.25rem",
  "3rem",
  "4rem",
];
const lineHeights = [
  ".5rem",
  ".75rem",
  ".875rem",
  "1rem",
  "1.125rem",
  "1.25rem",
  "1.5rem",
  "1.875rem",
  "2.25rem",
  "3rem",
  "4rem",
];

const radii = {
  sm: "0.125rem",
  base: "0.25rem",
  md: "0.375rem",
  lg: "0.5rem",
};

const shadows = {
  card: "0px 6px 32px rgba(0, 0, 0, 0.06)",
  xs: "0 0 0 1px rgba(0, 0, 0, 0.05)",
  sm: "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
  base: "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
  invision: "0 -1px 1px 0 rgba(0,0,0,.05),0 1px 2px 0 rgba(2,32,65,.2)",
  invisionHover: "0 4px 25px 0 rgba(0,0,0,.2),0 0 1px 0 rgba(0,0,0,.15)",
  md: "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
  lg: "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
  blueShadow: "0px 20px 64px rgba(29, 72, 123, 0.3)",
  orangeShadow: "0px 12px 32px #dd726a75",
  greenShadow: "0px 12px 32px #6addac75",
  shadow3: "0px 12px 32px #6a7cdd75",
  shadow4: "0px 12px 32px #99dd6a75",
};

const theme = {
  breakpoints,
  fonts,
  fontSizes,
  fontWeights,
  lineHeights,
  colors,
  shadows,
  radii,
  space,
};

export default theme;
