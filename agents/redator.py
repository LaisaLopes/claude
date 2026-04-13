"""
Redator de Comunicação — Copywriting agent for conversion and performance.
Creates email marketing, push notifications and WhatsApp messages.
"""

from agents.base import BaseAgent
from config.prompts import REDATOR_COMUNICACAO


class RedatorComunicacao(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Redator de Comunicação",
            system_prompt=REDATOR_COMUNICACAO,
        )
