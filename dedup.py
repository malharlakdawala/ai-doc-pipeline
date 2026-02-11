"""Document deduplication using content hashing."""

import hashlib
from chunker import Chunk


def deduplicate_chunks(chunks: list[Chunk]) -> list[Chunk]:
    seen_hashes = set()
    unique = []

    for chunk in chunks:
        content_hash = hashlib.md5(chunk.text.encode()).hexdigest()
        if content_hash not in seen_hashes:
            seen_hashes.add(content_hash)
            unique.append(chunk)

    removed = len(chunks) - len(unique)
    if removed > 0:
        import logging
        logging.getLogger(__name__).info(f"Removed {removed} duplicate chunks")

    return unique
