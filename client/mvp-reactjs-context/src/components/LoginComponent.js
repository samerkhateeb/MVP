import React, { useRef, useState } from "react";

import { Button } from "react-bootstrap";
import InputField from "../controls/InputField";

function LoginComponent(props) {
  const [nameV, setNameV] = useState();
  const [password, setPassword] = useState();

  function submitHandler(e) {
    e.preventDefault();

    const _data = {
      username: nameV,
      password: password,
    };

    props.onSubmit(_data);
  }

  return (
    <div className="card p-1">
      <form onSubmit={submitHandler}>
        <InputField title="User Name" onChange={setNameV} />
        <InputField title="Password" type="password" onChange={setPassword} />
        <Button variant="primary mt-2" type="submit">
          login
        </Button>
      </form>
    </div>
  );
}

export default LoginComponent;
