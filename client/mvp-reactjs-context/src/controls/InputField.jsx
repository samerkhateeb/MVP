import React, { useEffect, useRef, useState } from "react";

function InputField(props) {
  return (
    <div className="form-group m-2">
      <label>{props.title}</label>
      {props.type === "textarea" ? (
        <textarea
          name="w3review"
          rows="4"
          cols="50"
          onChange={(e) => {
            props.onChange(e.target.value);
          }}
          className="form-control"
          aria-describedby={props.title}
        />
      ) : (
        <input
          type={props.type || "text"}
          required
          value={props.value}
          onChange={(e) => {
            props.onChange(e.target.value);
          }}
          className="form-control"
          aria-describedby={props.title}
        />
      )}

      <small className="form-text text-muted">{props.small} </small>
    </div>
  );
}

export default InputField;
