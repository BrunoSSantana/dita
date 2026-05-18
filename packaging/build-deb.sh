#!/bin/bash
# Builds a .deb package for dita.
# Run from the project root: bash build-deb.sh
set -euo pipefail

PKG=dita
VERSION=$(grep '^version' pyproject.toml | head -1 | cut -d'"' -f2)
ARCH=$(dpkg --print-architecture)
DEB_NAME="${PKG}_${VERSION}_${ARCH}.deb"
STAGING=$(mktemp -d)
APP_DIR="$STAGING/opt/dita"

echo "==> Building $DEB_NAME"

# ── App files ──────────────────────────────────────────────────────────────
mkdir -p "$APP_DIR"
cp -r dita/ frontend/ "$APP_DIR/"

# ── Icon ───────────────────────────────────────────────────────────────────
mkdir -p "$STAGING/usr/share/icons/hicolor/scalable/apps"
cp assets/dita.svg "$STAGING/usr/share/icons/hicolor/scalable/apps/dita.svg"

# ── Launcher ───────────────────────────────────────────────────────────────
mkdir -p "$STAGING/usr/bin"
cat > "$STAGING/usr/bin/dita" <<'EOF'
#!/bin/bash
exec /opt/dita/.venv/bin/python -m dita.main "$@"
EOF
chmod 755 "$STAGING/usr/bin/dita"

# ── Desktop entry ──────────────────────────────────────────────────────────
mkdir -p "$STAGING/usr/share/applications"
cat > "$STAGING/usr/share/applications/dita.desktop" <<'EOF'
[Desktop Entry]
Name=Dita
Comment=Transcrição por voz
Exec=/usr/bin/dita
Icon=dita
Type=Application
Categories=Utility;AudioVideo;
EOF

# ── DEBIAN/control ─────────────────────────────────────────────────────────
mkdir -p "$STAGING/DEBIAN"
cat > "$STAGING/DEBIAN/control" <<EOF
Package: $PKG
Version: $VERSION
Architecture: $ARCH
Maintainer: Bruno Santana <brunoosouza15@gmail.com>
Depends: python3 (>= 3.11), python3-gi, python3-gi-cairo, gir1.2-webkit2-4.1, libportaudio2, xclip, ffmpeg
Description: Overlay de transcrição de voz para Linux
 Captura áudio do microfone, transcreve com Whisper e cola o texto
 na janela ativa. Controlado por atalho de teclado configurável.
EOF

# ── DEBIAN/postinst ────────────────────────────────────────────────────────
cat > "$STAGING/DEBIAN/postinst" <<'EOF'
#!/bin/bash
set -e

APP=/opt/dita
VENV=$APP/.venv
PY=$(command -v python3.12 || command -v python3.11 || command -v python3)

echo "==> Criando ambiente virtual em $VENV..."
"$PY" -m venv --system-site-packages "$VENV"

echo "==> Instalando dependências Python..."
"$VENV/bin/pip" install --quiet --upgrade pip
"$VENV/bin/pip" install --quiet \
    pywebview \
    faster-whisper \
    sounddevice \
    numpy \
    pyperclip \
    pynput \
    screeninfo

echo "==> Baixando modelo Whisper (medium) — pode demorar alguns minutos..."
"$VENV/bin/python" - <<'PYEOF'
from faster_whisper import WhisperModel
WhisperModel("medium", device="cpu", compute_type="int8")
print("  Modelo pronto.")
PYEOF

echo "==> Dita instalado. Execute: dita"
EOF
chmod 755 "$STAGING/DEBIAN/postinst"

# ── DEBIAN/prerm ───────────────────────────────────────────────────────────
cat > "$STAGING/DEBIAN/prerm" <<'EOF'
#!/bin/bash
set -e
rm -rf /opt/dita/.venv
EOF
chmod 755 "$STAGING/DEBIAN/prerm"

# ── Build ──────────────────────────────────────────────────────────────────
dpkg-deb --build --root-owner-group "$STAGING" "$DEB_NAME"
rm -rf "$STAGING"

echo ""
echo "Pacote gerado: $DEB_NAME"
echo "Instalar com: sudo dpkg -i $DEB_NAME && sudo apt-get install -f"
