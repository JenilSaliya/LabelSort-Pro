export function getApiBaseUrl(): string {
  const envUrl = import.meta.env.VITE_API_BASE_URL;

  // If running in browser and envUrl points to localhost/127.0.0.1,
  // but the current browser is accessing from a local network IP (e.g. mobile 192.168.x.x),
  // adapt the backend host to match the client's hostname on port 8000.
  if (typeof window !== "undefined" && window.location.hostname) {
    const hostname = window.location.hostname;
    if (
      hostname !== "localhost" &&
      hostname !== "127.0.0.1" &&
      (!envUrl || envUrl.includes("localhost") || envUrl.includes("127.0.0.1"))
    ) {
      return `http://${hostname}:8000`;
    }
  }

  return envUrl || "http://localhost:8000";
}

export const API_BASE_URL = getApiBaseUrl();

export const MAX_UPLOAD_SIZE_MB = 100;
export const MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024;

export const APP_ROUTES = {
  HOME: "/",
  WORKSPACE: "/app",
  UPLOAD: "/app/upload",
  JOB: (jobId: string) => `/app/job/${jobId}`,
  ANALYSIS: (jobId: string) => `/app/job/${jobId}/analysis`,
  SORT: (jobId: string) => `/app/job/${jobId}/sort`,
  RESULT: (jobId: string) => `/app/job/${jobId}/result`,
  PREVIEW: (jobId: string) => `/app/job/${jobId}/preview`,
  HISTORY: "/app/history",
  ANALYTICS: "/app/analytics",
  SETTINGS: "/app/settings",
  API_DOCS: "/app/api-docs",
};

export const MARKETPLACE_LABELS: Record<string, { name: string; color: string; bg: string }> = {
  meesho: {
    name: "Meesho",
    color: "#E11D48",
    bg: "rgba(225, 29, 72, 0.1)",
  },
  amazon: {
    name: "Amazon",
    color: "#FF9900",
    bg: "rgba(255, 153, 0, 0.1)",
  },
  flipkart: {
    name: "Flipkart",
    color: "#2874F0",
    bg: "rgba(40, 116, 240, 0.1)",
  },
  shopify: {
    name: "Shopify",
    color: "#95BF47",
    bg: "rgba(149, 191, 71, 0.1)",
  },
};
