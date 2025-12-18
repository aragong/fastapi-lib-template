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
- **Always propose a plan** before implementing changes
- **Include model recommendation** in the plan:
  - For **simple tasks** (formatting, basic CRUD, simple tests, doc updates): Recommend **Claude Haiku 4.5** to save tokens
  - For **complex tasks** (architecture, multi-file changes, debugging, optimization): Use **Claude Sonnet 4.5**
- **Always propose testing** after implementing code changes to ensure correctness via CLI commands in terminal whenever applicable, ask for confirmation running commands
- Do not generate snippets or partial code unless specifically requested
- Remind to activate virtual environment if needed before running commands (".venv" folder)
- Never add libraries or dependencies, this will be handled manually by me

### Task Complexity Classification

**Simple tasks (Haiku 4.5 recommended):**
- Code formatting and style fixes
- Adding simple endpoints following existing patterns
- Writing basic tests based on templates
- Documentation updates
- Straightforward single-file changes
- Configuration updates

**Complex tasks (Sonnet 4.5 required):**
- Architecture decisions and design
- Multi-file refactoring with dependencies
- Complex algorithm implementation
- Performance optimization
- Debugging issues with multiple potential causes
- Integration of new patterns or libraries

