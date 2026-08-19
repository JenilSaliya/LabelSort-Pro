"""
Field metadata — single source of truth for label field definitions.

Used by AnalysisService to build sortable field lists and statistics.
Enriched with `sortable` flag and complete field coverage from the
Label model.
"""

FIELD_METADATA = {
    "courier_partner": {
        "label": "Courier Partner",
        "sortable": True,
    },
    "payment_type": {
        "label": "Payment Type",
        "sortable": True,
    },
    "sku": {
        "label": "SKU",
        "sortable": True,
    },
    "product_name": {
        "label": "Product Name",
        "sortable": True,
    },
    "size": {
        "label": "Size",
        "sortable": True,
    },
    "quantity": {
        "label": "Quantity",
        "sortable": True,
    },
    "color": {
        "label": "Color",
        "sortable": True,
    },
    "order_number": {
        "label": "Order Number",
        "sortable": True,
    },
    "invoice_number": {
        "label": "Invoice Number",
        "sortable": True,
    },
    "order_date": {
        "label": "Order Date",
        "sortable": True,
    },
    "tracking_number": {
        "label": "Tracking Number",
        "sortable": False,
    },
}