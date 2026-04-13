"""
Base agent class for the Content Creation Hub.
All agents inherit from this class and share common API call logic.
"""

import os
import anthropic
from typing import Iterator


MODEL = "claude-opus-4-6"
MAX_TOKENS = 4096


def _build_system(system_prompt: str) -> list[dict]:
    return [{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}]


class BaseAgent:
    """
    Base class for all Content Hub agents.
    Handles Anthropic API calls with prompt caching and streaming.
    """

    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )

    def stream(self, pedido: str, context: list[dict] | None = None) -> Iterator[str]:
        """
        Generator that yields text chunks as they arrive from the API.
        Used by the Streamlit UI (st.write_stream) and by run().
        Prompt caching is applied to the system prompt automatically.
        """
        messages = (context or []) + [{"role": "user", "content": pedido}]
        with self.client.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=_build_system(self.system_prompt),
            messages=messages,
        ) as stream_obj:
            yield from stream_obj.text_stream

    def run(self, pedido: str, context: list[dict] | None = None) -> str:
        """
        Execute the agent and print output to stdout (CLI mode).
        Returns the full response string.
        """
        full_response = ""
        for text in self.stream(pedido, context):
            print(text, end="", flush=True)
            full_response += text
        return full_response
