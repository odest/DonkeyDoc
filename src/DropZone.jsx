import React from "react";
import { useDropzone } from "react-dropzone";
import { useNavigate } from "react-router-dom";

const DropZone = ({ setFileUrl }) => {
  const navigate = useNavigate();

  const onDrop = (acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      const url = URL.createObjectURL(file);
      setFileUrl(url);
      navigate("/viewer");
    }
  };

  const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
    onDrop,
    accept: "application/pdf",
    noClick: true,
    noKeyboard: true,
  });

  return (
    <div {...getRootProps({ className: "dropzone" })}>
      <input {...getInputProps()} />
      {isDragActive ? (
        <p>Drop the file here...</p>
      ) : (
        <>
          <p>
            <b>Drag & Drop a PDF File Here</b>
          </p>
          <p>or</p>
          <button onClick={open}>Select a PDF File</button>
        </>
      )}
    </div>
  );
};

export default DropZone;
