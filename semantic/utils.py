import json
import os
import hashlib

def get_dataset_id(source_type, config):
    base = f"{source_type}_{str(config)}"
    return hashlib.md5(base.encode()).hexdigest()

def save_semantic_layer(dataset_id, semantic_layer):
    os.makedirs("semantic_store", exist_ok=True)
    path = f"semantic_store/{dataset_id}.json"

    with open(path, "w") as f:
        json.dump(semantic_layer, f, indent=2)

def load_semantic_layer(dataset_id):
    path = f"semantic_store/{dataset_id}.json"

    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None

def list_semantic_files():
    path = "semantic_store"
    if not os.path.exists(path):
        return []
    return [f for f in os.listdir(path) if f.endswith(".json")]

def load_semantic_file(file_name):
    path = os.path.join("semantic_store", file_name)
    with open(path) as f:
        return json.load(f)