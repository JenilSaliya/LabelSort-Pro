export interface JobMetadata {
  job_id: string;
  status: string;
  marketplace?: string | null;
  filename?: string | null;
  file_size?: number | null;
  page_count?: number | null;
  label_groups?: number | null;
  uploaded_filenames?: string[];
  uploaded_file_count?: number;
  mime_type?: string;
  created_at: string;
  updated_at: string;
}

export type JobWorkflowStage = 
  | 'upload_completed'
  | 'marketplace_detected'
  | 'labels_extracted'
  | 'analysis_ready'
  | 'statistics_generated'
  | 'waiting_for_sort'
  | 'processing'
  | 'completed'
  | 'error';

export interface UploadResultData {
  job_id: string;
  status: string;
  marketplace?: string;
  page_count?: number;
  label_count?: number;
  uploaded_file_count?: number;
}
