import React, { useEffect, Suspense } from "react";
import { Route, Switch, Redirect } from "react-router-dom";
import { setGlobal, useGlobal } from "reactn";
import { setHeader, defaultQueryFn, setJwtHeader } from "./Api";
import { ReactQueryDevtools } from "react-query/devtools";
import { QueryClient, QueryClientProvider } from "react-query";
import { ChakraProvider, createStandaloneToast } from "@chakra-ui/react";
import Header from "./components/Header/Header";
import Sidebar from "./components/Sidebar/Sidebar";
import { ThemeProvider } from "@emotion/react";
import theme from "./styles/theme";
import { Box } from "./styles";
import "./styles/globals.css";
import ClipLoader from "react-spinners/ClipLoader";
import { io } from "socket.io-client";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      queryFn: defaultQueryFn,
      refetchOnWindowFocus: false,
    },
  },
});

setGlobal({
  token: null,
  baseURL: {},
});

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

socket.on("connect", () => {});

const App = (props) => {
  const [token, setToken] = useGlobal("token");
  const [deployProcessStatus, setdeployProcessStatus] = useGlobal("deploy");
  const [html, setHtml] = useGlobal("html");
  const [jwtToken, setJwtToken] = useGlobal("jwtToken");
  const toast = createStandaloneToast();

  useEffect(() => {
    if (socket.disconnected) {
      socket.on("connect", () => {});
    }
  }, [socket]);

  React.useEffect(() => {
    socket.on("broadcast message", function (msg) {
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
  }, []);

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

  let routes = (
    <Switch>
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
      </Switch>
    );
  }

  let show = !localStorage.getItem("token") ? (
    <Suspense fallback={<p>Loading...</p>}>{routes}</Suspense>
  ) : (
    <Box
      display="grid"
      gridTemplateColumns={{ _: "1fr", md: "220px auto" }}
      gridTemplateAreas={{}}
      maxHeight="100%"
      height="calc(100vh)"
    >
      <Sidebar />
      <Box width="auto" gridTemplateRows="auto" backgroundColor="#ffffff">
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
    </Box>
  );

  return (
    <>
      <QueryClientProvider client={queryClient}>
        <ChakraProvider>
          <ThemeProvider theme={theme}>
            {/* <ReactQueryDevtools initialIsOpen={false} /> */}
            <Box>{show}</Box>
          </ThemeProvider>
        </ChakraProvider>
      </QueryClientProvider>
    </>
  );
};

export default App;
