import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import { APIURLS } from "../../Api";
import { useQuery } from "react-query";
import { Box, Button, H2, Para } from "../../styles";
import { useIsFetching } from "react-query";
import ClipLoader from "react-spinners/ClipLoader";

const Dashboard = () => {
  const appsCreated = useQuery(APIURLS.appInfo("app"));

  const dbConnections = useQuery(APIURLS.getDbConnections);

  const isFetchingApps = useIsFetching([APIURLS.getContentType]);
  return appsCreated?.isLoading ||
    dbConnections?.isLoading ||
    isFetchingApps > 0 ? (
    <>
      {" "}
      <Box type="loader">
        <ClipLoader color={"#ffffff"} size={55} />
      </Box>{" "}
    </>
  ) : (
    <>
      <Box
        boxShadow="invision"
        p={2}
        backgroundColor="white"
        style={{ margin: "50px" }}
      >
        <Box style={{ margin: "25px" }}>
          <H2 type="centerBorder" color={"#6E798C"}>
            {" "}
            Hi {localStorage.getItem("userName")}!
          </H2>
          <Para mt={4}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
            ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
            aliquip ex ea commodo consequat. Duis aute irure dolor in
            reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
            pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
            culpa qui officia deserunt mollit anim id est laborum.
          </Para>
          <Box type="row" style={{ marginTop: "55px" }}>
            <NavLink to={`/create-new-app`}>
              {" "}
              <Button width="235px">Create A New APP</Button>
            </NavLink>

            <NavLink to={`/deploy/aws`}>
              <Button width="195px">Deploy On AWS</Button>
            </NavLink>
            <NavLink to={`/deploy/heroku`}>
              <Button width="195px">Deploy On Heroku</Button>
            </NavLink>
            <NavLink to={`/plugin/sendgrid`}>
              <Button width="195px">Sendgrid</Button>
            </NavLink>
            <NavLink to={`/plugin/twilio`}>
              <Button width="195px">Twilio</Button>
            </NavLink>
          </Box>
        </Box>
      </Box>
    </>
  );
};

export default Dashboard;
