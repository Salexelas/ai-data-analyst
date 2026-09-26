import requests

payload = {
    "question": "¿Cuál es la tarea con mayor prioridad y su estado?",
    "dataset_ids": ["tareas"],
    "inline_datasets": {
        "tareas": [
            {"id": 1, "titulo": "Diseñar UI", "estado": "Completado", "prioridad": "Media"},
            {"id": 2, "titulo": "Integrar API Agent", "estado": "En Progreso", "prioridad": "Alta"},
            {"id": 3, "titulo": "Testing de estres", "estado": "Pendiente", "prioridad": "Baja"}
        ]
    }
}

response = requests.post("http://127.0.0.1:8000/query", json=payload)

print("Status Code:", response.status_code)
print("Respuesta cruda:", response.text)