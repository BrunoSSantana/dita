# CLAUDE.md

Entry point for AI agents and contributors. Read this first, then follow the links.

## Quick Reference

| Topic | File |
|---|---|
| Product spec & features | [docs/spec.md](docs/spec.md) |
| Architecture & layers | [docs/architecture.md](docs/architecture.md) |
| Python/pywebview conventions | [docs/conventions.md](docs/conventions.md) |
| JS↔Python API contract | [docs/api-contract.md](docs/api-contract.md) |
| Riscos e decisões pendentes | [docs/risks.md](docs/risks.md) |

## Como implementar

As tasks estão em `tasks/`. Cada arquivo é autocontido — leia apenas o da task designada e os docs que ele referencia.

1. Veja `tasks/README.md` para o estado atual e o grafo de dependências
2. Escolha uma task `pending` com dependências `done`
3. Leia o arquivo da task — ele define interface, requisitos e acceptance criteria
4. Ao concluir: mude `status: done` no frontmatter do arquivo da task e atualize a tabela em `tasks/README.md`

Tasks que podem começar imediatamente (sem dependências): **T01, T02, T05, T08**

## Ambiente e Ferramentas

Gerenciamento de dependências via **uv**. Nunca usar `pip` diretamente.

### Pré-requisitos de sistema (Ubuntu/Debian)

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-webkit2-4.1 libportaudio2 xclip
```

Necessários para GTK/WebKit (pywebview), áudio (sounddevice) e clipboard (pyperclip).

### Comandos

```bash
make install   # cria .venv e instala tudo (deps + dev)
make run       # inicia a aplicação
make fmt       # black + isort
make lint      # ruff + isort --check
make test      # pytest tests/
```

Para adicionar dependência de produção:
```bash
uv add <pacote>
```

Para adicionar dependência de dev:
```bash
uv add --group dev <pacote>
```

O lockfile é `uv.lock` — commitar sempre junto com mudanças no `pyproject.toml`.

## Non-negotiables
- `transcriber.py`, `audio.py`, `config.py` sem imports de `backend.py` ou `frontend/`
- Todos os métodos do `backend.py` retornam `{"ok": bool, ...}` — nunca levantam exceção para o JS
- No `print()` — use `logging`
- Type hints em todas as funções públicas
- `black` + `isort` + `ruff` antes de commitar

## Stack
Python 3.11+ · pywebview · faster-whisper · sounddevice · pyperclip · pynput (ver R1) · vanilla JS

## Git
Conventional Commits · branch from `main`

Ao concluir uma task ou step importante, sempre sugira um commit com mensagem no formato Conventional Commits antes de continuar.
