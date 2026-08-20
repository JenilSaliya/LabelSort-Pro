import re
from typing import Optional


class MeeshoParser:
    """
    Extract structured information from one Meesho shipping-label page.

    Supports both full Meesho shipping labels (with bottom TAX INVOICE section)
    and cropped Meesho labels (label-only pages without invoice).
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

    # Precompiled regular expressions for courier detection
    _COURIER_REGEX = re.compile(
        r"\b(ValmoPlus|Valmo|Delhivery|Xpress\s*Bees|Shadowfax|Ecom\s*Express|Blue\s*Dart|Ekart)\b",
        re.IGNORECASE,
    )
    _COURIER_CANONICAL = {
        "valmoplus": "ValmoPlus",
        "valmo": "Valmo",
        "delhivery": "Delhivery",
        "xpress bees": "Xpress Bees",
        "xpressbees": "Xpress Bees",
        "shadowfax": "Shadowfax",
        "ecom express": "Ecom Express",
        "ecomexpress": "Ecom Express",
        "blue dart": "Blue Dart",
        "bluedart": "Blue Dart",
        "ekart": "Ekart",
    }

    # Precompiled payment patterns
    _PAYMENT_COD = re.compile(r"\bCOD\b", re.IGNORECASE)
    _PAYMENT_PREPAID = re.compile(r"\bPrepaid\b", re.IGNORECASE)
    _PAYMENT_COD_INSTRUCTION = re.compile(
        r"Check\s+the\s+payable\s+amount\s+on\s+the\s+app",
        re.IGNORECASE,
    )

    # Precompiled tracking number patterns
    _TRACKING_VALMO = re.compile(r"\bVL\d{13}\b", re.IGNORECASE)
    _TRACKING_SHADOWFAX = re.compile(r"\bSF[A-Za-z0-9]{8,}\b", re.IGNORECASE)
    _TRACKING_NUMERIC = re.compile(r"\b\d{14,}\b")

    # Precompiled product details patterns (supports full labels and cropped labels)
    _PRODUCT_SECTION_RE = re.compile(
        r"Product Details\s+"
        r"SKU\s+Size\s+Qty\s+Color\s+Order No\."
        r"\s+"
        r"(.+?)"
        r"(?:\s+TAX INVOICE|\Z)",
        re.IGNORECASE | re.DOTALL,
    )
    _PRODUCT_SECTION_FALLBACK_RE = re.compile(
        r"Product Details\s+(?:SKU\s+Size\s+Qty\s+Color\s+Order No\.\s+)?(.+?)(?:\s+TAX INVOICE|\Z)",
        re.IGNORECASE | re.DOTALL,
    )
    _ORDER_MATCH_RE = re.compile(r"([0-9]{10,}_\d+)")
    _QTY_COLOR_RE = re.compile(
        r"\s+(\d+)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?|NA|N/A)$",
        re.IGNORECASE,
    )
    _SIZE_RE = re.compile(
        r"^(.*?)\s+("
        r"(?:\d+-\d+\s+(?:Months?|Years?))|"
        r"(?:Free\s*Size|FS)|"
        r"(?:(?:XXS|XS|S|M|L|XL|XXL|XXXL|[2-6]XL))|"
        r"(?:(?:UK|IND|US)[\s-]*\d+(?:\.\d+)?)|"
        r"(?:\d{2})|"
        r"(?:\S+)"
        r")$",
        re.IGNORECASE,
    )

    # Precompiled normalization and invoice patterns
    _WHITESPACE_RE = re.compile(r"\s+")
    _BLANK_LINES_RE = re.compile(r"\n[ \t]*\n+")
    _PRODUCT_NAME_RE = re.compile(
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
        re.IGNORECASE | re.DOTALL,
    )
    _PURCHASE_ORDER_RE = re.compile(
        r"Purchase Order No\.\s+([A-Za-z0-9_-]+)",
        re.IGNORECASE,
    )
    _INVOICE_NO_RE = re.compile(
        r"Invoice No\.\s+([A-Za-z0-9_-]+)",
        re.IGNORECASE,
    )
    _ORDER_DATE_RE = re.compile(
        r"Order Date\s+([0-9]{2}\.[0-9]{2}\.[0-9]{4})",
        re.IGNORECASE,
    )

    def parse_page(self, text: str, page_number: int) -> dict:
        """
        Parse one PDF page using a single-pass extraction pipeline.
        """
        text = self._normalize_text(text)

        # 1. Courier partner
        courier = self._extract_courier(text)

        # 2. Payment type
        payment_type = self._extract_payment_type(text)

        # 3. Tracking number
        tracking_number = self._extract_tracking_number(text)

        # 4. Product details (SKU, Size, Qty, Color) in a single pass
        sku, size, quantity, color = self._extract_product_details(text)

        # 5. Invoice Metadata (only evaluated if TAX INVOICE section is present)
        has_invoice = "TAX INVOICE" in text or "Tax Invoice" in text or "tax invoice" in text
        product_name = self._extract_product_name(text) if has_invoice else None
        order_number = self._extract_order_number(text) if has_invoice else None
        invoice_number = self._extract_invoice_number(text) if has_invoice else None
        order_date = self._extract_order_date(text) if has_invoice else None

        return {
            "page_number": page_number,
            "courier_partner": courier,
            "payment_type": payment_type,
            "tracking_number": tracking_number,
            "sku": sku,
            "product_name": product_name,
            "size": size,
            "quantity": quantity,
            "color": color,
            "order_number": order_number,
            "invoice_number": invoice_number,
            "order_date": order_date,
        }

    # =========================================================
    # NORMALIZATION
    # =========================================================

    def _normalize_text(self, text: str) -> str:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        return self._BLANK_LINES_RE.sub("\n", text).strip()

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
        match = self._COURIER_REGEX.search(text)
        if match:
            raw_key = self._WHITESPACE_RE.sub(" ", match.group(1)).strip().lower()
            return self._COURIER_CANONICAL.get(raw_key, match.group(1))

        # Fallback to direct lowercase scan if spacing differs
        lower_text = text.lower()
        for courier in self.COURIER_NAMES:
            if courier.lower() in lower_text:
                return courier

        return None

    # =========================================================
    # PAYMENT
    # =========================================================

    def _extract_payment_type(self, text: str) -> Optional[str]:
        if self._PAYMENT_COD.search(text):
            return "COD"

        if self._PAYMENT_PREPAID.search(text):
            return "Prepaid"

        if self._PAYMENT_COD_INSTRUCTION.search(text):
            return "COD"

        return None

    # =========================================================
    # TRACKING NUMBER
    # =========================================================

    def _extract_tracking_number(self, text: str) -> Optional[str]:
        # Valmo / ValmoPlus
        valmo_match = self._TRACKING_VALMO.search(text)
        if valmo_match:
            return valmo_match.group(0)

        # Shadowfax
        sf_match = self._TRACKING_SHADOWFAX.search(text)
        if sf_match:
            return sf_match.group(0)

        # Delhivery / Xpress Bees / 14+ digit identifiers
        numeric_candidates = self._TRACKING_NUMERIC.findall(text)
        for candidate in numeric_candidates:
            # Skip if part of order number (e.g. 12345678901234_1)
            if f"{candidate}_" in text:
                continue
            return candidate

        return None

    # =========================================================
    # PRODUCT DETAILS (SINGLE PASS — FULL & CROPPED LABELS)
    # =========================================================

    def _extract_product_details(
        self, text: str
    ) -> tuple[Optional[str], Optional[str], Optional[int], Optional[str]]:
        """
        Extracts SKU, Size, Quantity, and Color in a single regex pass.
        Seamlessly handles both full invoice pages and cropped label-only pages.
        """
        sec_match = self._PRODUCT_SECTION_RE.search(text)
        if not sec_match:
            sec_match = self._PRODUCT_SECTION_FALLBACK_RE.search(text)
            if not sec_match:
                return None, None, None, None

        section = self._WHITESPACE_RE.sub(" ", sec_match.group(1)).strip()

        order_match = self._ORDER_MATCH_RE.search(section)
        if not order_match:
            return None, None, None, None

        product_row = section[:order_match.end()].strip()
        before_order = product_row[:order_match.start()].strip()

        qty_color_match = self._QTY_COLOR_RE.search(before_order)
        if not qty_color_match:
            return None, None, None, None

        try:
            quantity = int(qty_color_match.group(1))
        except ValueError:
            quantity = None

        color = qty_color_match.group(2).strip()

        before_quantity = before_order[:qty_color_match.start()].strip()

        size_match = self._SIZE_RE.search(before_quantity)
        if size_match:
            sku = size_match.group(1).strip()
            size = size_match.group(2).strip()
            return sku, size, quantity, color

        return before_quantity if before_quantity else None, None, quantity, color

    # =========================================================
    # PRODUCT NAME
    # =========================================================

    def _extract_product_name(self, text: str) -> Optional[str]:
        match = self._PRODUCT_NAME_RE.search(text)
        if not match:
            return None

        return self._WHITESPACE_RE.sub(" ", match.group(1)).strip()

    # =========================================================
    # ORDER NUMBER
    # =========================================================

    def _extract_order_number(self, text: str) -> Optional[str]:
        match = self._PURCHASE_ORDER_RE.search(text)
        if match:
            return match.group(1)

        return None

    # =========================================================
    # INVOICE NUMBER
    # =========================================================

    def _extract_invoice_number(self, text: str) -> Optional[str]:
        match = self._INVOICE_NO_RE.search(text)
        if match:
            return match.group(1)

        return None

    # =========================================================
    # ORDER DATE
    # =========================================================

    def _extract_order_date(self, text: str) -> Optional[str]:
        match = self._ORDER_DATE_RE.search(text)
        if match:
            return match.group(1)

        return None