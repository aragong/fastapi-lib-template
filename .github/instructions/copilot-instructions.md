---
applyTo: '**'
---

# Copilot Chat Instructions

## Language Preferences

- **Communication language**: Always respond in Spanish (español) for explanations, descriptions, and conversations
- **Code generation**: Always generate code in English, including:
  - Variable names
  - Function names
  - Comments
  - Docstrings
  - File content
  - Any generated artifacts

## Response Style

- Prioritize **short, concise answers**
- Keep implementation plans **simple with minimal steps** (ideally 3-5 steps maximum)
- Avoid lengthy explanations unless explicitly requested
- Get straight to the point

## Agent Mode Behavior

When working in agent mode:
- **Always propose testing** after implementing code changes to ensure correctness via CLI commands in terminal whenever applicable, ask for confirmation running commands.
- Do not generate spinnets or partial code unless specifically requested.
- Remind to activate virtual environment if needed before running commands (".venv" folder).
- Never add libraries or dependencies, this will be handled manually by me.

