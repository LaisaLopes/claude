"""
Hub de Criação de Conteúdo — Genial Investimentos
Interface visual Streamlit para os agentes especializados.

Execução:
    streamlit run app.py
"""

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from config.prompts import AGENT_DISPLAY_NAMES
from agents import AGENT_REGISTRY

# ─── Constantes ───────────────────────────────────────────────────────────────

AGENT_ICONS = {
    "biblioteca": "📚",
    "secretario": "📋",
    "redator": "✍️",
    "jornalista": "📰",
}

AGENT_DESCRIPTIONS = {
    "biblioteca": "Informações sobre produtos, regras e comunicações da Genial",
    "secretario": "Briefings, calendário editorial, organização de demandas",
    "redator": "E-mail, push notification e WhatsApp com foco em conversão",
    "jornalista": "Resumo do cenário econômico e ganchos de conteúdo",
}

GENIAL_GREEN = "#00B37E"
GENIAL_DARK = "#121214"

# ─── Configuração da página ────────────────────────────────────────────────────

st.set_page_config(
    page_title="Hub de Conteúdo · Genial",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS customizado ──────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
        /* Fonte e fundo geral */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Cabeçalho do hub */
        .hub-header {
            display: flex;
            align-items: center;
            gap: 12px;
            padding-bottom: 4px;
        }
        .hub-title {
            font-size: 1.6rem;
            font-weight: 700;
            color: #FFFFFF;
            margin: 0;
        }
        .hub-subtitle {
            font-size: 0.85rem;
            color: #8D8D99;
            margin-top: 2px;
        }

        /* Badge do agente no resultado */
        .agent-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #1C1C1F;
            border: 1px solid #323238;
            border-radius: 8px;
            padding: 6px 14px;
            font-size: 0.85rem;
            font-weight: 600;
            color: #E1E1E6;
            margin-bottom: 12px;
        }

        /* Separador de resposta */
        .response-divider {
            border: none;
            border-top: 1px solid #29292E;
            margin: 24px 0;
        }

        /* Ajuste nos expanders */
        .streamlit-expanderHeader {
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }

        /* Botão primário */
        .stButton > button[kind="primary"] {
            background-color: #00B37E !important;
            border: none !important;
            font-weight: 600 !important;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #00A36E !important;
        }

        /* Área de texto */
        .stTextArea > label {
            font-weight: 600;
            font-size: 0.9rem;
        }

        /* Oculta o footer do Streamlit */
        footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🎯 Agentes")
    st.caption("Selecione um ou mais agentes para sua demanda")
    st.divider()

    selected_agents: list[str] = []
    for key in AGENT_REGISTRY:
        icon = AGENT_ICONS[key]
        display = AGENT_DISPLAY_NAMES[key]
        desc = AGENT_DESCRIPTIONS[key]
        checked = st.checkbox(
            f"{icon} {display}",
            key=f"check_{key}",
            help=desc,
        )
        if checked:
            selected_agents.append(key)

    st.divider()
    st.markdown("**Como usar:**")
    st.markdown(
        """
        1. Selecione os agentes acima
        2. Digite seu pedido no campo principal
        3. Clique em **Executar**

        Você pode acionar **mais de um agente** por pedido — as respostas se complementam.
        """
    )
    st.divider()
    st.caption("Powered by Claude Opus · Anthropic")

# ─── Header principal ──────────────────────────────────────────────────────────

st.markdown(
    """
    <div class="hub-header">
        <div>
            <p class="hub-title">💹 Hub de Criação de Conteúdo</p>
            <p class="hub-subtitle">Genial Investimentos · Agentes Especializados</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("")  # espaço

# ─── Input ────────────────────────────────────────────────────────────────────

pedido = st.text_area(
    "Pedido",
    placeholder=(
        "Ex: Traga as principais notícias de hoje sobre a Selic e crie um push "
        "notification comunicando o impacto para os clientes da Genial."
    ),
    height=130,
    label_visibility="collapsed",
)

col_btn, col_status = st.columns([2, 8])
with col_btn:
    executar = st.button(
        "▶ Executar",
        type="primary",
        use_container_width=True,
        disabled=not selected_agents or not pedido.strip(),
    )

if not selected_agents:
    st.caption("← Selecione pelo menos um agente no menu lateral para começar.")

# ─── Execução dos agentes ─────────────────────────────────────────────────────

if executar and selected_agents and pedido.strip():
    st.divider()
    st.markdown(
        f"**Agentes acionados:** "
        + " · ".join(
            f"{AGENT_ICONS[k]} {AGENT_DISPLAY_NAMES[k]}" for k in selected_agents
        )
    )
    st.markdown("")

    for i, key in enumerate(selected_agents):
        icon = AGENT_ICONS[key]
        display = AGENT_DISPLAY_NAMES[key]

        # Badge do agente
        st.markdown(
            f'<div class="agent-badge">{icon} {display}</div>',
            unsafe_allow_html=True,
        )

        # Resposta em streaming
        with st.container():
            agent = AGENT_REGISTRY[key]()
            st.write_stream(agent.stream(pedido))

        # Separador entre agentes (exceto no último)
        if i < len(selected_agents) - 1:
            st.markdown('<hr class="response-divider">', unsafe_allow_html=True)

    st.success("✅ Concluído", icon=None)

# ─── Estado vazio ─────────────────────────────────────────────────────────────

elif not executar:
    st.markdown("")
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "📚", "Biblioteca Virtual", "Consulte produtos, regras e informações institucionais da Genial"),
        (c2, "📋", "Secretário", "Monte briefings, calendário editorial e organize suas demandas"),
        (c3, "✍️", "Redator", "Crie e-mails, pushs e mensagens WhatsApp prontos para usar"),
        (c4, "📰", "Jornalista", "Acompanhe o cenário de mercado e encontre ganchos de conteúdo"),
    ]
    for col, icon, title, desc in cards:
        with col:
            st.markdown(
                f"""
                <div style="
                    background:#1C1C1F;
                    border:1px solid #29292E;
                    border-radius:12px;
                    padding:20px 16px;
                    text-align:center;
                    height:160px;
                ">
                    <div style="font-size:2rem;margin-bottom:8px">{icon}</div>
                    <div style="font-weight:700;font-size:0.85rem;color:#E1E1E6;margin-bottom:6px">{title}</div>
                    <div style="font-size:0.78rem;color:#8D8D99;line-height:1.4">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
