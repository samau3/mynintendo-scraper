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
      type="button"
      onClick={toggleDarkMode}
      aria-label="Toggle dark mode"
      className="rounded-md bg-slate-800 px-4 py-2 text-white focus:ring-2 focus:ring-blue-400 focus:outline-none dark:bg-slate-400"
    >
      {darkMode ? (
        <SunIcon className="h-6 w-6 text-yellow-400"></SunIcon>
      ) : (
        <MoonIcon className="h-6 w-6 text-blue-500"></MoonIcon>
      )}
    </button>
  );
};

export default ThemeSwitcher;
