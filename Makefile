.DEFAULT_GOAL := help

.PHONY: help install run lint fmt test hooks

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

install: hooks ## Cria venv e instala todas as dependências (incluindo dev)
	@echo "Dependências de sistema necessárias (Ubuntu/Debian):"
	@echo "  sudo apt install python3-gi python3-gi-cairo gir1.2-webkit2-4.1 libportaudio2 xclip"
	uv sync --all-groups

hooks: ## Instala git hooks locais
	cp scripts/pre-push .git/hooks/pre-push
	chmod +x .git/hooks/pre-push

run: ## Inicia a aplicação
	uv run python main.py

lint: ## Verifica estilo e erros (ruff + isort check)
	uv run ruff check .
	uv run isort --check-only .

fmt: ## Formata o código (black + isort)
	uv run black .
	uv run isort .

test: ## Roda os testes
	uv run pytest tests/ -v
