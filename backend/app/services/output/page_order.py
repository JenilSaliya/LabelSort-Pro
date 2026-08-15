from app.models.label import Label


class PageOrderBuilder:
    """
    Converts sorted Label objects into the physical
    PDF page order required for output generation.

    Multi-page labels remain together.
    """

    @staticmethod
    def build(labels: list[Label]) -> list[int]:
        """
        Return PDF page numbers in their required output order.
        """

        page_order: list[int] = []

        for label in labels:
            page_order.extend(label.pages)

        return page_order