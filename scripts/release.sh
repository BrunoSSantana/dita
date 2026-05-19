#!/bin/bash
set -euo pipefail

VERSION="${1:-}"

if [[ -z "$VERSION" ]]; then
    echo "Uso: bash scripts/release.sh <versão>  (ex: 0.2.1)"
    exit 1
fi

if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Erro: versão deve seguir semver (ex: 1.2.3)"
    exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "Erro: working tree com alterações não commitadas. Faça commit ou stash antes."
    exit 1
fi

CURRENT=$(grep '^version' pyproject.toml | head -1 | cut -d'"' -f2)
echo "==> $CURRENT → $VERSION"

sed -i "s/^version = \"$CURRENT\"/version = \"$VERSION\"/" pyproject.toml
uv lock --quiet

git add pyproject.toml uv.lock
git commit -m "chore(release): bump version to $VERSION"
git tag "v$VERSION"

echo "==> Pushing commit e tag v$VERSION..."
git push origin main "v$VERSION"

echo ""
echo "Release v$VERSION disparada. Acompanhe em:"
echo "  https://github.com/BrunoSSantana/dita/releases"
