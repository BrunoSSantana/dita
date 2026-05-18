---
id: T04
title: main.py — entry point e janela pywebview
status: done
depends_on: [T03]
files_to_create:
  - main.py
---

## Goal

Implementar o entry point da aplicação: cria a janela pywebview, registra o atalho global via `hotkey.py` e inicia o loop de eventos.

## Contexto

- Spec: [docs/spec.md](../docs/spec.md) — seção "Janela"
- Arquitetura: [docs/architecture.md](../docs/architecture.md)
- `hotkey.py` já implementado — ver arquivo

## Comportamento Esperado

```python
# pseudocódigo
cfg = load_config()
backend = Backend()
window = webview.create_window(
    title='', url='frontend/index.html', js_api=backend,
    width=400, height=320,
    frameless=True, transparent=True, on_top=True,
    resizable=False, shadow=False,
)
backend.set_window(window)
listener = start_listener(cfg['hotkey'], make_toggle(window))
webview.start(debug=False)
listener.stop()
```

## Requisitos

- Janela centralizada na tela ao abrir
- `on_top=True`, `frameless=True`, `transparent=True`
- Atalho registrado **antes** de `webview.start()` — o listener roda em thread separada
- `listener.stop()` chamado após `webview.start()` retornar (app fechou)
- Não colocar lógica de negócio em `main.py` — apenas orquestração

## Acceptance Criteria

- [ ] `dita` (ou `python main.py`) abre a janela
- [ ] Janela aparece centralizada, sem barra de título
- [ ] Atalho global funciona sem a janela estar em foco
- [ ] Fechar a janela encerra o processo completamente (sem hang)
- [ ] `debug=False` em produção

## Notas

- `webview.start()` bloqueia até a janela fechar — código após ele é cleanup
- Para centralizar: `webview` não tem API de posição direta; usar `x` e `y` no `create_window` calculados com `screeninfo` ou deixar o sistema operacional decidir (padrão já costuma centralizar)
- Testar se `transparent=True` funciona no ambiente antes de reportar como done

---

## Log

| Data | Status | Observação |
|---|---|---|
| 2026-05-18 | `done` | implementado |
