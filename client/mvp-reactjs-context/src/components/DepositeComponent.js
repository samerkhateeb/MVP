import { Alert, Button } from "react-bootstrap";

import React from "react";

function DepositeComponent(props) {
  function submitHandler(e) {
    e.preventDefault();
    props.onSubmit();
  }

  return (
    <form onSubmit={submitHandler}>
      <Button variant="primary m-2" type="submit">
        {props.text || "Reset Deposite?"}
      </Button>
    </form>
  );
}

export default DepositeComponent;
