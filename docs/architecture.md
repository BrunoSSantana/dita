# Architecture

## Layer Diagram

```
┌────────────────────────────────────────────┐
│  frontend/  (HTML · CSS · JS)              │
│  window.pywebview.api.*  ← único canal     │
├────────────────────────────────────────────┤
│  backend.py  (js_api)                      │
│  traduz chamadas JS → core; retorna dicts  │
│  sem lógica de negócio                     │
├────────────────────────────────────────────┤
│  transcriber.py  ·  audio.py  ·  config.py │
│  lógica pura Python, sem coupling a UI     │
│  100% testável sem webview                 │
└────────────────────────────────────────────┘
       ↕  keyboard (hotkey global, processo paralelo)
```

## Estrutura de Arquivos

```
dita/
├── main.py           # entry point: cria janela + inicia listener de hotkey
├── backend.py        # js_api exposta ao frontend via pywebview
├── hotkey.py         # listener pynput + make_toggle(); isolado para facilitar teste
├── transcriber.py    # wrapper faster-whisper
├── audio.py          # gravação com sounddevice
├── config.py         # load_config() / save_config() — lê/escreve config.json
├── config.json       # configurações do usuário
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js        # inclui handleHotkey() para o toggle via evaluate_js
├── tests/
│   ├── unit/         # cobre transcriber, audio, config — sem webview
│   └── integration/
├── install.sh
├── run.sh
├── dita.desktop
└── docs/
```

> **Nota:** estrutura plana intencional — app pequena, sem justificativa para `src/` hierárquico.
> Revisar se a base de código ultrapassar ~10 módulos.

## Decisões

| Decisão | Motivo |
|---|---|
| pywebview | Frameless + transparent nativo no Linux; suporta `backdrop-filter` real via WebKitGTK |
| faster-whisper | 2× mais rápido que whisper original, mesma API, VAD integrado |
| sounddevice + numpy | Captura de microfone simples; produz float32 16kHz direto |
| pyperclip | Abstrai X11 (`xclip`) e Wayland (`wl-clipboard`) |
| pynput | Escuta atalho global sem root; suporta X11 e Wayland |
| config.json | Configuração legível pelo usuário sem editar código; sem `.env` |
| Vanilla JS | Mockup já definido; sem necessidade de framework |

## Threading Model

`stop_recording()` executa transcrição que pode levar 2–10s. O pywebview chama métodos do `js_api` em thread separada, então o `await` no JS espera sem congelar a UI. A waveform e o status "processando" devem ser atualizados **antes** de chamar `stop_recording()` no JS.

## Regras de Dependência

- `transcriber.py`, `audio.py`, `config.py` → stdlib + libs específicas; sem imports de `backend.py` ou `frontend/`
- `backend.py` → importa core modules; nunca o inverso
- `frontend/` → sem imports Python; comunica exclusivamente via `window.pywebview.api`
- `main.py` → orquestra tudo; único lugar onde `webview.start()` é chamado
