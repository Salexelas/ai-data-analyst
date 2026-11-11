import traceback
import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Form
from pydantic import BaseModel

from api.schemas import QueryRequest, ClientCreateRequest
from agents.service import answer_question
from core.llm_service import LLMService
from core.supabase_client import get_supabase_client
from connectors.duckdb import DuckDBConnector

router = APIRouter()
llm_service = LLMService()

class LoginRequest(BaseModel):
    email: str
    password: str


def sanitize_for_json(obj):
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


# =========================================================
# ENDPOINT DE AUTENTICACIÓN
# =========================================================
@router.post("/auth/login")
def login(request: LoginRequest):
    supabase = get_supabase_client()
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase no configurado en el backend.")
    try:
        res = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        user_id = res.user.id if hasattr(res.user, "id") else res.user.get("id")
        cliente_res = supabase.table("clients").select("*").eq("id", user_id).execute()
        
        if not cliente_res.data:
            cliente_res = supabase.table("clients").select("*").eq("email", request.email).execute()

        if not cliente_res.data:
            raise HTTPException(status_code=404, detail="Usuario sin empresa asociada en la tabla clients.")
            
        client_data = cliente_res.data[0] if cliente_res.data else {}
        nombre_empresa = client_data.get('nombre') or client_data.get('name') or "Empresa Demo SA"
        
        # --- DEFINICIÓN DINÁMICA DEL LÍMITE SEGÚN EL PLAN ---
        plan_db = str(client_data.get("plan", "bronze")).strip().lower()
        limites_por_plan = {"bronze": 10, "plata": 30, "gold": 100}
        
        # Si el plan existe en nuestro diccionario, toma ese valor; sino, usa el de la base o 100 por defecto
        limite_dinamico = limites_por_plan.get(plan_db, client_data.get("limite_datasets", 100))
        
        return {
            "success": True,
            "user": res.user.model_dump() if hasattr(res.user, "model_dump") else res.user,
            "client": {
                "id": client_data.get("id"),
                "name": nombre_empresa,
                "slug": client_data.get("slug", "empresa_demo"),
                "plan": plan_db,
                "limite_datasets": limite_dinamico  # <--- Límite dinámico inyectado
            }
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Credenciales inválidas o error: {str(e)}")


# =========================================================
# ENDPOINT DE CONSULTAS
# =========================================================
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
            inline_datasets=getattr(request, "inline_datasets", None),
            inline_dataset_schema=getattr(request, "inline_dataset_schema", None),
            connector=connector,
            llm=llm_service,
        )

        if hasattr(response, "__dict__"):
            res_dict = response.__dict__
        elif isinstance(response, dict):
            res_dict = response
        else:
            res_dict = {}

        if "error" in res_dict and res_dict["error"]:
            raise RuntimeError(f"Error devuelto por el pipeline: {res_dict['error']}")

        return sanitize_for_json(response)

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error al procesar la consulta: {str(e)}")


# =========================================================
# ENDPOINTS DE CLIENTES Y GESTIÓN DE DATASETS EN NUBE
# =========================================================
@router.get("/clients")
def get_clients():
    supabase = get_supabase_client()
    if not supabase:
        return [{"id": "default", "name": "Cliente Por Defecto", "slug": "default_client"}]
    response = supabase.table("clients").select("*").execute()
    return response.data

@router.post("/clients")
def create_client(request: ClientCreateRequest):
    supabase = get_supabase_client()
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase no configurado en el servidor.")
    response = supabase.table("clients").insert({
        "name": request.name,
        "slug": request.slug
    }).execute()
    return response.data

@router.post("/datasets/upload")
def upload_dataset(client_id: str = Form(...), file: UploadFile = File(...)):
    supabase = get_supabase_client()
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase no configurado en el backend.")
    try:
        file_path = f"{client_id}/{file.filename}"
        file_bytes = file.file.read()

        # 1. Subir a Supabase Storage (sobrescribiendo si ya existe con upsert=True)
        storage_res = supabase.storage.from_("client-datasets").upload(
            path=file_path,
            file=file_bytes,
            file_options={"upsert": "true", "content-type": file.content_type}
        )

        # 2. Verificar si ya existe un registro con este nombre para el cliente
        existing = supabase.table("datasets").select("*").eq("client_id", client_id).eq("nombre_archivo", file.filename).execute()

        if existing.data:
            # Si ya existe, actualizamos la ruta o mantenemos el registro único
            db_res = supabase.table("datasets").update({
                "file_path": file_path
            }).eq("client_id", client_id).eq("nombre_archivo", file.filename).execute()
        else:
            # Si no existe, insertamos el nuevo registro
            db_res = supabase.table("datasets").insert({
                "client_id": client_id,
                "nombre_archivo": file.filename,
                "file_path": file_path
            }).execute()

        return {"success": True, "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir dataset: {str(e)}")

# --- IMPORTANTE: /download-url DEBE IR ANTES DE /{client_id} ---
@router.get("/datasets/download-url")
def get_dataset_download_url(client_id: str = Query(...), file_path: str = Query(...)):
    supabase = get_supabase_client()
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase no configurado.")
    try:
        if not file_path.startswith(client_id):
            raise HTTPException(status_code=403, detail="No autorizado.")
        
        res = supabase.storage.from_("client-datasets").create_signed_url(file_path, 60)
        
        # Extracción segura compatible con cualquier versión de supabase-py
        if isinstance(res, str):
            signed_url = res
        elif isinstance(res, dict):
            signed_url = res.get("signedURL") or res.get("signedUrl") or res.get("data", {}).get("signedURL")
        else:
            signed_url = getattr(res, "signedURL", None) or getattr(res, "signedUrl", None)

        if not signed_url:
            raise HTTPException(status_code=500, detail=f"No se pudo extraer la URL firmada de la respuesta: {res}")

        return {"success": True, "download_url": signed_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar URL: {str(e)}")

@router.get("/datasets/{client_id}")
def get_client_datasets(client_id: str):
    supabase = get_supabase_client()
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase no configurado.")
    response = supabase.table("datasets").select("*").eq("client_id", client_id).execute()
    return response.data

@router.delete("/datasets/delete")
def delete_dataset(client_id: str = Query(...), file_path: str = Query(...)):
    supabase = get_supabase_client()
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase no configurado en el backend.")
    
    try:
        if not file_path.startswith(client_id):
            raise HTTPException(status_code=403, detail="No autorizado para eliminar este archivo.")

        supabase.storage.from_("client-datasets").remove([file_path])
        supabase.table("datasets").delete().eq("file_path", file_path).eq("client_id", client_id).execute()

        return {"success": True, "message": "Dataset eliminado correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el dataset: {str(e)}")