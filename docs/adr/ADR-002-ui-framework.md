# ADR-002: UI Framework

**Date:** 2026-05  
**Status:** Accepted

## Decision
Electron + React + TypeScript for the desktop UI. FastAPI + WebSocket for UI↔Backend communication.

## Reasoning
- Developer already has frontend skills (React/TypeScript)
- Electron enables single distributable for Windows + Linux
- WebSocket supports streaming (token-by-token response display)
- Backend stays as independent Python process — UI just connects to it

## Alternatives Considered
- PyQt6: less flexible UI, steeper learning curve for this developer
- Tauri: requires Rust, adds new language dependency
