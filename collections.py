"""Multi-collection management for separate document projects."""

from vector_store import VectorStore


class CollectionManager:
    def __init__(self):
        self._stores: dict[str, VectorStore] = {}

    def get_store(self, name: str) -> VectorStore:
        if name not in self._stores:
            self._stores[name] = VectorStore(collection_name=name)
        return self._stores[name]

    def list_collections(self) -> list[str]:
        return list(self._stores.keys())

    def delete_collection(self, name: str):
        if name in self._stores:
            self._stores[name].reset()
            del self._stores[name]
