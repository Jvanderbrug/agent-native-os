import type { Config } from "tailwindcss";

// Design tokens lifted verbatim from STYLE.md (the AI Build Lab field-manual aesthetic).
// If you change a value here, change it in src/styles/tokens.css too.
const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        paper: "#F5F2EB",
        "paper-2": "#EBE7DE",
        "paper-3": "#DDD7CA",
        surface: "#FFFFFF",
        terminal: "#080808",
        ink: "#0F0F0F",
        "ink-2": "#4A4A52",
        "ink-3": "#7A7A85",
        border: "#0F0F0F",
        lime: "#C8FF00",
        "lime-dim": "#A8D600",
        caution: "#FF3300",
        blueprint: "#0055FF",
        success: "#00D084",
      },
      fontFamily: {
        display: ["Space Grotesk", "sans-serif"],
        body: ["Inter", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      boxShadow: {
        offset: "3px 3px 0 #0F0F0F",
        "offset-md": "5px 5px 0 #0F0F0F",
        "offset-lg": "9px 9px 0 #0F0F0F",
      },
      backgroundImage: {
        grid: "linear-gradient(rgba(15,15,15,0.055) 1px, transparent 1px), linear-gradient(90deg, rgba(15,15,15,0.055) 1px, transparent 1px)",
      },
      backgroundSize: {
        grid: "46px 46px",
      },
    },
  },
  plugins: [],
};

export default config;
