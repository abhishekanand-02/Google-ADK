# Google ADK — Agent examples

This repository is a **local workspace** for experimenting with the [Agent Development Kit (ADK) for Python](https://google.github.io/adk-docs/). Each top-level folder (except the virtual environment) is a separate **ADK app**: a Python package with `agent.py` that defines `root_agent`.

Use it as a **reference** for patterns: tools, MCP, session state, planning, and the Dev UI.

---

## Prerequisites

| Requirement | Notes |
|-------------|--------|
| **Python** | 3.10+ recommended (match your ADK version). |
| **`google-adk`** | Installed inside the project virtual environment (see [ADK installation](https://google.github.io/adk-docs/get-started/installation/)). |
| **`GOOGLE_API_KEY`** | For Gemini via Google AI Studio when not using Vertex AI. [Create a key](https://aistudio.google.com/apikey). |
| **Node.js** (optional) | Needed for MCP examples that spawn `npx` (e.g. filesystem server). |

---

## Quick start

### 1. Virtual environment

From the repo root:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install google-adk
```

Using the folder name **`.venv`** (or keeping the venv **outside** this repo) avoids the venv directory appearing as a fake “app” in the ADK Web UI when the agents root is the repository folder.

### 2. Environment variables

Copy the template and add your key:

```powershell
copy .env.example .env
```

Edit `.env`:

```env
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your_key_here
```

You can also place a `.env` **inside a specific app folder** (e.g. `name_extractor\.env`) if only that app needs extra variables. **Do not commit** `.env` — it is listed in `.gitignore`.

### 3. Run the Dev UI (recommended)

From the repo root with the venv activated:

```powershell
adk web .
```

You can also keep a local **`adk_web.cmd`** (gitignored) that `cd`s to the repo root and runs `adk.exe` from `.venv\Scripts` or `adk_venv\Scripts` with the same `adk web .` command.

That sets the **agents directory** to the repo root, so **each subfolder** with an agent appears as its own app (`customer_support`, `name_extractor`, …).

**Avoid:** running `adk web` with no path from a parent folder that also contains a directory literally named `agents` — that can register an app called `agents` by mistake. **Always** use the repo root as the agents directory for this layout, or pass that path explicitly.

---

## Repository layout

```text
google_adk/
├── adk_web.cmd          # (local) Launch ADK Web — gitignored; create from README Quick start
├── rename_venv_to_dotvenv.cmd   # (local, optional) — gitignored
├── .env.example         # Safe template (committed)
├── .gitignore           # Excludes .env, .adk, venvs, *.cmd, etc.
├── .venv/ or adk_venv/  # Local virtualenv (gitignored)
├── customer_support/    # Example app (agent.py, __init__.py, …)
├── geography_assistant/
├── MCP_assistant/
├── name_extractor/
├── …                    # Other sample apps
└── README.md
```

Each **app folder** is expected to expose `root_agent` (typically in `agent.py`). ADK discovers apps by **immediate subdirectories** of the agents root.

---

## Sample apps (reference)

| Folder | Focus |
|--------|--------|
| `problem_solver` | `BuiltInPlanner` + `ThinkingConfig` for multi-step reasoning. |
| `geography_assistant` | Custom **function tools** (e.g. capital lookup). |
| `research_assistant` | Built-in **Google Search** tool. |
| `MCP_assistant` | **MCP** filesystem tools via `npx` + `@modelcontextprotocol/server-filesystem`. |
| `travel_agent` | Multiple coordinated function tools (flights, hotels, budget). |
| `customer_support` | Tools + structured instructions (orders, refunds, escalation). |
| `name_extractor` | `output_key` and session state; includes `test_state.py` for **Runner** without the UI. |
| `model_comparison` | Config / multi-agent comparison demo. |
| `product_extractor` | Nested package layout example. |
| `customer_support_agent` | Alternate layout (`support_specialist` subfolder). |
| `adk-workspace` | Starter-style workspace from `adk create`. |

See each folder’s `agent.py` module docstring and the [ADK documentation](https://google.github.io/adk-docs/) for details.

### Runner / session state (no UI)

From the repo root, with venv activated:

```powershell
python name_extractor/test_state.py
```

Requires a valid API key in `.env` (or environment). Demonstrates `InMemorySessionService`, `Runner`, and reading `session.state` after a run.


---

## Troubleshooting

| Symptom | Likely cause |
|---------|----------------|
| **`adk_venv` or `.venv` in the app list** | Agents root is the repo folder and the venv is a **sibling** app folder. Prefer **`.venv`** as the directory name, or move the venv outside the repo. |
| **App named `agents` in the list** | The agents root was set to a **parent** of a folder named `agents`. Use the folder that **directly** contains each app, or run `adk_web.cmd` from this repo root. |
| **Session `404` when switching apps** | Session IDs are **per app**. Switching apps creates or selects a new session — expected. |
| **MCP / `npx` failures** | Install Node.js; ensure firewall allows `npx` to download the MCP server. |
| **`No root_agent found`** | That folder is missing `agent.py` / `root_agent` or is not a valid app package. |

---

## Official resources

- [ADK Python documentation](https://google.github.io/adk-docs/)
- [LLM agents](https://google.github.io/adk-docs/agents/llm-agents/)
- [Tools (function & built-in)](https://google.github.io/adk-docs/tools-custom/)
- [Session state](https://google.github.io/adk-docs/sessions/state)
- [MCP tools](https://google.github.io/adk-docs/tools-custom/mcp-tools/)

---

## License

Example code follows patterns from the ADK docs; refer to [ADK’s license](https://github.com/google/adk-python) for the library itself. Your own additions can be licensed as you choose.
