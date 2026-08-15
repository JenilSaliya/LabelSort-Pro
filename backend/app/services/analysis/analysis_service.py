from collections import Counter

from app.models.label import Label
from app.schemas.analysis import AnalysisResult,SortableField,FieldStatistics
from app.core.field_metadata import FIELD_METADATA

class AnalysisService:

    def analyze(
        self,
        labels: list[Label],
        marketplace: str,
    ) -> AnalysisResult:

        counters = {
            field_name: Counter()
            for field_name in FIELD_METADATA
        }

        for label in labels:

            fields = label.fields

            for field_name in FIELD_METADATA:

                value = getattr(
                    fields,
                    field_name,
                    None,
                )

                if value is None:
                    continue

                counters[field_name][
                    str(value)
                ] += 1

        field_statistics = {}

        for field_name, counter in counters.items():

            if not counter:
                continue

            field_statistics[field_name] = (
                FieldStatistics(
                    values=dict(counter)
                )
            )
        

        sortable_fields = []

        for field_name, label in (
            FIELD_METADATA.items()
        ):

            counter = counters[field_name]

            if not counter:
                continue

            sortable_fields.append(
                SortableField(
                    id=field_name,
                    label=label,
                    unique_values=len(counter),
                    total_labels=sum(
                        counter.values()
                    ),
                )
            )

        courier_priority_options = sorted(
            counters[
                "courier_partner"
            ].keys()
        )

        return AnalysisResult(
            marketplace=marketplace,

            page_count=sum(
                len(label.pages)
                for label in labels
            ),

            label_count=len(labels),

            sortable_fields=sortable_fields,

            courier_priority_options=(
                courier_priority_options
            ),

            field_statistics=field_statistics,
        )