from pypdf import PdfReader

from app.core.config import settings
from app.models.sort_options import SortOptions
from app.services.processing.processing_service import ProcessingService


# --------------------------------------------------
# TEST JOB
# --------------------------------------------------

JOB_ID = "20260813_204951_f0dbeb"


# --------------------------------------------------
# PATHS
# --------------------------------------------------

JOB_DIR = settings.JOBS_DIR / JOB_ID

INPUT_PDF = (
    JOB_DIR
    / "original"
    / "original.pdf"
)

OUTPUT_PDF = (
    JOB_DIR
    / "output"
    / "sorted.pdf"
)


# --------------------------------------------------
# TEST
# --------------------------------------------------

def main():

    print()
    print("=" * 60)
    print("PROCESSING SERVICE - END TO END TEST")
    print("=" * 60)

    # --------------------------------------------------
    # STEP 1 - Verify input PDF
    # --------------------------------------------------

    print()
    print("STEP 1 - Checking input PDF...")

    if not INPUT_PDF.exists():
        raise FileNotFoundError(
            f"Input PDF not found:\n{INPUT_PDF}"
        )

    print("PASS: Input PDF exists.")
    print(f"      {INPUT_PDF}")

    # --------------------------------------------------
    # STEP 2 - Create sorting options
    # --------------------------------------------------

    print()
    print("STEP 2 - Creating sorting options...")

    options = SortOptions(
        fields=[
            "courier_partner",
            "sku",
            "size",
        ]
    )

    print("PASS: SortOptions created.")
    print(f"      Fields: {options.fields}")

    # --------------------------------------------------
    # STEP 3 - Process job
    # --------------------------------------------------

    print()
    print("STEP 3 - Processing PDF...")

    service = ProcessingService()

    result = service.process_job(
        job_id=JOB_ID,
        options=options,
    )

    print("PASS: Processing completed.")

    # --------------------------------------------------
    # STEP 4 - Display result
    # --------------------------------------------------

    print()
    print("PROCESSING RESULT")
    print("-" * 60)

    for key, value in result.items():
        print(f"{key:15}: {value}")

    # --------------------------------------------------
    # STEP 5 - Verify output exists
    # --------------------------------------------------

    print()
    print("STEP 4 - Verifying output PDF...")

    if not OUTPUT_PDF.exists():
        raise AssertionError(
            "Output PDF was not created."
        )

    print("PASS: Output PDF created.")
    print(f"      {OUTPUT_PDF}")

    # --------------------------------------------------
    # STEP 6 - Verify page count
    # --------------------------------------------------

    print()
    print("STEP 5 - Verifying page count...")

    input_reader = PdfReader(
        str(INPUT_PDF)
    )

    output_reader = PdfReader(
        str(OUTPUT_PDF)
    )

    input_pages = len(input_reader.pages)
    output_pages = len(output_reader.pages)

    print(f"INPUT PAGE COUNT : {input_pages}")
    print(f"OUTPUT PAGE COUNT: {output_pages}")

    if input_pages != output_pages:
        raise AssertionError(
            "Output PDF page count does not match input."
        )

    print("PASS: Page count preserved.")

    # --------------------------------------------------
    # STEP 7 - Verify labels
    # --------------------------------------------------

    print()
    print("STEP 6 - Verifying label count...")

    label_count = result["label_count"]

    print(f"LABEL COUNT: {label_count}")

    if label_count != input_pages:
        raise AssertionError(
            "Label count does not match PDF page count."
        )

    print("PASS: All PDF pages produced labels.")

    # --------------------------------------------------
    # FINAL
    # --------------------------------------------------

    print()
    print("=" * 60)
    print("PASS: END-TO-END PROCESSING TEST")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()