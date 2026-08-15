from collections import Counter

from app.models.label import Label
from app.models.label import LabelFields
from app.services.analysis.analysis_service import (
    AnalysisService,
)


labels = [

    Label(
        id="1",
        pages=[1],
        fields=LabelFields(
            courier_partner="Valmo",
            sku="SKU-A",
            size="2-3 Years",
            quantity=1,
            color="NA",
        ),
    ),

    Label(
        id="2",
        pages=[2],
        fields=LabelFields(
            courier_partner="Valmo",
            sku="SKU-A",
            size="2-3 Years",
            quantity=1,
            color="NA",
        ),
    ),

    Label(
        id="3",
        pages=[3],
        fields=LabelFields(
            courier_partner="Delhivery",
            sku="SKU-B",
            size="3-4 Years",
            quantity=1,
            color="Red",
        ),
    ),
]


service = AnalysisService()

result = service.analyze(
    labels=labels,
    marketplace="meesho",
)

print(result.model_dump())