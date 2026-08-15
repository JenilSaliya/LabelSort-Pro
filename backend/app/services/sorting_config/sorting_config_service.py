from app.utils.json_utils import load_json


class SortingConfigService:

    def get_config(
        self,
        analysis_path,
    ):

        analysis = load_json(
            analysis_path
        )

        return {
            "available_fields":
                analysis[
                    "available_fields"
                ],

            "field_values": {
                "courier_partner":
                    list(
                        analysis[
                            "courier_partner"
                        ].keys()
                    ),

                "sku":
                    list(
                        analysis[
                            "sku"
                        ].keys()
                    ),

                "size":
                    list(
                        analysis[
                            "size"
                        ].keys()
                    ),

                "quantity":
                    list(
                        analysis[
                            "quantity"
                        ].keys()
                    ),

                "color":
                    list(
                        analysis[
                            "color"
                        ].keys()
                    ),
            },

            "supports_custom_order": [
                "courier_partner"
            ],
        }