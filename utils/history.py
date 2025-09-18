"""Query history tracking."""

import json
import os
from datetime import datetime


class QueryHistory:
    def __init__(self, path: str = ".query_history.jsonl"):
        self.path = path

    def log(self, query: str, answer: str, sources: list[str]):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "answer_length": len(answer),
            "sources": sources,
        }
        with open(self.path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def recent(self, n: int = 10) -> list[dict]:
        if not os.path.exists(self.path):
            return []
        with open(self.path) as f:
            lines = f.readlines()
        return [json.loads(l) for l in lines[-n:]]
