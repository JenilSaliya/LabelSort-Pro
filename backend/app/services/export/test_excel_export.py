from app.services.export.excel_export_service import (
    ExcelExportService,
)

analysis = {
    "field_statistics": {
        "courier_partner": {
            "values": {
                "Valmo": 6,
                "Delhivery": 4,
            }
        },
        "size": {
            "values": {
                "2-3 Years": 4,
                "6-7 Years": 3,
            }
        },
    }
}

service = ExcelExportService()

path = service.export_statistics(
    analysis=analysis,
    output_path="statistics.xlsx",
)

print(path)