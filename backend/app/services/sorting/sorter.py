from typing import Callable

from app.models.label import Label


class LabelSorter:
    """
    Sorts logical shipping labels.

    A Label may contain multiple PDF pages.
    Sorting operates on Label objects so their pages
    always remain together.
    """

    SUPPORTED_KEYS = {
        "courier_partner",
        "payment_type",
        "tracking_number",
        "sku",
        "product_name",
        "size",
        "quantity",
        "color",
        "order_number",
        "invoice_number",
        "order_date",
    }

    def sort(
        self,
        labels: list[Label],
        key: str | list[str],
        reverse: bool = False,
    ) -> list[Label]:
        """
        Return a new sorted list of labels.

        key can be:
            "sku"

        or:

            ["courier_partner", "payment_type", "sku"]

        Original list is not modified.
        """

        # --------------------------------------------------------
        # SINGLE-FIELD SORT
        # --------------------------------------------------------

        if isinstance(key, str):
            key_function = self._get_key_function(key)

            return sorted(
                labels,
                key=key_function,
                reverse=reverse,
            )

        # --------------------------------------------------------
        # MULTI-FIELD SORT
        # --------------------------------------------------------

        if isinstance(key, list):

            if not key:
                raise ValueError(
                    "At least one sorting field is required"
                )

            for field in key:
                if field not in self.SUPPORTED_KEYS:
                    raise ValueError(
                        f"Unsupported sorting field: {field}"
                    )

            def multi_key(label: Label) -> tuple:
                return tuple(
                    self._extract_sort_value(label, field)
                    for field in key
                )

            return sorted(
                labels,
                key=multi_key,
                reverse=reverse,
            )

        raise TypeError(
            "Sorting key must be a string or list of strings"
        )

    def sort_multiple(
        self,
        labels: list[Label],
        keys: list[str],
        reverse: bool = False,
        courier_priority: list[str] | None = None,
    ) -> list[Label]:
            """
            Sort labels using multiple fields.
    
            Fields are applied in the order supplied.
    
            Example:
    
                ["courier_partner", "payment_type", "sku"]
    
            means:
    
                1. courier_partner
                2. payment_type
                3. sku
    
            The original list is not modified.
            """
    
            for key in keys:
                if key not in self.SUPPORTED_KEYS:
                    raise ValueError(
                        f"Unsupported sorting field: {key}"
                    )
    
            priority_map = {}

            if courier_priority:
                priority_map = {
                    courier.strip().lower(): index
                    for index, courier
                    in enumerate(courier_priority)
                }

            def sort_key(label: Label) -> tuple:
                return tuple(
                    self._extract_sort_value(
                        label,
                        key,
                        priority_map,
                    )
                    for key in keys
                )
    
            return sorted(
                labels,
                key=sort_key,
                reverse=reverse,
            )

    def _get_key_function(
        self,
        key: str,
    ) -> Callable[[Label], object]:

        if key not in self.SUPPORTED_KEYS:
            raise ValueError(
                f"Unsupported sorting field: {key}"
            )

        return lambda label: self._extract_sort_value(
            label,
            key,
        )

    @staticmethod
    def _extract_sort_value(
        label: Label,
        key: str,
        priority_map: dict[str, int] | None = None,
    ) -> object:

        value = getattr(label.fields, key)

        if (
            key == "courier_partner"
            and priority_map
        ):
            courier = (
                value.strip().lower()
                if value
                else ""
            )

            return priority_map.get(
                courier,
                999999,
            )

        if value is None:
            if key == "quantity":
                return -1

            return ""

        if isinstance(value, str):
            return value.strip().lower()

        return value


    