import json


class LLMOutputFormatError(Exception):
    pass


def format_examples(examples: list) -> str:
    if not examples:
        return ""
    lines = ["EJEMPLOS DE REFERENCIA (Few-Shot):"]
    for ex in examples:
        lines.append(f"Pregunta: {ex.get('question')}\nSQL: {ex.get('sql', '').strip()}\n---")
    return "\n".join(lines)


def format_taxonomies(taxonomies: dict) -> str:
    if not taxonomies:
        return ""
    return f"TAXONOMIAS Y VALORES CANONICOS:\n{json.dumps(taxonomies, indent=2, ensure_ascii=False)}"


def build_sql_prompt(
    question: str,
    semantic_layer: dict,
    taxonomies: dict = None,
    examples: list = None,
    intent: dict = None,
) -> str:
    
    examples_text = format_examples(examples or [])
    taxonomies_text = format_taxonomies(taxonomies or {})
    intent_text = f"INTENT DETECTADO: {json.dumps(intent)}\n" if intent else ""

    # Extraemos solo métricas y columnas para mantener el prompt compacto
    compact_semantic = {
        "dataset_id": semantic_layer.get("dataset_id"),
        "columns": list(semantic_layer.get("columns", {}).keys()),
        "metrics": semantic_layer.get("metrics", {}),
        "aliases": semantic_layer.get("aliases", {}),
    }

    return f"""
Eres un analista de datos experto en SQL. Genera la consulta SQL para responder a la pregunta.

METADATOS DEL DATASET:
{json.dumps(compact_semantic, indent=2, ensure_ascii=False)}

{taxonomies_text}

{examples_text}

{intent_text}

REGLAS DE ORO:
1. Responde UNICAMENTE con un JSON válido: {{"sql": "SELECT ...", "confidence": 0.95}}
2. Usa SOLO sentencias SELECT.
3. Respeta las funciones y lógica mostrada en los ejemplos Few-Shot (ej. JULIANDAY, REPLACE, etc.).
4. No agregues texto ni formato Markdown fuera del JSON.

Pregunta del usuario:
"{question}"
"""


def generate_sql_structured(
    question: str,
    semantic_layer: dict,
    llm,
    taxonomies: dict = None,
    examples: list = None,
    intent: dict = None,
) -> str:  # Retorna str
    
    if isinstance(llm, dict):
        raise TypeError(f"Se esperaba LLMService, se recibió dict: {llm}")

    prompt = build_sql_prompt(
        question=question,
        semantic_layer=semantic_layer,
        taxonomies=taxonomies,
        examples=examples,
        intent=intent,
    )

    raw = llm.generate(
        prompt,
        system_prompt="You are a senior data analyst. Return ONLY valid JSON.",
    )

    if not raw or not str(raw).strip():
        raise LLMOutputFormatError("Respuesta vacía del LLM")

    raw = str(raw).strip().replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(raw)
    except Exception as e:
        raise LLMOutputFormatError(f"Error al decodificar JSON: {raw}") from e

    if "sql" not in parsed or not isinstance(parsed["sql"], str):
        raise LLMOutputFormatError("Falta el campo 'sql' en el JSON devuelto")

    # 🔑 CORRECCIÓN: Retornar solo el string de la consulta SQL
    return parsed["sql"].strip()