"""
LLM client using the Anthropic Claude API.
"""

import base64
from anthropic import Anthropic


SYSTEM_PROMPT = """You are a helpful AI assistant in a Discord server.
You answer questions using the provided context from the knowledge base.
If the context doesn't contain relevant information, say so honestly.
Keep responses concise and conversational — this is Discord, not an essay."""


def _build_user_content(
    question: str,
    context_chunks: list[dict],
    user_memory: list[str] | None = None,
    server_context: str | None = None,
) -> str:
    parts = []

    if server_context:
        parts.append(f"--- SERVER CONTEXT ---\n{server_context}\n--- END SERVER CONTEXT ---")
    if user_memory:
        mem = "\n".join(f"- {m}" for m in user_memory)
        parts.append(f"--- USER MEMORY ---\n{mem}\n--- END USER MEMORY ---")

    if context_chunks:
        ctx = "\n\n".join(
            f"[Source: {c['source']}]\n{c['text']}" for c in context_chunks
        )
        parts.append(f"--- CONTEXT ---\n{ctx}\n--- END CONTEXT ---")
        parts.append(f"Question: {question}")
        return "\n\n".join(parts)

    parts.append(
        f"No relevant context was found in the knowledge base.\n\n"
        f"Question: {question}\n\n"
        f"Answer based on your general knowledge."
    )
    return "\n\n".join(parts)


class ClaudeClient:
    """LLM client using the Anthropic Claude API."""

    def __init__(self, api_key: str, model: str = "claude-opus-4-6"):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def generate(
        self,
        question: str,
        context_chunks: list[dict],
        user_memory: list[str] | None = None,
        server_context: str | None = None,
    ) -> str:
        user_content = _build_user_content(question, context_chunks, user_memory, server_context)
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_content}],
            )
            return "".join(
                b.text for b in response.content if getattr(b, "type", None) == "text"
            )
        except Exception as e:
            return f"Error generating response: {e}"

    def generate_with_attachments(
        self,
        question: str,
        context_chunks: list[dict],
        attachments: list[dict] | None = None,
        user_memory: list[str] | None = None,
        server_context: str | None = None,
    ) -> str:
        """attachments: [{"kind": "image"|"text", "media_type", "data": bytes, "filename"}]"""
        text_part = _build_user_content(question, context_chunks, user_memory, server_context)
        blocks: list[dict] = []

        for att in attachments or []:
            if att["kind"] == "image":
                blocks.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": att["media_type"],
                        "data": base64.standard_b64encode(att["data"]).decode("utf-8"),
                    },
                })
            elif att["kind"] == "text":
                decoded = att["data"].decode("utf-8", errors="replace")
                blocks.append({
                    "type": "text",
                    "text": f"[Attached file: {att['filename']}]\n{decoded}",
                })

        blocks.append({"type": "text", "text": text_part})

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": blocks}],
            )
            return "".join(
                b.text for b in response.content if getattr(b, "type", None) == "text"
            )
        except Exception as e:
            return f"Error generating response: {e}"
