from app.models.label import Label
from app.models.sort_options import SortOptions
from app.services.sorting.sorter import LabelSorter


class SortingService:
    """
    High-level service responsible for sorting Label objects.

    Sorting is performed using SortOptions.
    The original label list is never modified.
    """

    def __init__(self) -> None:
        self.sorter = LabelSorter()

    def sort_labels(
        self,
        labels: list[Label],
        options: SortOptions,
    ) -> list[Label]:

        return self.sorter.sort_multiple(
            labels,
            keys=options.fields,
            reverse=options.reverse,
            courier_priority=options.courier_priority,
        )