import time
import hashlib
import json


class SimpleCache:
    def __init__(self, ttl=300):
        self.store = {}
        self.ttl = ttl

    def get(self, key):
        item = self.store.get(key)

        if not item:
            return None

        if time.time() - item["ts"] > self.ttl:
            del self.store[key]
            return None

        return item["value"]

    def set(self, key, value):
        self.store[key] = {
            "value": value,
            "ts": time.time()
        }


def build_cache_key(question, dataset_id, semantic_layer, intent, language):
    base = {
        "q": question,  # 🔥 IMPORTANTE: ahora sí incluimos la query
        "dataset": dataset_id,
        "semantic": semantic_layer,
        "intent": intent,
        "lang": language
    }

    raw = json.dumps(base, sort_keys=True, default=str)
    return hashlib.md5(raw.encode()).hexdigest()