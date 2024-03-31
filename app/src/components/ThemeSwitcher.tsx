import { useState, useEffect } from "react";
import { SunIcon } from "@heroicons/react/24/solid";
import { MoonIcon } from "@heroicons/react/16/solid";

const ThemeSwitcher = () => {
  const [darkMode, setDarkMode] = useState(true);

  useEffect(() => {
    const isDarkMode = localStorage.getItem("darkMode") === "true";
    setDarkMode(isDarkMode);
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
    localStorage.setItem("darkMode", darkMode.toString()); // Convert darkMode to string
  }, [darkMode]);

  const toggleDarkMode = () => {
    setDarkMode((prevMode) => !prevMode);
  };

  return (
    <button
      onClick={toggleDarkMode}
      className="px-4 py-2 rounded-md bg-slate-800 dark:bg-slate-400 text-white"
    >
      {darkMode ? <SunIcon className="h-6 w-6 text-yellow-400"></SunIcon> : <MoonIcon className="h-6 w-6 text-blue-500"></MoonIcon>}
    </button>
  );
};

export default ThemeSwitcher;
