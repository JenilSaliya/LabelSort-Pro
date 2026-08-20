import { apiClient, parseApiError } from "@/lib/api";
import { getApiBaseUrl } from "@/lib/constants";
import { AxiosProgressEvent } from "axios";
import {
  ApiResponse,
  JobMetadata,
  AnalysisResult,
  SortingConfigResponse,
  ProcessRequest,
  ProcessResultData,
  UploadResultData,
} from "@/types";

export const labelsortApi = {
  /**
   * Health Check
   */
  async healthCheck(): Promise<{ status: string; message: string }> {
    try {
      const response = await apiClient.get("/health/");
      return response.data;
    } catch (error) {
      throw parseApiError(error);
    }
  },

  /**
   * Upload PDF Files (short-lived HTTP request returning job_id)
   */
  async uploadFiles(
    files: File[],
    onProgress?: (percentage: number) => void
  ): Promise<ApiResponse<UploadResultData>> {
    try {
      const formData = new FormData();
      files.forEach((file) => {
        formData.append("files", file);
      });

      const response = await apiClient.post<ApiResponse<UploadResultData>>(
        "/upload/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          onUploadProgress: (progressEvent: AxiosProgressEvent) => {
            if (progressEvent.total && onProgress) {
              const percent = Math.round(
                (progressEvent.loaded * 100) / progressEvent.total
              );
              onProgress(percent);
            }
          },
        }
      );

      return response.data;
    } catch (error) {
      throw parseApiError(error);
    }
  },

  /**
   * Get Job Metadata
   */
  async getJob(jobId: string): Promise<JobMetadata> {
    try {
      const response = await apiClient.get<JobMetadata>(`/job/${jobId}`);
      return response.data;
    } catch (error) {
      throw parseApiError(error);
    }
  },

  /**
   * Poll Job Status with resilient retry and exponential backoff
   */
  async pollJobStatus(
    jobId: string,
    onProgress?: (job: JobMetadata) => void,
    intervalMs: number = 1000,
    timeoutMs: number = 600000 // 10 minutes maximum polling
  ): Promise<JobMetadata> {
    const startTime = Date.now();
    let consecutiveErrors = 0;

    while (Date.now() - startTime < timeoutMs) {
      try {
        const job = await this.getJob(jobId);
        consecutiveErrors = 0; // Reset error counter on success

        if (onProgress) {
          onProgress(job);
        }

        if (job.status === "completed") {
          return job;
        }

        if (job.status === "failed") {
          throw new Error(job.error || "Job processing failed on server.");
        }
      } catch (err: any) {
        // If server explicitly returned failed job status, propagate immediately
        if (err.message && err.message.includes("Job processing failed on server")) {
          throw err;
        }

        consecutiveErrors++;
        // If 5 consecutive transient network errors occur, throw error
        if (consecutiveErrors >= 5) {
          throw new Error("Lost connection to processing server. Please check your network.");
        }

        // Exponential backoff during transient glitch (1s -> 2s -> 4s max)
        const backoffDelay = Math.min(4000, intervalMs * Math.pow(1.5, consecutiveErrors - 1));
        await new Promise((resolve) => setTimeout(resolve, backoffDelay));
        continue;
      }

      await new Promise((resolve) => setTimeout(resolve, intervalMs));
    }

    throw new Error("Job processing timed out on server. Please try again.");
  },

  /**
   * Get Label Analysis Report
   */
  async getAnalysis(jobId: string): Promise<AnalysisResult> {
    try {
      const response = await apiClient.get<AnalysisResult>(`/job/${jobId}/analysis`);
      return response.data;
    } catch (error) {
      throw parseApiError(error);
    }
  },

  /**
   * Get Sorting Configuration Options
   */
  async getSortingOptions(jobId: string): Promise<SortingConfigResponse> {
    try {
      const response = await apiClient.get<SortingConfigResponse>(
        `/jobs/${jobId}/sorting-options`
      );
      return response.data;
    } catch (error) {
      throw parseApiError(error);
    }
  },

  /**
   * Trigger Sorting & PDF Generation
   */
  async processJob(
    jobId: string,
    payload: ProcessRequest
  ): Promise<ApiResponse<ProcessResultData>> {
    try {
      const response = await apiClient.post<ApiResponse<ProcessResultData>>(
        `/process/${jobId}`,
        payload
      );
      return response.data;
    } catch (error) {
      throw parseApiError(error);
    }
  },

  /**
   * Download Sorted PDF (Blob)
   */
  async downloadSortedPdf(jobId: string): Promise<Blob> {
    try {
      const response = await apiClient.get(`/job/${jobId}/download`, {
        responseType: "blob",
      });
      return response.data;
    } catch (error) {
      throw parseApiError(error);
    }
  },

  /**
   * Download Statistics Excel (Blob)
   */
  async downloadStatistics(jobId: string): Promise<Blob> {
    try {
      const response = await apiClient.get(`/job/${jobId}/statistics`, {
        responseType: "blob",
      });
      return response.data;
    } catch (error) {
      throw parseApiError(error);
    }
  },

  /**
   * Fetch PDF Preview as Blob (for secure in-app viewer)
   */
  async getPreviewBlob(jobId: string): Promise<Blob> {
    try {
      const response = await apiClient.get(`/job/${jobId}/preview`, {
        responseType: "blob",
      });
      return response.data;
    } catch (error) {
      throw parseApiError(error);
    }
  },

  /**
   * Direct Preview URL for iframe / new tab
   */
  getPreviewUrl(jobId: string): string {
    return `${getApiBaseUrl()}/job/${jobId}/preview`;
  },
};
