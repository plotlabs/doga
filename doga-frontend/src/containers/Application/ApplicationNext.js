import { useState } from "react";
import { Box, Button, Para, Span } from "../../styles";
import Select from "react-select";
import { APIURLS } from "../../Api";
import { useQuery } from "react-query";

const ApplicationNext = ({ setStep, setConnectionSelected }) => {
  const [loading, setLoading] = useState(false);
  const [showConnectionStep, setShowConnectionStep] = useState();
  const [dbTypeSelected, setDbTypeSelected] = useState();
  const [selectedCollection, setSelectedCollection] = useState();

  const mysqlCreated = useQuery(APIURLS.dbInfo("mysql"));
  const sqliteCreated = useQuery(APIURLS.dbInfo("sqlite"));
  const postgresCreated = useQuery(APIURLS.dbInfo("postgres"));

  let sqliteOptions = [];
  if (sqliteCreated?.data?.result) {
    {
      Object.entries(sqliteCreated?.data?.result).map(([prop, val]) => {
        return sqliteOptions.push({ value: val, label: val });
      });
    }
  }
  let mysqlOptions = [];
  if (mysqlCreated?.data?.result) {
    {
      Object.entries(mysqlCreated?.data?.result).map(([prop, val]) => {
        return mysqlOptions.push({ value: val, label: val });
      });
    }
  }
  let postgresOptions = [];
  if (postgresCreated?.data?.result) {
    {
      Object.entries(postgresCreated?.data?.result).map(([prop, val]) => {
        return postgresOptions.push({ value: val, label: val });
      });
    }
  }

  const showConnectionHandler = (key) => {
    setShowConnectionStep(key);
  };
  const dbTypeSelect = (key) => {
    setDbTypeSelected(key);
  };
  const applicationNextHandler = () => {
    setConnectionSelected(selectedCollection);
    setStep(3);
  };

  let showConnection =
    showConnectionStep === 0 ? (
      <>
        <Box m={6} textAlign="center">
          <Span fontSize={6} mb={2}>
            Select Type of Db Connection you want to make
          </Span>
        </Box>
        <Box type="row" flexDirection="row" justifyContent="center">
          <Box
            background={"#6e798c38"}
            backgroundImage={
              dbTypeSelected === 0
                ? "linear-gradient(to right, #7f00ff, #8b008bd4)"
                : "#6e798c38"
            }
            m={8}
            p={6}
            borderRadius="5px"
            style={{ cursor: "pointer" }}
            onClick={() => {
              dbTypeSelect(0);
            }}
          >
            <Para
              textAlign="center"
              color={dbTypeSelected === 0 ? "white" : "blue"}
            >
              MySQl
            </Para>
          </Box>
          <Box
            background={"#6e798c38"}
            backgroundImage={
              dbTypeSelected === 1
                ? "linear-gradient(to right, #7f00ff, #8b008bd4)"
                : "#6e798c38"
            }
            borderRadius="5px"
            m={8}
            p={6}
            style={{ cursor: "pointer" }}
            onClick={() => {
              dbTypeSelect(1);
            }}
          >
            <Para
              textAlign="center"
              color={dbTypeSelected === 1 ? "white" : "blue"}
            >
              PostgreSQL
            </Para>
          </Box>
          <Box
            background={"#6e798c38"}
            backgroundImage={
              dbTypeSelected === 2
                ? "linear-gradient(to right, #7f00ff, #8b008bd4)"
                : "#6e798c38"
            }
            borderRadius="5px"
            m={8}
            p={6}
            style={{ cursor: "pointer" }}
            onClick={() => {
              dbTypeSelect(2);
            }}
          >
            <Para
              textAlign="center"
              color={dbTypeSelected === 2 ? "white" : "blue"}
            >
              sqlite
            </Para>
          </Box>
        </Box>
      </>
    ) : (
      <>
        <Box></Box>{" "}
      </>
    );

  let showDBConnection =
    dbTypeSelected === 0 ? (
      <>
        <Box
          style={{
            marginBottom: "1.5rem",
            color: "#6E798C",
            fontSize: "1.25rem",
            width: "40%",
            padding: "45px",
            paddingTop: "10px",
          }}
        >
          <Select
            key={0}
            onChange={({ value }) => setSelectedCollection(value)}
            required
            theme={CARD_ELEMENT_OPTIONS}
            placeholder="Select Mysql Connection"
            options={mysqlOptions}
          />
        </Box>
      </>
    ) : dbTypeSelected === 1 ? (
      <>
        <Box
          style={{
            marginBottom: "1.5rem",
            color: "#6E798C",
            fontSize: "1.25rem",
            width: "40%",
            padding: "45px",
            paddingTop: "10px",
          }}
        >
          <Select
            key={0}
            onChange={({ value }) => setSelectedCollection(value)}
            required
            theme={CARD_ELEMENT_OPTIONS}
            placeholder="Select PostgreSQL Connection"
            options={postgresOptions}
          />
        </Box>
      </>
    ) : dbTypeSelected === 2 ? (
      <>
        <Box
          style={{
            marginBottom: "1.5rem",
            color: "#6E798C",
            fontSize: "1.25rem",
            width: "40%",
            padding: "45px",
            paddingTop: "10px",
          }}
        >
          <Select
            key={0}
            onChange={({ value }) => setSelectedCollection(value)}
            required
            theme={CARD_ELEMENT_OPTIONS}
            placeholder="Select Sqlite Connection"
            options={sqliteOptions}
          />
        </Box>
      </>
    ) : null;

  return (
    <>
      <Box display="grid" gridTemplateColumns="1fr" gridGap={8}>
        <Box type="row" flexDirection="column" justifyContent="center">
          <Box m={6} textAlign="center">
            <Span fontSize={6} mb={2}>
              Select connection for your Application
            </Span>
            {/* <Box my={2} borderBottom="4px solid" borderColor="orange"></Box> */}
          </Box>

          <Box type="row" flexDirection="row" justifyContent="center">
            <Box
              // boxShadow={!showConnectionStep ? "orangeShadow" : null}
              background={"#6e798c38"}
              backgroundImage={
                !showConnectionStep
                  ? "linear-gradient(to right, #7f00ff, #8b008bd4)"
                  : "#6e798c38"
              }
              borderRadius="5px"
              m={8}
              p={6}
              style={{ cursor: "pointer" }}
              onClick={() => {
                showConnectionHandler(0);
              }}
            >
              <Para
                textAlign="center"
                color={!showConnectionStep ? "white" : "blue"}
              >
                Choose from existing connections
              </Para>
            </Box>
            <Box
              background={"#6e798c38"}
              backgroundImage={
                showConnectionStep
                  ? "linear-gradient(to right, #7f00ff, #8b008bd4)"
                  : "#6e798c38"
              }
              m={8}
              p={6}
              borderRadius="5px"
              style={{ cursor: "pointer" }}
              onClick={() => {
                showConnectionHandler(1);
              }}
            >
              <Para
                textAlign="center"
                color={showConnectionStep ? "white" : "blue"}
              >
                create a new connection
              </Para>
            </Box>
          </Box>
          {showConnection}
          {showDBConnection}

          <Box>
            <Button onClick={applicationNextHandler}>NEXT</Button>
          </Box>
        </Box>
      </Box>
    </>
  );
};

const CARD_ELEMENT_OPTIONS = {
  style: {
    base: {
      color: "#32325d",
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: "antialiased",
      fontSize: "18px",
      "::placeholder": {
        color: "#aab7c4",
      },
    },
    invalid: {
      color: "#fa755a",
      iconColor: "#fa755a",
    },
  },
};

export default ApplicationNext;
