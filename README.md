# ⚡ vibe2prompt

*Turn vague vibes into precise, technical prompts — ready for any AI agent.*

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Powered by Gemini](https://img.shields.io/badge/powered_by-Gemini%202.5%20Flash-purple.svg)](https://ai.google.dev/)

---

## Description

vibe2prompt transforms informal, off-the-cuff ideas ("make a button that increments a counter") into structured, technical prompts — copy-paste ready for **Cursor**, **Claude Code**, **Windsurf**, or **ChatGPT**.

Stop wrestling with vague instructions. Type how you feel, and get back a well-formed spec your AI tool can actually build.

## Features

- **Textual TUI** with a polished Claude Code / OpenCode aesthetic — dark Catppuccin palette, block-style banner, and a clean chat-like layout.
- **Gemini 2.5 Flash** integration for fast, high-quality prompt compilation.
- **Clipboard auto-copying** — generated prompts are copied instantly (`Ctrl+Y` to re-copy).
- **Keyboard scrolling** — `PageUp` / `PageDown` to browse long outputs even while typing.
- **Local execution** — everything runs on your machine; nothing leaves your terminal except the API request.

## Installation

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/vibe2prompt.git
cd vibe2prompt
pip install -e .
```

## Configuration

Set your Gemini API key as an environment variable:

```bash
export GEMINI_API_KEY="your_key"
```

## Usage

Launch the TUI:

```bash
v2p
```

| Shortcut      | Action                         |
| ------------- | ------------------------------ |
| `PageUp`      | Scroll up                      |
| `PageDown`    | Scroll down                    |
| `Ctrl+Y`      | Copy prompt to clipboard       |
| `Ctrl+C`      | Exit                           |

Type an informal idea into the input box, press `Enter`, and watch it compile into a structured technical prompt.

## License

MIT