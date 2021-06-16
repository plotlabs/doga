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
              <p>Welcome to DOGA</p>
              <p>DOGA is a headless content management system written in and to
              create Flask Application.</p>It helps you model your data to  fit
              your requirements, with features like tabular content
              definition , simple definition of relationships, easy addition
              of data, simple deployments and monitoring and managing data
              on your remote apps too.<p>To get started click on
              Create a New App and begin creating your backed with no code !</p>
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
