'''import re

def extract_sql(text: str):

    # 🔥 caso 1: bloque ```sql
    match = re.search(r"```sql(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # 🔥 caso 2: cualquier SELECT
    match = re.search(r"(SELECT .*?)(;|$)", text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()

    return text.strip()'''