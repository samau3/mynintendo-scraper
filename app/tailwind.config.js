/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'selector',
  theme: {
    screens: {
      'xs': '445px',
      ...defaultTheme.screens,
    },
    extend: {},
  },
  plugins: [],
}

