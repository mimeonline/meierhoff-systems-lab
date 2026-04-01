export default {
  content: ["./index.html", "./src/main.ts"],
  theme: {
    extend: {
      colors: {
        canvas: "#f3f0e8",
        ink: "#1d2a26",
        moss: "#35544a",
        sand: "#e7d6b5",
        ember: "#c76b4f",
        panel: "#fffaf2"
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'IBM Plex Sans'", "sans-serif"],
        mono: ["'IBM Plex Mono'", "monospace"]
      },
      boxShadow: {
        soft: "0 18px 45px rgba(38, 53, 46, 0.12)"
      },
      keyframes: {
        rise: {
          "0%": { opacity: "0", transform: "translateY(18px)" },
          "100%": { opacity: "1", transform: "translateY(0)" }
        },
        pulseLine: {
          "0%, 100%": { opacity: "0.5" },
          "50%": { opacity: "1" }
        }
      },
      animation: {
        rise: "rise 500ms ease-out both",
        pulseLine: "pulseLine 2.6s ease-in-out infinite"
      }
    }
  },
  plugins: []
};
