"""
Base agent class for the Content Creation Hub.
All agents inherit from this class and share common API call logic.
"""

import os
import anthropic
from typing import Iterator


MODEL = "claude-opus-4-6"
MAX_TOKENS = 4096


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

    def run(self, pedido: str, stream: bool = True) -> str:
        """
        Execute the agent with the given request.
        Uses prompt caching on the system prompt to reduce cost on repeated calls.
        Returns the full response as a string.
        """
        full_response = ""

        with self.client.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=[
                {
                    "type": "text",
                    "text": self.system_prompt,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": pedido}],
        ) as stream_obj:
            for text in stream_obj.text_stream:
                print(text, end="", flush=True)
                full_response += text

        return full_response

    def run_with_context(self, pedido: str, context: list[dict]) -> str:
        """
        Execute the agent with conversation history (multi-turn).
        Useful for follow-up questions within the same session.
        """
        full_response = ""
        messages = context + [{"role": "user", "content": pedido}]

        with self.client.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=[
                {
                    "type": "text",
                    "text": self.system_prompt,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=messages,
        ) as stream_obj:
            for text in stream_obj.text_stream:
                print(text, end="", flush=True)
                full_response += text

        return full_response
