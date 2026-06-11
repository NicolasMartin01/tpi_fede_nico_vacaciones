# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

TPI (Trabajo Práctico Integrador) for Organización Empresarial — TUPaD.  
Simulates a vacation-request chatbot modeled after a BPMN 2.0 TO-BE process.  
Authors: Federico Moretto, Nicolás Martín.

## Running the chatbot

```bash
cd codigo
python main.py
```

The script must be run from inside `codigo/` because file paths in `constantes.py` are relative (`datos/empleados.csv`, `datos/solicitudes.csv`).

## Architecture

The code lives entirely in `codigo/` with no external dependencies beyond the Python standard library.

| File | Role |
|---|---|
| `main.py` | Entry point. Orchestrates the BPMN flow: validate employee → check balance → save request → supervisor decision → approve/reject. |
| `archivos.py` | All CSV I/O: create files, seed initial employees, read/write employees and requests. |
| `constantes.py` | Paths, CSV headers, seed data, and request-state string constants. |
| `validaciones.py` | Input helpers (`pedir_legajo`, `pedir_numero`, `pedir_respuesta`) that loop until valid input is received. |

**Data layer:** two CSV files under `codigo/datos/` — `empleados.csv` (legajo, nombre, dias_disponibles) and `solicitudes.csv` (id, legajo, nombre, dias, estado, observacion). `crear_archivos()` seeds them on first run. To reset state, delete or empty both CSVs.

**Request states:** `PENDIENTE` → `APROBADA` or `RECHAZADA_SUPERVISOR`; immediate rejections use `RECHAZADA_SALDO` or `EMPLEADO_INEXISTENTE`.

## Repository layout

```
bpmn/       BPMN 2.0 diagrams (AS-IS / TO-BE) in .drawio and Excalidraw formats
codigo/     Python chatbot simulator
docs/       Project brief (PDF)
```
