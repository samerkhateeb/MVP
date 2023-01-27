import { Button } from "react-bootstrap";
import React from "react";
import { useNavigate } from "react-router-dom";

function LoginComponent(props) {
  const navigate = useNavigate();

  function submitHandler(e) {
    e.preventDefault();
    props.onSubmit();
    navigate("/account");
  }

  return (
    <form onSubmit={submitHandler}>
      <Button variant="primary m-2" type="submit">
        logout
      </Button>
    </form>
  );
}

export default LoginComponent;
