import os

from dataset_editor.adapters.pandas_adapter import PandasAdapter
from dataset_editor.services.schema_service import SchemaService
from dataset_editor.services.type_service import TypeService


class EditorService:

    def __init__(self):
        self.adapter = PandasAdapter()

    def load_preview(self, file_path, limit=1000):
        return self.adapter.load_preview(file_path, limit)

    def load_schema(self, file_path):
        return SchemaService.load(os.path.basename(file_path))

    def save_schema(self, file_path, schema):
        SchemaService.save(os.path.basename(file_path), schema)

    def apply_types(self, df, schema):
        return TypeService.apply(df, schema)

    def detect_type(self, series):
        return TypeService.detect(series)

    def save_dataset(self, df, file_path):
        self.adapter.save(df, file_path)

    def build_updated_schema(self, rename_map, column_types):

        return {
            rename_map[old]: column_types[old]
            for old in rename_map
        }