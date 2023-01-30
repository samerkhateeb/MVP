import { Alert, Button } from "react-bootstrap";
import React, { useEffect, useRef, useState } from "react";

import ButtonGroup from "react-bootstrap/ButtonGroup";
import FileUploadSingle from "../controls/FileUploadSingle";
import InputField from "../controls/InputField";
import ToggleButton from "react-bootstrap/ToggleButton";

function RegisterComponent(props) {
  const [firstName, setFirstName] = useState();
  const [lastName, setLastName] = useState();
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  const [passwordc, setPasswordc] = useState();
  const [concent, setConcent] = useState();
  const [images, setImages] = useState();
  // const [file, setFile] = useState();
  const [bio, setBio] = useState();
  const [error, setError] = useState();
  const [message, setMessage] = useState();

  useEffect(() => {
    if (concent === "false")
      setMessage(
        "You should approve our terms and conditions to proceed your registration..."
      );
    else {
      setMessage(null);
    }
  }, [concent]);

  useEffect(() => {
    setMessage(props.message);
  }, [props.message]);

  const radios = [
    { name: "Reject", value: "false" },
    { name: "Approve", value: "true" },
  ];

  function submitHandler(e) {
    e.preventDefault();

    if (concent) {
      let data = new FormData();

      data.append("firstname", firstName);
      data.append("lastname", lastName);
      data.append("password", password);
      data.append("cpassword", passwordc);
      data.append("email", email);
      if (images) data.append("images", images, images.name);
      data.append("concent", concent === "true");
      data.append("bio", bio);
      props.onSubmit(data);
    } else setConcent("false");
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
        <FileUploadSingle title="Image" onChange={setImages} />
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
        {message && <Alert variant="danger">{message}</Alert>}
        <br />
        <Button variant="primary mt-2" type="submit">
          register
        </Button>
      </form>
    </div>
  );
}

export default RegisterComponent;
