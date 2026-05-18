---
id: T07
title: install.sh · run.sh · dita.desktop
status: done
depends_on: [T04, T06]
files_to_create:
  - install.sh
  - run.sh
  - dita.desktop
---

## Goal

Scripts de instalação e integração com o sistema Linux para que a app rode via comando `dita`.

## Contexto

- Spec: [docs/spec.md](../docs/spec.md) — seção "Script de instalação"
- Riscos: [docs/risks.md](../docs/risks.md) — R8 (conteúdo de run.sh e dita.desktop), R9 (apt-get é Debian/Ubuntu only)

## `install.sh`

Deve:
1. Instalar deps do sistema via `apt-get`: `ffmpeg libportaudio2 xclip python3-gi gir1.2-webkit2-4.0`
2. Criar venv em `.venv/`
3. Instalar pacotes Python: `pywebview faster-whisper sounddevice numpy pyperclip pynput`
   - **Não instalar** `keyboard` nem `python-dotenv` (removidos)
4. Baixar modelo Whisper medium no install (não em runtime)
5. Criar symlink `/usr/local/bin/dita → <pwd>/run.sh`
6. Copiar `dita.desktop` para `~/.local/share/applications/`

## `run.sh`

```bash
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
exec python main.py "$@"
```

## `dita.desktop`

```ini
[Desktop Entry]
Name=Dita
Comment=Transcrição por voz
Exec=/usr/local/bin/dita
Icon=audio-input-microphone
Type=Application
Categories=Utility;AudioVideo;
```

## Acceptance Criteria

- [ ] `./install.sh` roda sem erros em Ubuntu 22.04+
- [ ] `dita` disponível no PATH após install
- [ ] `run.sh` tem permissão de execução (`chmod +x`)
- [ ] `dita.desktop` aparece no launcher do sistema
- [ ] Reinstalar (rodar install.sh de novo) não quebra estado existente

## Notas

- Escopar para Ubuntu/Debian — documentar no topo do `install.sh` que é Debian-based only (R9)
- `set -e` no topo do install.sh para falhar rápido em caso de erro
- Não instalar globalmente com pip — sempre dentro do venv

---

## Log

| Data | Status | Observação |
|---|---|---|
| — | `pending` | — |
