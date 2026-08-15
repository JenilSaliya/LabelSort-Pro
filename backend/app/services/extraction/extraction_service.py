import fitz

from app.models.label import Label

from app.services.marketplace.detector import (
    MarketplaceDetector,
)

from app.services.meesho.parser import (
    MeeshoParser,
)

from app.services.meesho.label_builder import (
    build_label,
)


class ExtractionService:

    def __init__(self):

        self.marketplace_detector = (
            MarketplaceDetector()
        )

        self.meesho_parser = (
            MeeshoParser()
        )

    def extract_labels(
        self,
        input_pdf,
    ) -> tuple[str, list[Label]]:

        labels: list[Label] = []

        with fitz.open(input_pdf) as pdf:

            first_page_text = (
                pdf[0].get_text("text")
            )

            marketplace = (
                self.marketplace_detector.detect(
                    first_page_text
                )
            )

            if marketplace.value != "meesho":
                raise ValueError(
                    f"Unsupported marketplace: "
                    f"{marketplace.value}"
                )

            for page_index, page in enumerate(pdf):

                page_number = (
                    page_index + 1
                )

                text = page.get_text(
                    "text"
                )

                if not text.strip():
                    continue

                parsed = (
                    self.meesho_parser.parse_page(
                        text,
                        page_number,
                    )
                )

                label = build_label(
                    parsed
                )

                labels.append(
                    label
                )

        if not labels:
            raise ValueError(
                "No labels extracted."
            )

        return (
            marketplace.value,
            labels,
        )