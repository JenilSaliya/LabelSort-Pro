from pypdf import PdfReader

from app.models.sort_options import SortOptions
from app.services.processing.processing_service import ProcessingService


JOB_ID = "20260813_204951_f0dbeb"


print("STEP 1 - Creating ProcessingService...")

service = ProcessingService()

print("PASS")


print("\nSTEP 2 - Creating SortOptions...")

options = SortOptions(
    fields=[
        "courier_partner",
        "sku",
        "size",
    ],
    courier_priority=[
        "Shadowfax",
        "ValmoPlus",
        "Xpress Bees",
        "Delhivery",
        "Valmo",
    ]
)

print("PASS")


print("\nSTEP 3 - Processing job...")

result = service.process_job(
    job_id=JOB_ID,
    options=options,
)

print("PASS")


output_pdf = result["output_pdf"]

print("\nOUTPUT PDF:")
print(output_pdf)


print("\nSTEP 4 - Reading sorted PDF...")

reader = PdfReader(output_pdf)

print("PASS")


print("\nSORTED PDF ORDER\n")

for i, page in enumerate(reader.pages, start=1):

    text = page.extract_text() or ""

    if "ValmoPlus" in text:
        courier = "ValmoPlus"

    elif "Valmo" in text:
        courier = "Valmo"

    elif "Delhivery" in text:
        courier = "Delhivery"

    elif "Shadowfax" in text:
        courier = "Shadowfax"

    elif "Xpress Bees" in text:
        courier = "Xpress Bees"

    else:
        courier = "UNKNOWN"

    print(
        f"Output Page {i}: {courier}"
    )