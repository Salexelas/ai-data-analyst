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

    def extract_text(self, file_bytes, file_name=None):

        image = Image.open(
            io.BytesIO(file_bytes)
        )

        image = image.convert("L")
        image = image.filter(ImageFilter.SHARPEN)
        image = ImageEnhance.Contrast(image).enhance(2.0)

        image_np = np.array(image)

        results = self.reader.readtext(
            image_np,
            detail=0,
            paragraph=False
        )

        return "\n".join(results)