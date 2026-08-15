from pathlib import Path

from openpyxl import Workbook


class ExcelExportService:

    def export_statistics(
        self,
        analysis: dict,
        output_path: str | Path,
    ) -> Path:

        workbook = Workbook()

        default_sheet = workbook.active
        workbook.remove(default_sheet)

        field_statistics = (
            analysis.field_statistics
        )

        for field_name, data in (
            field_statistics.items()
        ):

            sheet = workbook.create_sheet(
                title=field_name[:31]
            )

            sheet.append(
                ["Value", "Count"]
            )

            values = data.values

            for value, count in (
                values.items()
            ):
                sheet.append(
                    [value, count]
                )

        workbook.save(output_path)

        return Path(output_path)