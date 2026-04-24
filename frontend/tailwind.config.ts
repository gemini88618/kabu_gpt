import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0e1116",
        panel: "#f7f8f3",
        line: "#d9dfd0",
        accent: "#0f8b6f",
        gold: "#d6a642"
      },
      fontFamily: {
        display: ["Avenir Next", "Hiragino Sans", "Yu Gothic", "sans-serif"]
      },
      boxShadow: {
        app: "0 18px 55px rgba(13, 20, 30, 0.16)"
      }
    }
  },
  plugins: []
};

export default config;
