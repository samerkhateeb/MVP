import { Alert, Button } from "react-bootstrap";
import React, { useEffect, useRef, useState } from "react";

import ButtonGroup from "react-bootstrap/ButtonGroup";
import InputField from "../controls/InputField";
import ToggleButton from "react-bootstrap/ToggleButton";

function RegisterComponent(props) {
  const [firstName, setFirstName] = useState();
  const [lastName, setLastName] = useState();
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  const [passwordc, setPasswordc] = useState();
  const [concent, setConcent] = useState();
  const [image, setImage] = useState();
  const [bio, setBio] = useState();
  const [error, setError] = useState();

  useEffect(() => {
    setError(concent === "false");
  }, [concent]);

  const radios = [
    { name: "Reject", value: "false" },
    { name: "Approve", value: "true" },
  ];

  function submitHandler(e) {
    e.preventDefault();

    const data = {
      firstname: firstName,
      lastname: lastName,
      password: password,
      cpassword: passwordc,
      email: email,
      concent: concent === "true",
      image: image,
      bio: bio,
    };

    if (concent) props.onSubmit(data);
    else setError(true);
  }

  return (
    <div className="card p-1">
      <form onSubmit={submitHandler}>
        <InputField title="First Name" onChange={setFirstName} />
        <InputField title="Last Name" onChange={setLastName} />
        <InputField title="Password" type="password" onChange={setPassword} />
        <InputField
          title="Repeat Password*"
          type="password"
          onChange={setPasswordc}
        />
        <InputField title="Email" onChange={setEmail} />
        <InputField title="Image" notrequied="true" onChange={setImage} />
        <InputField
          title="Bio"
          notrequied="true"
          type="textarea"
          onChange={setBio}
        />

        <ButtonGroup>
          {radios.map((radio, idx) => (
            <ToggleButton
              key={idx}
              id={`radio-${idx}`}
              type="radio"
              variant={idx % 2 ? "outline-success" : "outline-danger"}
              name="radio"
              value={radio.value}
              checked={concent === radio.value}
              onChange={(e) => setConcent(e.currentTarget.value)}
            >
              {radio.name}
            </ToggleButton>
          ))}
        </ButtonGroup>
        {error && (
          <>
            <Alert variant="danger">
              You should approve our terms and conditions to proceed your
              registration...
            </Alert>
          </>
        )}
        <br />

        <Button variant="primary mt-2" type="submit">
          register
        </Button>
      </form>
    </div>
  );
}

export default RegisterComponent;
