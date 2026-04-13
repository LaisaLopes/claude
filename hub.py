#!/usr/bin/env python3
"""
Hub de Criação de Conteúdo — Genial Investimentos
Orquestrador principal dos agentes especializados.

Formato de ativação:
    Agentes: [lista de agentes]
    Pedido: [sua solicitação]

Exemplo:
    Agentes: Jornalista + Redator
    Pedido: Traga as principais notícias de hoje sobre juros e crie um push com isso
"""

import re
import sys
import os
from dotenv import load_dotenv

load_dotenv()

from config.prompts import CANONICAL_NAMES, AGENT_DISPLAY_NAMES
from agents import AGENT_REGISTRY

SEPARATOR = "=" * 60
AGENT_SEPARATOR = "-" * 60


def parse_request(text: str) -> tuple[list[str], str]:
    """
    Parse the activation format:
        Agentes: X + Y
        Pedido: ...

    Returns (agent_keys, pedido_text)
    Raises ValueError if format is invalid.
    """
    # Normalize line endings
    text = text.strip()

    # Extract Agentes line
    agent_match = re.search(
        r"(?i)agentes?\s*:\s*(.+?)(?:\n|$)", text
    )
    if not agent_match:
        raise ValueError(
            "Formato inválido. Use:\n"
            "  Agentes: [agente1 + agente2]\n"
            "  Pedido: [sua solicitação]"
        )

    agents_raw = agent_match.group(1).strip()

    # Extract Pedido section (everything after "Pedido:")
    pedido_match = re.search(
        r"(?i)pedido\s*:\s*(.+)", text, re.DOTALL
    )
    if not pedido_match:
        raise ValueError(
            "Formato inválido. Use:\n"
            "  Agentes: [agente1 + agente2]\n"
            "  Pedido: [sua solicitação]"
        )

    pedido = pedido_match.group(1).strip()

    # Parse agent names (split by +, , or "e")
    raw_agents = re.split(r"[+,]|\s+e\s+", agents_raw, flags=re.IGNORECASE)
    raw_agents = [a.strip().lower() for a in raw_agents if a.strip()]

    # Resolve to canonical keys
    resolved = []
    unknown = []
    seen = set()

    for raw in raw_agents:
        canonical = CANONICAL_NAMES.get(raw)
        if canonical is None:
            unknown.append(raw)
        elif canonical not in seen:
            resolved.append(canonical)
            seen.add(canonical)

    if unknown:
        available = ", ".join(CANONICAL_NAMES.keys())
        raise ValueError(
            f"Agente(s) não reconhecido(s): {', '.join(unknown)}\n"
            f"Agentes disponíveis: Biblioteca Virtual, Secretário de Conteúdo, "
            f"Redator de Comunicação, Jornalista de Mercado"
        )

    if not resolved:
        raise ValueError("Nenhum agente válido encontrado na solicitação.")

    return resolved, pedido


def run_agents(agent_keys: list[str], pedido: str) -> None:
    """Instantiate and run each requested agent, printing formatted output."""
    print(f"\n{SEPARATOR}")
    print("HUB DE CRIAÇÃO DE CONTEÚDO — GENIAL INVESTIMENTOS")
    print(SEPARATOR)

    agents_str = " + ".join(
        AGENT_DISPLAY_NAMES[k] for k in agent_keys
    )
    print(f"Agentes acionados: {agents_str}")
    print(f"\nPedido: {pedido[:120]}{'...' if len(pedido) > 120 else ''}")
    print(SEPARATOR)

    for key in agent_keys:
        display_name = AGENT_DISPLAY_NAMES[key]
        AgentClass = AGENT_REGISTRY[key]

        print(f"\n{AGENT_SEPARATOR}")
        print(f"▶ {display_name}")
        print(AGENT_SEPARATOR)
        print()

        agent = AgentClass()
        agent.run(pedido)

        print(f"\n{AGENT_SEPARATOR}\n")

    print(SEPARATOR)
    print("FIM DA RESPOSTA")
    print(SEPARATOR)


def main():
    """Entry point: reads from stdin or command-line args."""
    if len(sys.argv) > 1:
        # Input passed as command-line argument
        raw_input = " ".join(sys.argv[1:])
    else:
        # Read from stdin (multiline)
        print("Hub de Criação de Conteúdo — Genial Investimentos")
        print("Digite sua solicitação (Agentes: ... / Pedido: ...) e pressione Ctrl+D:\n")
        raw_input = sys.stdin.read()

    try:
        agent_keys, pedido = parse_request(raw_input)
    except ValueError as e:
        print(f"\nErro: {e}", file=sys.stderr)
        sys.exit(1)

    run_agents(agent_keys, pedido)


if __name__ == "__main__":
    main()
