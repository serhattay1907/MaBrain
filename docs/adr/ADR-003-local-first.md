# ADR-003: Local-First Architecture

**Date:** 2026-05  
**Status:** Accepted

## Decision
All user data (reminders, conversation history, vector memory) stays on the local machine. Only LLM API calls and web search go to the internet.

## Reasoning
- Privacy: no user data on third-party servers
- Speed: no network round-trip for data access
- Cost control: no database hosting fees
- Offline resilience: system works without internet (except LLM calls)

## Trade-offs
- No sync across devices (V3+ concern)
- Backup is manual responsibility
