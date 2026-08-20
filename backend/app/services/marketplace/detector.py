from enum import Enum


class Marketplace(str, Enum):
    MEESHO = "meesho"
    AMAZON = "amazon"
    FLIPKART = "flipkart"
    AJIO = "ajio"
    MYNTRA = "myntra"
    SHOPIFY = "shopify"
    UNKNOWN = "unknown"


class MarketplaceDetector:
    """
    Detects e-commerce marketplace from label page text.
    Supports both full invoice pages and cropped label-only pages.
    """

    def detect(self, text: str) -> Marketplace:
        text = text.lower()

        # -----------------------------
        # Meesho (Full & Cropped)
        # -----------------------------
        if "product details" in text and (
            "sku" in text
            or "order no" in text
            or "purchase order no." in text
            or "destination code" in text
            or "return code" in text
        ):
            return Marketplace.MEESHO

        if "meesho" in text:
            return Marketplace.MEESHO

        # -----------------------------
        # Amazon
        # -----------------------------
        if "amazon" in text or "amazon transportation services" in text:
            return Marketplace.AMAZON

        # -----------------------------
        # Flipkart
        # -----------------------------
        if "flipkart" in text or "ekart" in text:
            return Marketplace.FLIPKART

        # -----------------------------
        # Ajio
        # -----------------------------
        if "ajio" in text:
            return Marketplace.AJIO

        # -----------------------------
        # Myntra
        # -----------------------------
        if "myntra" in text:
            return Marketplace.MYNTRA

        # -----------------------------
        # Shopify
        # -----------------------------
        if "shopify" in text:
            return Marketplace.SHOPIFY

        return Marketplace.UNKNOWN