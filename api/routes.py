from fastapi import APIRouter
from api.schemas import QueryRequest
from agents.service import answer_question
from core.llm_service import LLMService  # 👈 Importante para instanciar el LLM
import numpy as np
import pandas as pd

router = APIRouter()
llm_service = LLMService()

def sanitize_for_json(obj):
    """
    Convierte dinámicamente cualquier tipo de NumPy/Pandas o DataFrames 
    a tipos nativos de Python serializables en JSON.
    """
    # 1. Convertir DataFrames a lista de diccionarios (orient="records")
    if isinstance(obj, pd.DataFrame):
        return sanitize_for_json(obj.to_dict(orient="records"))
    
    # 2. Convertir Series de Pandas a listas
    elif isinstance(obj, pd.Series):
        return sanitize_for_json(obj.tolist())
    
    # 3. Recorrer diccionarios
    elif isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    
    # 4. Recorrer listas y tuplas
    elif isinstance(obj, (list, tuple)):
        return [sanitize_for_json(v) for v in obj]
    
    # 5. Escalares de NumPy (Enteros, Flotantes, Buleanos)
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return None if np.isnan(obj) else float(obj)
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    
    # 6. Valores nulos / NaNs escalares
    elif pd.isna(obj) if isinstance(obj, (float, int, str, np.number)) else False:
        return None
    
    # 7. Tipos que implementan .item() (escalares de numpy/pandas)
    elif hasattr(obj, "item") and callable(getattr(obj, "item")):
        return obj.item()
    
    return obj

@router.post("/query")
def query(request: QueryRequest):
    response = answer_question(
        question=request.question,
        dataset_ids=request.dataset_ids,
        dataset_relations=request.dataset_relations,
        semantic_layer=request.semantic_layer,
        inline_datasets=getattr(request, "inline_datasets", None),
        llm=llm_service  # 👈 Le pasamos el LLM instanciado
    )

    # Si la respuesta es una Dataclass (AnalyticsResponse), la convertimos a dict
    if hasattr(response, "__dict__"):
        response = response.__dict__

    # Limpiamos dinámicamente cualquier np.int64, float64 o NaN antes de responder a FastAPI
    return sanitize_for_json(response)