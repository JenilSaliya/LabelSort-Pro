from pydantic import BaseModel


class SortableField(BaseModel):
    id: str
    label: str

    sortable: bool = True

    unique_values: int = 0

    total_labels: int = 0


class FieldStatistics(BaseModel):
    values: dict[str, int]


class AnalysisResult(BaseModel):
    marketplace: str

    page_count: int
    label_count: int

    sortable_fields: list[SortableField]

    courier_priority_options: list[str]
    field_statistics: dict[str, FieldStatistics]
