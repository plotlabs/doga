import { MotionBox, Box, Button, Span, StyledLink } from "../../styles";
// import Link from "next/link";

const AdminProfile = (user, handleLogout) => {
  return (
    <MotionBox
      key={2}
      bg="white"
      boxShadow="invisionHover"
      width="fit-content"
      initial={{ y: -50, opacity: 0 }}
      animate={{
        y: 0,
        opacity: 1,
      }}
      p={4}
      type="column"
    >
      <Span color="blue" fontSize={6} mb={2}>
        {"Nishant"}
      </Span>
      {/* <Span>{user?.email}</Span> */}
      <Box my={4} borderBottom="4px solid" borderColor="orange"></Box>
      {/* <Link href="/dashboard">
        <StyledLink mt={4}>Dashboard</StyledLink>
      </Link> */}

      {/* <Link href="/account">
        <StyledLink mt={4}>Account</StyledLink>
      </Link> */}
      {/* {!isAdmin && (
        <Link href="http://help.lessonbee.com/en/">
          <StyledLink mt={4} href="http://help.lessonbee.com/en/">
            Help
          </StyledLink>
        </Link>
      )} */}

      <Button type="link" onClick={handleLogout} fontSize={5} mt={4}>
        Logout
      </Button>
    </MotionBox>
  );
};

export default AdminProfile;
