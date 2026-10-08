import traceback
import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException

from api.schemas import QueryRequest
from agents.service import answer_question
from core.llm_service import LLMService
from connectors.duckdb import DuckDBConnector  # Instancia del conector

router = APIRouter()
llm_service = LLMService()


def sanitize_for_json(obj):
    """
    Convierte dinámicamente cualquier tipo de NumPy/Pandas o DataFrames 
    a tipos nativos de Python serializables en JSON.
    """
    if isinstance(obj, pd.DataFrame):
        return sanitize_for_json(obj.to_dict(orient="records"))
    elif isinstance(obj, pd.Series):
        return sanitize_for_json(obj.tolist())
    elif isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [sanitize_for_json(v) for v in obj]
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return None if np.isnan(obj) else float(obj)
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    elif pd.isna(obj) if isinstance(obj, (float, int, str, np.number)) else False:
        return None
    elif hasattr(obj, "item") and callable(getattr(obj, "item")):
        return obj.item()
    return obj


@router.post("/query")
def query(request: QueryRequest):
    try:
        connector = DuckDBConnector()

        response = answer_question(
            question=request.question,
            dataset_ids=request.dataset_ids,
            dataset_relations=request.dataset_relations,
            semantic_layer=request.semantic_layer,
            taxonomies=request.taxonomies,
            examples=request.examples,
            inline_datasets=getattr(
                request,
                "inline_datasets",
                None,
            ),
            inline_dataset_schema=getattr(
                request,
                "inline_dataset_schema",
                None,
            ),
            connector=connector,
            llm=llm_service,
        )

        if hasattr(response, "__dict__"):
            res_dict = response.__dict__
        elif isinstance(response, dict):
            res_dict = response
        else:
            res_dict = {}

        # Si el pipeline devolvió un error
        if "error" in res_dict and res_dict["error"]:
            raise RuntimeError(
                f"Error devuelto por el pipeline: {res_dict['error']}"
            )

        # ============================================
        # DEBUG: respuesta final que recibe el ERP
        # ============================================
        final_response = sanitize_for_json(response)

        print("\n" + "=" * 80)
        print("RESPONSE FINAL PARA ERP")
        print("=" * 80)
        print(final_response)
        print("=" * 80 + "\n")

        return final_response

    except Exception as e:
        print("\n" + "=" * 60)
        print("  TRACEBACK DETALLADO DEL ERROR EN UVICORN:")
        print("=" * 60)
        traceback.print_exc()
        print("=" * 60 + "\n")

        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la consulta: {str(e)}"
        )