# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

TPI (Trabajo Práctico Integrador) for Organización Empresarial — TUPaD.  
Telegram bot for vacation-request management, modeled after a BPMN 2.0 TO-BE process.  
Authors: Federico Moretto, Nicolás Martín.

## Running the bot

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in BOT_TOKEN and SUPERVISOR_CHAT_ID
python main.py
```

## Architecture

All code lives in the repository root.

| File | Role |
|---|---|
| `main.py` | Entry point. Sets up the Telegram bot, conversation handlers, and orchestrates the BPMN flow. |
| `archivos.py` | All CSV I/O: create files, seed initial employees, read/write employees and requests. |
| `constantes.py` | Paths (relative to `__file__`), CSV headers, seed data, request-state constants, and conversation states. |

**Data layer:** two CSV files under `datos/` — `empleados.csv` and `solicitudes.csv`. Seeded automatically on first run. To reset state, delete both CSVs.

**Request states:** `PENDIENTE` → `APROBADA` or `RECHAZADA_SUPERVISOR`; immediate rejections use `RECHAZADA_SALDO` or `EMPLEADO_INEXISTENTE`.

**Environment variables:** `BOT_TOKEN` and `SUPERVISOR_CHAT_ID` must be set in `.env` (see `.env.example`).
