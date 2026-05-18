# Riscos e Problemas Conhecidos

Problemas identificados na spec original que precisam de decisão ou atenção durante a implementação.

---

## Críticos

### R1 — `keyboard` library requer root no Linux ✅ RESOLVIDO
A lib `keyboard` escuta eventos globais via `/dev/input`, o que exige root ou o usuário no grupo `input`.

**Impacto:** usuários sem root não conseguem usar o atalho global.

**Alternativa recomendada:** `pynput` — não requer root na maioria das distros com X11/Wayland.

```python
# trocar keyboard por pynput
from pynput import keyboard as kb

def on_activate():
    toggle()

with kb.GlobalHotKeys({'<ctrl>+<shift>+<space>': on_activate}) as h:
    h.join()
```

**Decisão pendente:** trocar `keyboard` por `pynput`? Atualizar `install.sh` e `config.json` (formato do hotkey difere).

---

### R2 — `config.py` ausente da spec ✅ RESOLVIDO
`main.py` referencia `from config import load_config`, mas `config.py` não está na estrutura de arquivos da spec original.

**Resolução:** criar `config.py` com:
- `load_config() -> dict` — lê `config.json`, retorna defaults se ausente
- `save_config(patch: dict)` — merge parcial e persiste

---

### R3 — `toggle()` em `main.py` não implementado ✅ RESOLVIDO
A spec deixa `toggle` como `pass`. Comportamento esperado:

```python
def toggle():
    if window is None or not window.shown:
        window.show()
    elif state == 'idle':
        window.evaluate_js('startRecording()')
    elif state == 'recording':
        window.evaluate_js('stopRecording()')
    # processing → ignora
```

Problema: o estado (`idle`/`recording`) vive no JS. Precisamos de um dos dois:
- `Backend` mantém `self.state` espelhado
- ou `toggle` só faz show/hide e o atalho chama `toggleRecord()` via `evaluate_js`

**Recomendação:** `Backend` mantém o estado; `toggle()` lê `backend.state`.

---

## Médios

### R4 — `backdrop-filter` no X11 sem compositor
`blur()` no CSS exige compositor ativo (Picom, KWin, Mutter). Em i3, Openbox ou TTY sem compositor, a janela aparece sem blur.

**Mitigação já na spec:** fallback `background: rgba(242,242,240,0.94)` — implementar detecção ou deixar para o usuário configurar.

---

### R5 — CSS: `animation-delay` não aplicado nas barras ✅ RESOLVIDO
O JS define `--d` (delay) em cada `.bar` via `style.cssText`, mas o CSS não usa a variável na propriedade `animation`:

```css
/* spec atual — delay não funciona */
.bar.idle { animation: bar-idle 2.4s ease-in-out infinite; }

/* correto */
.bar.idle { animation: bar-idle 2.4s ease-in-out var(--d, 0s) infinite; }
.bar.active { animation: bar-active 0.35s ease-in-out var(--d, 0s) infinite; }
```

Sem isso todas as barras animam em sincronia — efeito waveform não funciona.

---

### R6 — `save_language()` não implementado na spec
Método marcado como `...` em `backend.py`. Implementação necessária:

```python
def save_language(self, lang: str) -> dict:
    save_config({"language": lang})
    self.transcriber.language = lang
    return {"ok": True, "data": None}
```

---

### R7 — `python-dotenv` na spec mas sem uso ✅ RESOLVIDO
A spec lista `python-dotenv` nas dependências mas usa apenas `config.json` — nenhum `.env` é mencionado. Dependência desnecessária.

**Resolução:** remover `python-dotenv` das dependências.

---

## Menores

### R8 — `run.sh` e `dita.desktop` não definidos na spec
Mencionados na estrutura de arquivos mas sem conteúdo especificado.

**`run.sh`:**
```bash
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
exec python main.py "$@"
```

**`dita.desktop`:**
```ini
[Desktop Entry]
Name=Dita
Comment=Transcrição por voz
Exec=/usr/local/bin/dita
Icon=audio-input-microphone
Type=Application
Categories=Utility;AudioVideo;
```

---

### R9 — `install.sh` é Debian/Ubuntu-specific
Usa `apt-get` — não funciona em Arch, Fedora, etc.

**Decisão pendente:** scope do suporte. Se for apenas Ubuntu/Debian, documentar claramente. Caso contrário, criar seções por distro.

---

### R10 — `copyManual()` não recopia para clipboard
Função chama apenas `showCheck()` assumindo que `pyperclip` já copiou. Se o usuário pressionar "copy" depois de um `clearAll()` seguido de nova gravação falha, o clipboard pode ter conteúdo antigo.

**Resolução:** `copyManual()` deve chamar `window.pywebview.api.copy_text(text)` ou usar a Clipboard API do browser (`navigator.clipboard.writeText`).
