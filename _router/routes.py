from ui.pages.chat import render_chat
from ui.pages.ml import render_ml
from ui.pages.charts import render_charts
from ui.pages.semantic import render_semantic
from ui.pages.data import render_data
from ui.pages.ranking import render_ranking
from ui.pages.recents import render_recents
from ui.pages.datasets import render_datasets
from dataset_editor.pages.dataset_editor import render_dataset_editor
from ui.pages.dataset_info import render_dataset_info
from ui.pages.graph_builder import render_graph_builder
from ui.pages.ocr_studio import render_ocr_studio


ROUTES = {
    "chat": render_chat,
    "ml": render_ml,
    "charts": render_charts,
    "semantic": render_semantic,
    "data_create": render_data,
    "data_external": render_data,
    "datasets_manage": render_datasets,
    "dataset_editor": render_dataset_editor,
    "dataset_info": render_dataset_info,
    "graph_builder": render_graph_builder,
    "ranking": render_ranking,
    "recents": render_recents,
    "ocr_studio": render_ocr_studio
}