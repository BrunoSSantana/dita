#!/bin/bash
# Debian/Ubuntu only — requer apt-get e Python 3.11+
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "==> Instalando dependências do sistema..."
sudo apt-get update -qq
sudo apt-get install -y \
    ffmpeg \
    libportaudio2 \
    xclip \
    python3-gi \
    python3-gi-cairo \
    gir1.2-webkit2-4.1

echo "==> Criando ambiente virtual..."
python3 -m venv "$SCRIPT_DIR/.venv"
source "$SCRIPT_DIR/.venv/bin/activate"

echo "==> Instalando pacotes Python..."
pip install --quiet --upgrade pip
pip install --quiet \
    pywebview \
    faster-whisper \
    sounddevice \
    numpy \
    pyperclip \
    pynput

echo "==> Baixando modelo Whisper (medium)..."
python3 - <<'EOF'
from faster_whisper import WhisperModel
print("  Baixando... (pode demorar alguns minutos na primeira vez)")
WhisperModel("medium", device="cpu", compute_type="int8")
print("  Modelo pronto.")
EOF

echo "==> Configurando permissão de execução em run.sh..."
chmod +x "$SCRIPT_DIR/run.sh"

echo "==> Criando symlink /usr/local/bin/dita..."
sudo ln -sf "$SCRIPT_DIR/run.sh" /usr/local/bin/dita

echo "==> Instalando entrada no menu de aplicativos..."
mkdir -p "$HOME/.local/share/applications"
cp "$SCRIPT_DIR/dita.desktop" "$HOME/.local/share/applications/dita.desktop"

echo ""
echo "Instalação concluída. Execute: dita"
