import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import DropZone from "./DropZone";
import ViewerPage from "./Viewer";
import ThemeProvider, { ThemeContext } from "./ThemeContext";

import "./styles/styles.css";

const App = () => {
  const [fileUrl, setFileUrl] = useState(null);

  return (
    <ThemeProvider>
      <ThemeContext.Consumer>
        {({ theme }) => (
          <div className={`app-container ${theme}`}>
            <Router>
              <Routes>
                <Route
                  path="/"
                  element={<DropZone setFileUrl={setFileUrl} />}
                />
                <Route
                  path="/viewer"
                  element={<ViewerPage fileUrl={fileUrl} />}
                />
              </Routes>
            </Router>
          </div>
        )}
      </ThemeContext.Consumer>
    </ThemeProvider>
  );
};

export default App;
