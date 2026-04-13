"""
Secretário de Conteúdo — Operational and strategic support agent.
Handles briefings, compliance prep, calendars and task organization.
"""

from agents.base import BaseAgent
from config.prompts import SECRETARIO_CONTEUDO


class SecretarioConteudo(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Secretário de Conteúdo",
            system_prompt=SECRETARIO_CONTEUDO,
        )
