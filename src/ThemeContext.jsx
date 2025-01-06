import React, { createContext, useEffect, useState } from "react";

export const ThemeContext = createContext();

const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState("light");

  useEffect(() => {
    const darkThemeMq = window.matchMedia("(prefers-color-scheme: dark)");
    setTheme(darkThemeMq.matches ? "dark" : "light");

    const handleThemeChange = (e) => {
      setTheme(e.matches ? "dark" : "light");
    };

    darkThemeMq.addEventListener("change", handleThemeChange);

    return () => {
      darkThemeMq.removeEventListener("change", handleThemeChange);
    };
  }, []);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export default ThemeProvider;
