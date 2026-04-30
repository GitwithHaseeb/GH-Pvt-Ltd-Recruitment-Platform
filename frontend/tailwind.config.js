/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#090b12",
        card: "#121827",
        neon: "#00f5d4"
      }
    }
  },
  plugins: []
};
