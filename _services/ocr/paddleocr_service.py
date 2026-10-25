import tempfile
from paddleocr import PaddleOCR


class OCRService:

    def __init__(self):

        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang="en"
        )

    def extract_text(self, file_bytes):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".png"
        ) as f:

            f.write(file_bytes)
            temp_path = f.name

        result = self.ocr.ocr(temp_path)

        lines = []

        for page in result:
            for item in page:

                text = item[1][0]
                score = item[1][1]

                if score > 0.4:
                    lines.append(text)

        return "\n".join(lines)