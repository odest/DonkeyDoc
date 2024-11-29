import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

const DropZone = () => {
  const [fileNames, setFileNames] = useState([]);

  const onDrop = useCallback((acceptedFiles) => {
    setFileNames(acceptedFiles.map(file => file.name));
    console.log("Uploaded Files:", acceptedFiles);
  }, []);

  const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
    onDrop,
    noClick: true,
    noKeyboard: true,
  });

  const handlePaste = () => {
    navigator.clipboard.readText().then((text) => {
      console.log("Pasted Data:", text);
      setFileNames([text]);
    });
  };

  return (
    <div {...getRootProps({ className: "dropzone" })}>
      <input {...getInputProps()} />
      {isDragActive ? (
        <p>Drop the file(s) here</p>
      ) : (
        <>
          <p>
            <b>Drag & Drop File(s) Here</b>
          </p>
          <p>or</p>
          <div style={{ display: "flex", gap: "10px" }}>
            <button onClick={open}>Select File(s)</button>
            <button onClick={handlePaste}>Paste File(s)</button>
          </div>
        </>
      )}

      <div style={{ marginTop: "20px", textAlign: "center" }}>
        <h4>Uploaded Files:</h4>
        {fileNames.length > 0 ? (
          <ul>
            {fileNames.map((fileName, index) => (
              <li key={index}>{fileName}</li>
            ))}
          </ul>
        ) : (
          <p>No file selected or pasted yet.</p>
        )}
      </div>
    </div>
  );
};

export default DropZone;
