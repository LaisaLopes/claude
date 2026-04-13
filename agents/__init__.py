"""
Agent registry for the Content Creation Hub.
Maps canonical agent keys to their class instances.
"""

from agents.biblioteca import BibliotecaVirtual
from agents.secretario import SecretarioConteudo
from agents.redator import RedatorComunicacao
from agents.jornalista import JornalistaMercado

AGENT_REGISTRY = {
    "biblioteca": BibliotecaVirtual,
    "secretario": SecretarioConteudo,
    "redator": RedatorComunicacao,
    "jornalista": JornalistaMercado,
}
