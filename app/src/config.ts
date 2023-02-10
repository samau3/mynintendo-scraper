export const BACKEND_BASE_URL =
  process.env.NODE_ENV === "production"
    ? "https://mynintendo-scraper.fly.dev/"
    : "http://127.0.0.1:5000";
