import io
import easyocr
import numpy as np

from PIL import Image, ImageEnhance, ImageFilter


class OCRService:

    def __init__(self):

        self.reader = easyocr.Reader(
            ["es", "en"],
            gpu=False
        )

    def extract_text(self, file_bytes):

        image = Image.open(
            io.BytesIO(file_bytes)
        )

        image = image.convert("L")
        image = image.filter(ImageFilter.SHARPEN)
        image = ImageEnhance.Contrast(image).enhance(2.5)

        image_np = np.array(image)

        results = self.reader.readtext(
            image_np,
            detail=1,
            paragraph=False
        )

        rows = []

        for result in results:

            bbox, text, conf = result

            if conf < 0.25:
                continue

            x = bbox[0][0]
            y = bbox[0][1]

            rows.append({
                "x": x,
                "y": y,
                "text": text
            })

        # ordenar visualmente
        rows = sorted(
            rows,
            key=lambda r: (round(r["y"] / 20), r["x"])
        )

        return "\n".join(
            [
                r["text"]
                for r in rows
            ]
        )