from app.utils.json_utils import load_json


class SortingConfigService:

    def get_config(
        self,
        analysis_path,
    ):

        analysis = load_json(
            analysis_path
        )

        field_values = {}

        for field_id, field_data in (
            analysis["field_statistics"]
            .items()
        ):
            field_values[field_id] = list(
                field_data["values"]
                .keys()
            )

        return {
            "sortable_fields":
                analysis[
                    "sortable_fields"
                ],

            "courier_priority_options":
                analysis[
                    "courier_priority_options"
                ],

            "field_values":
                field_values,

            "supports_custom_order": [
                "courier_partner"
            ],
        }