import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          950: "#0b1220",
          900: "#0f1a2e",
          800: "#152238",
        },
      },
      borderRadius: {
        xl: "0.875rem",
      },
    },
  },
  plugins: [],
};

export default config;
