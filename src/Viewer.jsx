import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Worker, Viewer } from "@react-pdf-viewer/core";
import { dropPlugin } from '@react-pdf-viewer/drop';
import { defaultLayoutPlugin } from "@react-pdf-viewer/default-layout";
import { ThemeContext } from "./ThemeContext";

import "@react-pdf-viewer/core/lib/styles/index.css";
import '@react-pdf-viewer/drop/lib/styles/index.css';
import "@react-pdf-viewer/default-layout/lib/styles/index.css";

const ViewerPage = ({ fileUrl }) => {
  const navigate = useNavigate();
  const dropPluginInstance = dropPlugin();
  const defaultLayoutPluginInstance = defaultLayoutPlugin();
  const { theme } = useContext(ThemeContext);

  return (
    <div className={`viewer-container ${theme}`}>
      {fileUrl ? (
        <div className="viewer-container">
          <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.js">
            <Viewer
              fileUrl={fileUrl}
              plugins={[defaultLayoutPluginInstance, dropPluginInstance]}
              theme={theme}
            />
          </Worker>
        </div>
      ) : (
        <div className="text">
          <p>
            <b>No PDF file to display.</b>
          </p>
          <button onClick={() => navigate("/")}>Go Back to DropZone</button>
        </div>
      )}
    </div>
  );
};

export default ViewerPage;
