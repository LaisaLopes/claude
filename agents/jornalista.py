"""
Jornalista de Mercado — Daily market update and content hook agent.
Monitors economic/financial scenario and suggests content angles.
"""

from agents.base import BaseAgent
from config.prompts import JORNALISTA_MERCADO


class JornalistaMercado(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Jornalista de Mercado",
            system_prompt=JORNALISTA_MERCADO,
        )
