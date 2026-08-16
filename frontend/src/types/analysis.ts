export interface SortableField {
  id: string;
  label: string;
  sortable: boolean;
  unique_values: number;
  total_labels: number;
}

export interface FieldStatisticsItem {
  values: Record<string, number>;
}

export interface AnalysisResult {
  marketplace: string;
  page_count: number;
  label_count: number;
  sortable_fields: SortableField[];
  courier_priority_options: string[];
  field_statistics: Record<string, FieldStatisticsItem>;
}
