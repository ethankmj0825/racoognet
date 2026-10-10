# racoogent 🦝

**A local-first AI agent that lives on your Linux**

Your data stays on your machine. Racoogent connects powerful cloud LLMs to your local system through a secure interconnection service.

### Why racoogent?
Most AI agents live in the cloud. Racoogent lives on *your* Linux. You control the sandbox, the files, and the tools.

## Features
- 🔌 **Interconnection Service** - LLM <-> System hub
- 🧠 **Multi-LLM** - openai, gemini, deepseek, llama (Ollama Cloud), alibaba
- 🛠️ **Tools** - run_shell, read_file with sandboxed execution
- 🔗 **MCP** - Connect any MCP server
- 💳 **Clawlink** - Premium connectors

## Quick Start
```bash
pip install racoogent
racoogent first-setup
racoogent chat
```

## Commands
```bash
racoogent chat
racoogent models
racoogent use gpt-oss:120b
racoogent mcp list
racoogent clawlink status
```

## License
MIT
