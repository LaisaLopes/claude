"""
Biblioteca Virtual — Knowledge base agent for Genial Investimentos.
Serves as the single source of truth about products, services and communications.
"""

from agents.base import BaseAgent
from config.prompts import BIBLIOTECA_VIRTUAL


class BibliotecaVirtual(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Biblioteca Virtual",
            system_prompt=BIBLIOTECA_VIRTUAL,
        )
