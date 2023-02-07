import React, { useState } from "react";

import Badge from "react-bootstrap/Badge";
import { label } from "react-bootstrap";

function FileUploadSingle(props) {
  const [selectedFile, setSelectedFile] = useState(null);

  // On file select (from the pop up)
  function onFileChange(event) {
    setSelectedFile(event.target.files[0]);
    props.onChange(event.target.files[0]);
  }

  // On file upload (click the upload button)
  function onFileUpload() {
    // Create an object of formData
    const formData = new FormData();
    // Update the formData object
    const file = selectedFile;
    formData.append("myFile", file, file.name);
  }

  // File content to be displayed after
  // file upload is complete
  const fileData = selectedFile ? (
    <div>
      <h6>
        {selectedFile.type} | {selectedFile.lastModifiedDate.toDateString()}
      </h6>
    </div>
  ) : (
    <div />
  );

  // 👇 files is not an array, but it's iterable, spread to get an array of files
  return (
    <div className="m-2">
      <label className="m-2">{props.title}</label>
      <input type="file" onChange={onFileChange} />

      {Object.entries(fileData.props).length !== 0 && (
        <Badge bg="success">{fileData}</Badge>
      )}
    </div>
  );
}

export default FileUploadSingle;
