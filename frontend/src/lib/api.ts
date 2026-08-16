import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";
import { getApiBaseUrl } from "./constants";
import { ApiError } from "@/types";

export const apiClient = axios.create({
  timeout: 120000, // 2 minutes for large PDF processing
});

apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  if (!config.baseURL) {
    config.baseURL = getApiBaseUrl();
  }
  return config;
});

export function parseApiError(error: unknown): ApiError {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<any>;
    const status = axiosError.response?.status;
    const responseData = axiosError.response?.data;

    let message = "An unexpected error occurred. Please try again.";

    if (responseData) {
      if (typeof responseData === "string") {
        message = responseData;
      } else if (responseData.detail) {
        if (typeof responseData.detail === "string") {
          message = responseData.detail;
        } else if (Array.isArray(responseData.detail)) {
          message = responseData.detail.map((d: any) => d.msg || JSON.stringify(d)).join(", ");
        }
      } else if (responseData.message) {
        message = responseData.message;
      }
    } else if (axiosError.code === "ECONNABORTED") {
      message = "Request timed out. Processing might still be running or server is busy.";
    } else if (!axiosError.response) {
      message = "Cannot connect to LabelSort backend server. Please make sure the backend is running.";
    }

    // Specific status code user-friendly refinements
    if (status === 413) {
      message = "Uploaded file size exceeds server limit (Max 100MB).";
    } else if (status === 404) {
      if (message.toLowerCase().includes("job not found")) {
        message = "Sorting session not found or expired. Please upload your files again.";
      }
    } else if (status === 422) {
      message = "Invalid sorting parameters or request payload.";
    }

    return {
      message,
      statusCode: status,
      details: responseData,
    };
  }

  if (error instanceof Error) {
    return { message: error.message };
  }

  return { message: "An unknown error occurred." };
}
