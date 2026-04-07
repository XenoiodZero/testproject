"""
LLM client supporting OpenRouter (OpenAI-compatible) and Anthropic Claude.
Handles building the RAG prompt and calling the model.
"""

from openai import OpenAI


SYSTEM_PROMPT = """You are a helpful AI assistant in a Discord server.
You answer questions using the provided context from the knowledge base.
If the context doesn't contain relevant information, say so honestly.
Keep responses concise and conversational — this is Discord, not an essay."""


def _build_user_content(question: str, context_chunks: list[dict]) -> str:
    if context_chunks:
        context_text = "\n\n".join(
            f"[Source: {c['source']}]\n{c['text']}" for c in context_chunks
        )
        return (
            f"Use the following context to answer the question.\n\n"
            f"--- CONTEXT ---\n{context_text}\n--- END CONTEXT ---\n\n"
            f"Question: {question}"
        )
    return (
        f"No relevant context was found in the knowledge base.\n\n"
        f"Question: {question}\n\n"
        f"Answer based on your general knowledge, but note that "
        f"no specific documents were found."
    )


class LLMClient:
    def __init__(self, api_key: str, model: str = "meta-llama/llama-3-8b-instruct:free"):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model = model

    def generate(self, question: str, context_chunks: list[dict]) -> str:
        """Generate a response using retrieved context + the user's question."""
        user_content = _build_user_content(question, context_chunks)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                ],
                max_tokens=1024,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {e}"


class ClaudeClient:
    """LLM client using the Anthropic Claude API."""

    def __init__(self, api_key: str, model: str = "claude-opus-4-6"):
        from anthropic import Anthropic

        self.client = Anthropic(api_key=api_key)
        self.model = model

    def generate(self, question: str, context_chunks: list[dict]) -> str:
        user_content = _build_user_content(question, context_chunks)
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0.7,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_content}],
            )
            return "".join(
                block.text for block in response.content if getattr(block, "type", None) == "text"
            )
        except Exception as e:
            return f"Error generating response: {e}"
