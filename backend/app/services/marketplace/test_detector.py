from app.services.marketplace.detector import (
    MarketplaceDetector,
)

sample = """
Purchase Order No.
313354414974188736

Invoice No.
he1mq27471

Product Details
"""

detector = MarketplaceDetector()

result = detector.detect(sample)

print(result)