# ADR-001: Orchestration Framework

**Date:** 2026-05  
**Status:** Accepted

## Decision
LangGraph is used for agent orchestration (Phase 2+). Phase 1 uses a lightweight intent classifier (direct Claude API call) without a full state machine.

## Reasoning
- LangGraph provides production-grade state machine with built-in debugging
- Phase 1 starts simple (no LangGraph dependency) to validate core logic first
- Phase 2 migrates to full LangGraph StateGraph once routing is proven

## Alternatives Considered
- CrewAI: less control over state, heavier abstraction
- Manual routing: viable for Phase 1, doesn't scale to 5+ agents
