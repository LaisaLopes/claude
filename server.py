"""
FastAPI backend para o Hub de Criação de Conteúdo — Genial Investimentos.
Expõe os agentes via HTTP com streaming SSE.

Execução:
    uvicorn server:app --reload --port 8000
"""

import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from agents import AGENT_REGISTRY
from config.prompts import AGENT_DISPLAY_NAMES

app = FastAPI(title="Hub de Conteúdo · Genial")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    agents: list[str]
    pedido: str


@app.get("/")
def serve_ui():
    return FileResponse("interface.html")


@app.get("/api/agents")
def list_agents():
    return {
        key: {"display": AGENT_DISPLAY_NAMES[key]}
        for key in AGENT_REGISTRY
    }


@app.post("/api/run")
def run_hub(req: RunRequest):
    """
    Executa os agentes selecionados e retorna as respostas via SSE.

    Eventos SSE emitidos:
        agent_start  — início de cada agente
        chunk        — fragmento de texto em streaming
        agent_end    — fim de cada agente
        done         — todos os agentes concluídos
        error        — erro durante a execução
    """
    def generate():
        try:
            valid_keys = [k for k in req.agents if k in AGENT_REGISTRY]

            for key in valid_keys:
                yield f"data: {json.dumps({'event': 'agent_start', 'agent': key, 'display': AGENT_DISPLAY_NAMES[key]})}\n\n"

                agent = AGENT_REGISTRY[key]()
                for chunk in agent.stream(req.pedido):
                    yield f"data: {json.dumps({'event': 'chunk', 'agent': key, 'text': chunk})}\n\n"

                yield f"data: {json.dumps({'event': 'agent_end', 'agent': key})}\n\n"

            yield f"data: {json.dumps({'event': 'done'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'event': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
