# Tasks

Cada task é um arquivo independente. Um agente deve ler apenas o arquivo da task designada + os docs referenciados nela.

## Status

| ID | Task | Status | Depende de |
|---|---|---|---|
| [T01](T01-audio.md) | `audio.py` — gravação de microfone | `done` | — |
| [T02](T02-transcriber.md) | `transcriber.py` — transcrição faster-whisper | `done` | — |
| [T03](T03-backend.md) | `backend.py` — js_api exposta ao frontend | `done` | T01, T02 |
| [T04](T04-main.md) | `main.py` — entry point e janela pywebview | `done` | T03 |
| [T05](T05-frontend-html.md) | `frontend/index.html` — estrutura HTML | `done` | — |
| [T06](T06-frontend-js.md) | `frontend/app.js` — lógica JS e bridge | `done` | T03, T05 |
| [T07](T07-packaging.md) | `install.sh` · `run.sh` · `dita.desktop` | `done` | T04, T06 |
| [T08](T08-tests.md) | `tests/` — testes de `config.py` | `done` | — |

## Grafo de Dependências

```
T01 (audio)──────┐
                 ├──→ T03 (backend) ──→ T04 (main) ──→ T07 (packaging)
T02 (transcr)───┘         ↑
                           │
T05 (html) ────→ T06 (js)─┘               T07 ←───────┘

T08 (tests/config) — sem dependências
```

## Arquivos já implementados

Não precisam de task — já existem e estão alinhados com a spec:

| Arquivo | Observação |
|---|---|
| `config.py` | `load_config()` / `save_config()` com defaults |
| `config.json` | hotkey no formato pynput |
| `hotkey.py` | `start_listener()` + `make_toggle()` via evaluate_js |
| `frontend/style.css` | glassmorphism + fix animation-delay (R5) |

## Como usar (para agentes)

1. Leia este README para entender o estado geral
2. Escolha uma task `pending` cujas dependências estejam `done`
3. Abra o arquivo da task — ele contém tudo que você precisa
4. Ao concluir, marque `status: done` no frontmatter do arquivo da task e atualize a tabela acima
