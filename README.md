<p align="center">
  <img src="https://developer.axcient.com/logo.png" alt="Public Gateway MCP" width="180"/>
</p>

<h1 align="center">Public Gateway MCP</h1>

<p align="center">
  <strong>Bring Axcient into your AI workflow — instantly. ⚡</strong>
</p>

Public Gateway MCP connects your favorite AI assistants directly to Axcient. Ask questions, pull insights, and take action — all through natural conversation. No dashboards to hunt through. No context switching. Just answers. 🚀

---

## ✨ Why you'll love it

- 🔌 **Plug and play** — Drop it into Cursor, Claude Desktop, or any MCP-compatible client and go.
- 📡 **Real data, real time** — Your AI tools work with live Axcient information, not stale snapshots.
- 🛠️ **Built for builders** — Designed for teams who want their agents to *do* things, not just talk about them.

---

## 🚀 Quick start

### Prerequisites

- [uv](https://docs.astral.sh/uv/)
- [just](https://github.com/casey/just)
- [direnv](https://direnv.net/)

### Install

```bash
git clone https://github.com/axcient/public-gateway-mcp.git
cd public-gateway-mcp
direnv allow
```

### Configure

Add your Axcient API key to the `.env` file:

```bash
API_KEY="your-api-key-here"
```

### Run

```bash
just run
```

That's it. Your MCP server is live. 🎉

---

## 🤖 Connect your AI client

Add Public Gateway MCP to your MCP client configuration and point it at the running server. Once connected, your assistant can interact with Axcient on your behalf.

> 💡 **Tip:** Restart your AI client after adding the server so it picks up the new tools.

---

## 🧰 Development

Use `just` for everything — install, run, lint, and checks:

```bash
just             # see available commands
just fix         # auto-fix lint/format issues
just check-all   # full project check before you ship
```

---

<p align="center">
  <strong>Built by <a href="https://axcient.com">Axcient</a> 💙</strong><br>
  <em>Your data. Your AI. One gateway.</em>
</p>
