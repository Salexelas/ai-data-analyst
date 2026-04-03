class BaseConnector:

    def execute(self, query: str):
        raise NotImplementedError
    
    def get_schema(self):
        raise NotImplementedError

    def preview(self, limit=10):
        raise NotImplementedError