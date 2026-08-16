import { SortableField } from './analysis';

export interface SortingConfigResponse {
  sortable_fields: SortableField[];
  courier_priority_options: string[];
  field_values: Record<string, string[]>;
  supports_custom_order: string[];
}

export interface SortFieldSelection {
  id: string;
  label: string;
  enabled: boolean;
}
