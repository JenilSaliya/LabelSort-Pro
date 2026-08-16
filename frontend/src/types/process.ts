export interface ProcessRequest {
  fields: string[];
  reverse?: boolean;
  courier_priority?: string[];
}

export interface ProcessResultData {
  job_id: string;
  status: string;
  marketplace: string;
  input_pdf: string;
  output_pdf: string;
  page_count: number;
  label_count: number;
}
