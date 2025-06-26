"""Answer generation using Claude."""

import anthropic
from config import Config


class AnswerGenerator:
    SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on provided context.
Always cite your sources using [Source N] notation. If the context doesn't contain
enough information to answer the question, say so clearly. Do not make up information."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    def generate(self, query: str, context: str) -> str:
        user_message = f"""Context:
{context}

Question: {query}

Please answer the question based on the provided context. Cite sources using [Source N] notation."""

        response = self.client.messages.create(
            model=Config.MODEL,
            max_tokens=2048,
            system=self.SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.content[0].text

    def generate_streaming(self, query: str, context: str):
        user_message = f"""Context:
{context}

Question: {query}

Please answer the question based on the provided context. Cite sources using [Source N] notation."""

        with self.client.messages.stream(
            model=Config.MODEL,
            max_tokens=2048,
            system=self.SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        ) as stream:
            for text in stream.text_stream:
                yield text
