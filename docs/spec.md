# Spec — Dita

> Status: refinada ✓

## Visão Geral

Dita é uma aplicação desktop para Linux que abre como overlay flutuante sobre a tela, grava áudio do microfone, transcreve via `faster-whisper` e copia o resultado para a área de transferência. Acionada por atalho global de teclado. Interface glassmorphism, discreta e sem barra de título. Comando de terminal: `dita`.

---

## Público

Usuários técnicos em Linux que precisam de transcrição rápida sem abrir browser ou app pesado.

---

## Fluxo Principal

```
atalho global → janela abre (ou reaparece) → [gravar] → falar → [parar] → transcrito aparece → copia automático → janela fecha após N s
```

Alternativa teclado-only:
```
atalho → atalho (começa gravar) → atalho (para e transcreve) → colar
```

---

## Estados

```
idle
 └─[gravar / 2º atalho]──→ recording
      └─[parar / 3º atalho]──→ processing
            ├─[texto ok]──→ done ──→ (auto-fecha após auto_close_after s)
            └─[sem áudio]──→ idle

done
 └─[gravar novamente]──→ recording  (limpa resultado anterior)
```

---

## Configuração (`config.json`)

```json
{
  "model": "medium",
  "language": "pt",
  "hotkey": "ctrl+shift+space",
  "auto_copy": true,
  "auto_close_after": 3,
  "device": "cpu",
  "compute_type": "int8"
}
```

| Campo | Valores | Padrão |
|---|---|---|
| `model` | `tiny` \| `base` \| `small` \| `medium` \| `large-v3` | `medium` |
| `language` | código ISO ou `auto` | `pt` |
| `hotkey` | string do `pynput` (ex: `<ctrl>+<shift>+<space>`) | `<ctrl>+<shift>+<space>` |
| `auto_copy` | `true` \| `false` | `true` |
| `auto_close_after` | int segundos; `0` = não fecha | `3` |
| `device` | `cpu` \| `cuda` | `cpu` |
| `compute_type` | `int8` (cpu) \| `float16` (cuda) | `int8` |

---

## Features

### F1 — Atalho global
- Atalho configurável em `config.json`
- Comportamento ao acionar:
  1. Janela fechada → abre centralizada e foca
  2. Janela aberta, estado `idle` → começa a gravar imediatamente
  3. Janela aberta, estado `recording` → para e transcreve
  4. Janela aberta, estado `processing` → ignora

### F2 — Gravação de áudio
- Microfone padrão do sistema via `sounddevice`
- Sample rate: 16 kHz mono float32 (requerido pelo Whisper)
- Timer visível durante gravação (MM:SS)
- Waveform animada enquanto grava

### F3 — Transcrição
- Engine: `faster-whisper` com VAD integrado
- `vad_filter=True` filtra silêncio automaticamente
- Idioma configurável; `auto` usa detecção automática
- Transcrição ocorre em thread separada (não bloqueia UI)

### F4 — Clipboard
- Cópia automática ao concluir (`auto_copy: true`)
- Botão manual de cópia disponível
- Usa `pyperclip` (suporte X11 e Wayland via `xclip`/`wl-clipboard`)

### F5 — Interface
- Janela frameless, transparent, always-on-top
- Glassmorphism: `backdrop-filter: blur(28px)`; fallback opaco no X11 sem compositor
- Fechar: tecla `Esc` ou atalho global quando `done`/`idle`
- Fade-in de 150ms ao abrir
- Texto transcrição com efeito typewriter (22ms/char)
- Idioma ciclável no botão do header (persiste em `config.json`)

### F6 — Instalação
- `install.sh`: instala deps do sistema (apt), cria venv, baixa modelo, registra comando
- Comando `dita` via symlink em `/usr/local/bin/`
- Entrada no menu de aplicativos via `dita.desktop`

---

## Non-Goals

- Não é um editor de texto
- Não suporta múltiplas gravações simultâneas
- Não sincroniza transcrições em nuvem
- Não suporta Windows/macOS (Linux only)
- Não tem histórico de transcrições persistido
