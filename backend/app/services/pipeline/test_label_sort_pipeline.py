from pathlib import Path

from app.models.label import Label, LabelFields
from app.models.sort_options import SortOptions
from app.services.pipeline.label_sort_pipeline import (
    LabelSortPipeline,
)


def build_label(
    label_id: str,
    page: int,
    sku: str,
) -> Label:

    return Label(
        id=label_id,
        pages=[page],
        fields=LabelFields(
            courier_partner="Valmo",
            payment_type="COD",
            tracking_number=f"TRACK-{label_id}",
            sku=sku,
            product_name="Test Product",
            size="6-7 Years",
            quantity=1,
            color="NA",
            order_number=f"ORDER-{label_id}",
            invoice_number=f"INV-{label_id}",
            order_date="27.07.2026",
        ),
    )


def main() -> None:

    print("=" * 70)
    print("LABEL SORT PIPELINE TEST")
    print("=" * 70)

    input_pdf = Path(
        "temp/test_output/input.pdf"
    )

    output_pdf = Path(
        "temp/test_output/pipeline_sorted.pdf"
    )

    labels = [
        build_label("label-c", 3, "SKU-C"),
        build_label("label-a", 1, "SKU-A"),
        build_label("label-b", 2, "SKU-B"),
    ]

    options = SortOptions(
        fields=["sku"],
        reverse=False,
    )

    pipeline = LabelSortPipeline()

    result = pipeline.sort_labels(
        labels=labels,
        options=options,
        input_pdf=input_pdf,
        output_pdf=output_pdf,
    )

    print()
    print("SORTED LABEL ORDER")

    sorted_labels = pipeline.sorting_service.sort_labels(
        labels,
        options,
    )

    for label in sorted_labels:
        print(
            label.id,
            label.pages,
            label.fields.sku,
        )

    print()
    print("OUTPUT PDF:", result)

    assert result.exists(), (
        "Pipeline did not create output PDF."
    )

    assert result == output_pdf

    assert [
        label.fields.sku
        for label in sorted_labels
    ] == [
        "SKU-A",
        "SKU-B",
        "SKU-C",
    ]

    print()
    print("PASS: Labels sorted correctly.")
    print("PASS: Output PDF created.")
    print("PASS: Pipeline completed successfully.")

    print()
    print("=" * 70)
    print("PIPELINE TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()