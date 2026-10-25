# 🧠 MabrAIn — Local-First Multi-Agent Personal Assistant

A personal desktop assistant where specialised AI agents — each with its own domain and visual identity — are coordinated by a central orchestrator called **Obsidian**. Built on the Claude API with tool use; all personal data stays on the local machine.

> **Status:** Phase 1 (CLI + agents + tool calling) in progress. Planned phases below.

---

## 🏗️ Architecture

```
User (CLI) ──▶ Obsidian Router ──▶ intent → agent
                    │                 ├── Conscience  · file & task management
                    │                 ├── Daily       · reminders & routines
                    │                 └── News        · news, markets, current events
                    ▼
             Conversation memory (in-RAM window + SQLite)
                    │
        Core: Config · Logger · Token Budget · Path Safety
```

- **Intent routing** — Claude classifies each message into a domain (strict JSON output) and Obsidian dispatches it to the right agent
- **Tool use** — agents call real tools through the Claude tool-use API:
  - Conscience: `list_files`, `search_files`, `move_file`, `rename_file`, `create_folder`
  - Daily: `create_reminder`, `list_reminders`, `delete_reminder` (SQLite)
  - News: `search_web` (DuckDuckGo via httpx)
- **Safety** — file tools only work inside user-whitelisted folders (`ALLOWED_FOLDERS`); system paths are hard-blocked
- **Cost control** — persistent daily token budget stops runaway loops
- **Evaluation** — router eval set with an accuracy target of ≥ 85% (`tests/run_evals.py`)

## 🗺️ Roadmap
| Phase | Scope | Status |
|---|---|---|
| 0 | Environment, project structure, hello world | ✅ Done |
| 1 | CLI, Obsidian router, Conscience/Daily/News agents, tool calling, evals | 🔨 In progress |
| 2 | Electron + React + TypeScript UI, FastAPI/WebSocket streaming, LangGraph orchestration | ⏳ Planned |
| 3 | ChromaDB vector memory, voice (Whisper.cpp STT, Piper TTS) | ⏳ Planned |
| 4 | Packaging & distribution | ⏳ Planned |

Design decisions are recorded as ADRs in [`docs/adr`](docs/adr) — orchestration, UI framework, local-first data.

## 🛠️ Stack
**Now:** Python 3.11+ · Anthropic API (Claude) · tool use · SQLite · httpx · pydantic-settings · loguru
**Planned:** LangGraph · FastAPI + WebSocket · Electron + React + TypeScript · ChromaDB · Whisper.cpp · Piper TTS

## ▶️ Run (Phase 1)
```bash
git clone https://github.com/serhattay1907/MaBrain.git
cd MaBrain/backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # add ANTHROPIC_API_KEY and ALLOWED_FOLDERS
python hello_world.py       # connectivity check
python cli.py               # chat with the agents
python ../tests/run_evals.py  # router accuracy
```

Example prompts (Turkish UI): `Downloads klasöründeki dosyaları listele` · `yarın saat 10'a hatırlatma kur` · `dolar kaç TL`

## 📁 Structure
```
backend/
├── obsidian/   # orchestrator: intent router + conversation memory
├── agents/     # conscience, daily, news (+ base agent)
├── tools/      # file, reminder, web tools
├── services/   # LLM client
├── core/       # config, logger, token budget, path safety
├── cli.py
└── hello_world.py
tests/          # eval runner + eval sets
docs/adr/       # architecture decision records
docs/planning/  # project plan & build guide (Turkish)
```

## 🔒 Out of scope for V1
3D brain visualisation · mobile/watch apps · Google Calendar/Gmail · always-on wake word · multi-user

---
**Author:** Serhat Tay · developed alongside the TEKNOFEST 2026 Team Aytunga work
