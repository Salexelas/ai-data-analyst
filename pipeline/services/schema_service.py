from core.observability import log_event


class SchemaService:

    def load(self, connector):

        schema = connector.get_schema()

        columns = schema[
            "column_name"
        ].tolist()

        log_event(
            "schema_loaded",
            "system",
            columns=len(columns)
        )

        return schema, columns