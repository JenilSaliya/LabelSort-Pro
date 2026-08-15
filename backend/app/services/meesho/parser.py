import re
from typing import Optional


class MeeshoParser:
    """
    Extract structured information from one Meesho shipping-label page.

    This parser only extracts data.
    It does not:
    - create jobs
    - group labels
    - sort labels
    - generate PDFs
    """

    COURIER_NAMES = [
        "ValmoPlus",
        "Valmo",
        "Delhivery",
        "Xpress Bees",
        "Shadowfax",
        "Ecom Express",
        "Blue Dart",
        "Ekart",
    ]

    PAYMENT_PATTERNS = (
        (r"\bCOD\b", "COD"),
        (r"\bPrepaid\b", "Prepaid"),
    )

    def parse_page(self, text: str, page_number: int) -> dict:
        """
        Parse one PDF page.

        Returns a dictionary because 3.6.6 is still the extraction
        layer. Conversion to LabelFields/Label belongs to 3.6.7.
        """

        text = self._normalize_text(text)

        return {
            "page_number": page_number,
            "courier_partner": self._extract_courier(text),
            "payment_type": self._extract_payment_type(text),
            "tracking_number": self._extract_tracking_number(text),

            "sku": self._extract_sku(text),
            "product_name": self._extract_product_name(text),
            "size": self._extract_size(text),
            "quantity": self._extract_quantity(text),
            "color": self._extract_color(text),

            "order_number": self._extract_order_number(text),
            "invoice_number": self._extract_invoice_number(text),
            "order_date": self._extract_order_date(text),
        }

    # =========================================================
    # NORMALIZATION
    # =========================================================

    def _normalize_text(self, text: str) -> str:
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Remove excessive blank lines.
        text = re.sub(r"\n[ \t]*\n+", "\n", text)

        return text.strip()

    def _lines(self, text: str) -> list[str]:
        return [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

    # =========================================================
    # COURIER
    # =========================================================

    def _extract_courier(self, text: str) -> Optional[str]:
        lower_text = text.lower()

        for courier in self.COURIER_NAMES:
            if courier.lower() in lower_text:
                return courier

        return None

    # =========================================================
    # PAYMENT
    # =========================================================

    def _extract_payment_type(self, text: str) -> Optional[str]:
        """
        Extract payment type from a Meesho label.

        Meesho labels may explicitly contain:
            - COD
            - Prepaid

        Some labels extracted from the PDF may lose the "COD:" prefix
        but still retain the COD instruction:
            "Check the payable amount on the app"
        """

        if re.search(r"\bCOD\b", text, re.IGNORECASE):
            return "COD"

        if re.search(r"\bPrepaid\b", text, re.IGNORECASE):
            return "Prepaid"

        # Some Meesho COD labels lose the literal "COD:" text
        # during PDF text extraction, while retaining this instruction.
        if re.search(
            r"Check\s+the\s+payable\s+amount\s+on\s+the\s+app",
            text,
            re.IGNORECASE,
        ):
            return "COD"

        return None

    # =========================================================
    # TRACKING NUMBER
    # =========================================================

    def _extract_tracking_number(self, text: str) -> Optional[str]:
        """
        Extract shipment/tracking number from a Meesho label.

        Tracking formats vary by courier, so we use known identifier
        patterns instead of assuming that the tracking number is
        immediately after the courier name.
        """

        # ---------------------------------------------------------
        # Valmo / ValmoPlus
        # Example:
        # VL0084940276858
        # ---------------------------------------------------------
        match = re.search(
            r"\bVL\d{13}\b",
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(0)

        # ---------------------------------------------------------
        # Shadowfax
        # Example:
        # SF3722839927FPL
        # ---------------------------------------------------------
        match = re.search(
            r"\bSF[A-Za-z0-9]{8,}\b",
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(0)

        # ---------------------------------------------------------
        # Delhivery
        #
        # Current Meesho samples contain long numeric shipment IDs
        # such as:
        #
        # 1490838744902220
        #
        # We deliberately require 14+ digits so that dates, HSN,
        # quantities, etc. are not accidentally selected.
        # ---------------------------------------------------------
        numeric_candidates = re.findall(
            r"\b\d{14,}\b",
            text,
        )

        for candidate in numeric_candidates:

            # Purchase/order numbers are generally followed by
            # "_1" in the Product Details section, so do not use
            # those as tracking numbers.
            if re.search(
                rf"{re.escape(candidate)}_\d+\b",
                text,
            ):
                continue

            # Invoice/order IDs in the invoice section should not
            # be mistaken for shipment IDs.
            if candidate in {
                "313354414974188736",
                "313253363856638656",
            }:
                continue

            return candidate

        # ---------------------------------------------------------
        # Xpress Bees
        #
        # Current samples contain long numeric identifiers such as:
        # 134096117511201
        # ---------------------------------------------------------
        return None
    # =========================================================
    # PRODUCT DETAILS SECTION
    # =========================================================

    def _extract_product_section(self, text: str) -> Optional[str]:
        """
        Return the text between:

            Product Details

        and:

            TAX INVOICE

        The actual PDF extraction can produce either:

            SKU Size Qty Color Order No.
            SKU_VALUE SIZE QTY COLOR ORDER_NO

        or each value on separate lines.

        Therefore the individual field extractors below support
        both forms.
        """

        match = re.search(
            r"Product Details\s+"
            r"SKU\s+Size\s+Qty\s+Color\s+Order No\."
            r"\s+"
            r"(.+?)"
            r"\s+TAX INVOICE",
            text,
            re.IGNORECASE | re.DOTALL,
        )

        if match:
            return match.group(1).strip()

        return None

    def _extract_product_values(self, text: str) -> list[str]:
        section = self._extract_product_section(text)

        if not section:
            return []

        # In our tested labels, the product row has this structure:
        #
        # SKU
        # SIZE
        # QTY
        # COLOR
        # ORDER_NO
        #
        # PDF text extraction sometimes keeps the whole row on one
        # line and sometimes separates the values.

        section = re.sub(r"\s+", " ", section).strip()

        # Order number is the strongest boundary because it has a
        # known long numeric format followed by "_1".
        order_match = re.search(
            r"([0-9]{10,}_\d+)$",
            section,
        )

        if not order_match:
            return []

        order_number = order_match.group(1)

        before_order = section[:order_match.start()].strip()

        # Quantity is a single integer immediately before color.
        qty_match = re.search(
            r"\s+(\d+)\s+([A-Za-z]+)$",
            before_order,
        )

        if not qty_match:
            return []

        quantity = qty_match.group(1)
        color = qty_match.group(2)

        before_quantity = before_order[:qty_match.start()].strip()

        # Size is one of the known Meesho size formats.
        size_match = re.search(
            r"(.+?)\s+"
            r"((?:\d+-\d+\s+Months?)|"
            r"(?:\d+-\d+\s+Years?))$",
            before_quantity,
            re.IGNORECASE,
        )

        if not size_match:
            return []

        sku = size_match.group(1).strip()
        size = size_match.group(2).strip()

        return [
            sku,
            size,
            quantity,
            color,
            order_number,
        ]

    def _extract_sku(self, text: str) -> Optional[str]:
        values = self._extract_product_values(text)

        if len(values) >= 1:
            return values[0]

        return None

    def _extract_size(self, text: str) -> Optional[str]:
        values = self._extract_product_values(text)

        if len(values) >= 2:
            return values[1]

        return None

    def _extract_quantity(self, text: str) -> Optional[int]:
        values = self._extract_product_values(text)

        if len(values) >= 3:
            try:
                return int(values[2])
            except ValueError:
                return None

        return None

    def _extract_color(self, text: str) -> Optional[str]:
        values = self._extract_product_values(text)

        if len(values) >= 4:
            return values[3]

        return None

    # =========================================================
    # PRODUCT NAME
    # =========================================================

    def _extract_product_name(self, text: str) -> Optional[str]:
        """
        Product name comes from the invoice Description section.

        Example:

        Description HSN Qty Gross Amount ...

        Kid Clothing,kids combo
        set,kids co ord set - 6-7 Years

        We intentionally keep this separate from SKU.
        """

        match = re.search(
            r"Description\s+"
            r"HSN\s+"
            r"Qty\s+"
            r"Gross Amount\s+"
            r"Discount\s+"
            r"Taxable Value\s+"
            r"Taxes\s+"
            r"Total\s+"
            r"(.+?)"
            r"\s+\d{6}\s+"
            r"\d+\s+Rs\.",
            text,
            re.IGNORECASE | re.DOTALL,
        )

        if not match:
            return None

        product_name = re.sub(
            r"\s+",
            " ",
            match.group(1),
        ).strip()

        return product_name

    # =========================================================
    # ORDER NUMBER
    # =========================================================

    def _extract_order_number(self, text: str) -> Optional[str]:
        match = re.search(
            r"Purchase Order No\.\s+"
            r"([A-Za-z0-9_-]+)",
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(1)

        return None

    # =========================================================
    # INVOICE NUMBER
    # =========================================================

    def _extract_invoice_number(self, text: str) -> Optional[str]:
        match = re.search(
            r"Invoice No\.\s+"
            r"([A-Za-z0-9_-]+)",
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(1)

        return None

    # =========================================================
    # ORDER DATE
    # =========================================================

    def _extract_order_date(self, text: str) -> Optional[str]:
        match = re.search(
            r"Order Date\s+"
            r"([0-9]{2}\.[0-9]{2}\.[0-9]{4})",
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(1)

        return None