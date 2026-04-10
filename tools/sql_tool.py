import pandas as pd
import re


class SQLTool:

    def run(self, sql, connector, context):

        schema = connector.get_schema()
        columns = schema["column_name"].tolist()

        sql = fix_sql_columns(sql, columns)  # 🔥 FIX automático

        print("\n🧠 SQL generado FINAL:")
        print(sql)
        print("-" * 50)


        sql_upper = sql.upper()

        if not sql_upper.startswith(("SELECT", "WITH")):
            raise ValueError("SQL inválido")

        forbidden = ["DROP", "DELETE", "UPDATE", "INSERT"]

        if any(word in sql_upper for word in forbidden):
            raise ValueError("SQL peligroso")

        result = connector.execute(sql)

        context["last_result"] = result

        return result
    
def fix_sql_columns(sql, schema_columns):

    for col in schema_columns:
        if " " in col:
            # reemplaza solo si NO está ya entre comillas
            pattern = rf'(?<!")\b{re.escape(col)}\b(?!")'
            sql = re.sub(pattern, f'"{col}"', sql)

    return sql