import { Button } from "react-bootstrap";
import React from "react";

function LoginComponent(props) {
  function submitHandler(e) {
    e.preventDefault();
    props.onSubmit();
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
