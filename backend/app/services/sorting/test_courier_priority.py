from app.models.sort_options import SortOptions
from app.services.processing.processing_service import (
    ProcessingService,
)

JOB_ID = "20260813_204951_f0dbeb"

print("\nSTEP 1 - Creating ProcessingService...")
service = ProcessingService()
print("PASS")

print("\nSTEP 2 - Creating SortOptions...")

options = SortOptions(
    fields=[
        "courier_partner",
    ],
    courier_priority=[
        "Valmo",
        "Delhivery",
        "Shadowfax",
        "ValmoPlus",
        "Xpress Bees",
    ],
)

print("PASS")

print("\nSTEP 3 - Processing PDF...")

result = service.process_job(
    job_id=JOB_ID,
    options=options,
)

print("PASS")

print("\nOUTPUT PDF:")
print(result["output_pdf"])