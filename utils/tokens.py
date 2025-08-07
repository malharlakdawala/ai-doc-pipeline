"""Token counting utilities."""

import tiktoken


def count_tokens(text: str, model: str = "cl100k_base") -> int:
    enc = tiktoken.get_encoding(model)
    return len(enc.encode(text))


def truncate_to_tokens(text: str, max_tokens: int, model: str = "cl100k_base") -> str:
    enc = tiktoken.get_encoding(model)
    tokens = enc.encode(text)
    if len(tokens) <= max_tokens:
        return text
    return enc.decode(tokens[:max_tokens])
