import React, { useEffect, Suspense, useState } from "react";
import { Route, Switch, withRouter, Redirect } from "react-router-dom";
import { setGlobal, useGlobal } from "reactn";
import { setHeader, defaultQueryFn, setJwtHeader } from "./Api";
import { ReactQueryDevtools } from "react-query/devtools";
import { QueryClient, QueryClientProvider, useQuery } from "react-query";
import { ChakraProvider } from "@chakra-ui/react";
import Header from "./components/Header/Header";
import Sidebar from "./components/Sidebar/Sidebar";
import Footer from "./components/Footer/Footer";
import { ThemeProvider } from "@emotion/react";
import theme from "./styles/theme";
import { Box, H1 } from "./styles";
import "./styles/globals.css";
import ClipLoader from "react-spinners/ClipLoader";
import { io } from "socket.io-client";
import { useToast, createStandaloneToast } from "@chakra-ui/react";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      queryFn: defaultQueryFn,
      refetchOnWindowFocus: false,
      // suspense: true,
    },
  },
});
// const queryClient = new QueryClient();

setGlobal({
  token: null,
});

const myTheme = {
  backgroundColor: "#F1EFF8",
};

const Login = React.lazy(() => {
  return import("./containers/Login/Login");
});
const Signup = React.lazy(() => {
  return import("./containers/Signup/Signup");
});
const Dashboard = React.lazy(() => {
  return import("./containers/Dashboard/Dashboard");
});
const CreateDatabase = React.lazy(() => {
  return import("./containers/CreateDatabase/CreateDatabase");
});
const Database = React.lazy(() => {
  return import("./containers/Database/Database");
});
const Mysql = React.lazy(() => {
  return import("./containers/Mysql/Mysql");
});
const Content = React.lazy(() => {
  return import("./containers/Application/Content");
});
const AppHome = React.lazy(() => {
  return import("./containers/AppHome/AppHome");
});
const HerokuDeploy = React.lazy(() => {
  return import("./containers/Deploy/HerokuDeploy");
});
const AwsDeploy = React.lazy(() => {
  return import("./containers/Deploy/Deploy");
});
const Twilio = React.lazy(() => {
  return import("./containers/Plugins/Twilio");
});
const Sendgrid = React.lazy(() => {
  return import("./containers/Plugins/Sendgrid");
});
const Application = React.lazy(() => {
  return import("./containers/Application/Application");
});
const AppDocs = React.lazy(() => {
  return import("./containers/AppDocs/AppDocs");
});

const socket = io("http://127.0.0.1:8008", {
  query: `Authorization=${localStorage.getItem("token")}`,
});

console.log(socket);

// useEffect(() => {
socket.on("connect", () => {
  // socket.send("User has connected!");
});
// socket.send(localStorage.getItem("userEmail"));
// }, [localStorage.getItem("userEmail")]);

const App = (props) => {
  const [token, setToken] = useGlobal("token");
  const [deployProcessStatus, setdeployProcessStatus] = useGlobal("deploy");
  const [jwtToken, setJwtToken] = useGlobal("jwtToken");
  // const [data, setData] = useState();
  const toast = createStandaloneToast();

  // const socket = io("http://127.0.0.1:8008", {
  //   extraHeaders: {
  //     Authorization: localStorage.getItem("jwtToken"),
  //   },
  // });

  React.useEffect(() => {
    socket.on("broadcast message", function (msg) {
      console.log(msg, "MSG");

      if (msg.action_type === "deploy-app") {
        setdeployProcessStatus({
          status: msg.action_status,
          message: msg.full_message,
        });
      }
      toast({
        position: "top-right",
        description: msg.full_message,
        status: "info",
        duration: 3000,
        isClosable: true,
      });
    });
    // socket.emit("message", { admin_id: "nishant@gmail.com" });
  }, []);
  // });
  console.log(deployProcessStatus, "deployProcessStatus-main");
  useEffect(() => {
    let token = localStorage.getItem("token");
    if (token) {
      setToken(token);
      setHeader(token);
    }
  }, [token, setHeader, localStorage.getItem("token")]);

  useEffect(() => {
    let token = localStorage.getItem("jwtToken");
    if (token) {
      setJwtToken(token);
      setJwtHeader(token);
    }
  }, [jwtToken, setJwtHeader, localStorage.getItem("jwtToken")]);
  console.log("app", token, localStorage.getItem("token"));
  let routes = (
    <Switch>
      {/* <Route path="/auth" render={(props) => <Auth {...props} />} /> */}
      <Route path="/Login" render={(props) => <Login />} />
      <Route path="/Signup" render={(props) => <Signup />} />
      <Redirect to="/Login" />
    </Switch>
  );

  if (localStorage.getItem("token")) {
    routes = (
      <Switch>
        <Route path="/Login" render={(props) => <Login />} />
        <Route path="/Signup" render={(props) => <Signup />} />
        <Route path="/Dashboard" render={(props) => <Dashboard />} />
        <Route path="/create-db" render={(props) => <CreateDatabase />} />
        <Route path="/mysql" render={(props) => <Mysql />} />
        <Route path="/database" render={(props) => <Database />} />
        <Route
          exact
          path="/deploy/heroku"
          render={(props) => <HerokuDeploy />}
        />
        <Route path="/deploy/aws" render={(props) => <AwsDeploy />} />
        <Route path="/plugin/twilio" render={(props) => <Twilio />} />
        <Route path="/plugin/sendgrid" render={(props) => <Sendgrid />} />
        <Route path="/create-new-app" render={(props) => <Application />} />

        <Route exact path="/application/:app" render={(props) => <AppHome />} />
        <Route path="/application/docs/:app" render={(props) => <AppDocs />} />
        <Route
          path="/application/:app/:table"
          render={(props) => <Content />}
        />
        {/* <Redirect to="/" /> */}
      </Switch>
    );
  }

  let show = !localStorage.getItem("token") ? (
    <Suspense fallback={<p>Loading...</p>}>{routes}</Suspense>
  ) : (
    <Box
      display="grid"
      gridTemplateColumns={{ _: "1fr", md: "220px auto" }}
      gridTemplateAreas={
        {
          // _: "p-workspace__sidebar p-workspace__primary_view",
        }
      }
      maxHeight="100%"
      height="calc(100vh )"
    >
      <Sidebar />
      <Box
        // width={{ _: "100vw", md: "calc(100vw - 220px)" }}
        width="auto"
        // gridTemplateAreas={{ _: "p-workspace__primary_view_contents" }}
        gridTemplateRows="auto"
        backgroundColor="#ffffff"
      >
        <Suspense
          fallback={
            <Box type="loader">
              <ClipLoader color={"#ffffff"} size={55} />
            </Box>
          }
        >
          <Header />
          {routes}
        </Suspense>
      </Box>
      {/* <Ads /> */}
    </Box>
  );

  return (
    <>
      <QueryClientProvider client={queryClient}>
        <ChakraProvider>
          <ThemeProvider theme={theme}>
            <ReactQueryDevtools initialIsOpen={false} />

            {/* <Box margin="auto" maxWidth="1400px"> */}
            <Box>
              {show}
              {/* <Footer /> */}
            </Box>
          </ThemeProvider>
        </ChakraProvider>
      </QueryClientProvider>
    </>
  );
};

export default App;
