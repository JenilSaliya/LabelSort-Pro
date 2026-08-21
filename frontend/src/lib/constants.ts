export function getApiBaseUrl(): string {
  // 1. Desktop Mode: Check for Tauri/Electron injected URL or port
  if (typeof window !== "undefined") {
    const customApiUrl = (window as any).__LABELSORT_API_URL__;
    if (customApiUrl) {
      return customApiUrl;
    }
    const customPort = (window as any).__LABELSORT_PORT__;
    if (customPort) {
      return `http://127.0.0.1:${customPort}`;
    }
  }

  // 2. Web Mode: Environment variable from Vite build
  const envUrl = import.meta.env.VITE_API_BASE_URL;

  // 3. Mobile / Local Network adaptation
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

export const DESKTOP_DOWNLOAD_URL = "https://github.com/JenilSaliya/LabelSort-Pro/releases/latest";

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
