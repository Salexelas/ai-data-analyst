'''import logging

logger = logging.getLogger(__name__)

class SQLTool:

    def run(self, sql, connector, context):

        logger.info("Executing SQL", extra={"query": sql})

        return connector.execute(sql)'''