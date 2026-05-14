'''import pandas as pd
import re


class OCRParserService:

    def parse_invoice(self, text):

        lines = text.split("\n")

        data = []

        i = 0

        while i < len(lines):

            line = lines[i].strip()

            # detecta descripción
            if any(word in line.upper() for word in [
                "ALICATE",
                "PINZA",
                "ALMADANA",
                "LLAVE"
            ]):

                descripcion = line

                try:
                    cant = lines[i + 2].strip()
                    precio = lines[i + 3].strip()

                    data.append({
                        "descripcion": descripcion,
                        "cant": cant,
                        "precio_unitario": precio
                    })

                except:
                    pass

            i += 1

        return pd.DataFrame(data)

'''