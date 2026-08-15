# app/exceptions/custom_exceptions.py

class LabelSortException(Exception):
    pass


class JobNotFoundException(
    LabelSortException
):
    pass


class MarketplaceNotSupportedException(
    LabelSortException
):
    pass


class InvalidPdfException(
    LabelSortException
):
    pass