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

    def detect(self, text: str) -> Marketplace:

        text = text.lower()

        # -----------------------------
        # Meesho
        # -----------------------------

        if (
            "purchase order no." in text
            and "invoice no." in text
            and "product details" in text
        ):
            return Marketplace.MEESHO

        # -----------------------------
        # Amazon
        # -----------------------------

        if (
            "amazon" in text
            or "amazon transportation services" in text
        ):
            return Marketplace.AMAZON

        # -----------------------------
        # Flipkart
        # -----------------------------

        if (
            "flipkart" in text
            or "ekart" in text
        ):
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