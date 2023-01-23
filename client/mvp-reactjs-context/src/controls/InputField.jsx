import React, { useEffect, useRef, useState } from "react";

function InputField(props) {
  return (
    <div className="form-group">
      <label>{props.title}</label>
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
      <small className="form-text text-muted">{props.small} </small>
    </div>
  );
}

export default InputField;
