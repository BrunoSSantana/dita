# JS↔Python API Contract

## Como Funciona

pywebview expõe a instância de `Backend` ao browser como `window.pywebview.api`. Cada método público vira chamada JS assíncrona.

```js
// JS
const result = await window.pywebview.api.metodo(arg)
```

```python
# Python — backend.py
class Backend:
    def metodo(self, arg: str) -> dict:
        try:
            data = core_module.fazer_algo(arg)
            return {"ok": True, "data": data}
        except AppError as e:
            return {"ok": False, "error": str(e)}
```

## Envelope de Resposta

Todo método retorna este formato — sem exceções não tratadas:

```json
{ "ok": true,  "data": <valor> }
{ "ok": false, "error": "<mensagem legível>" }
```

## Métodos

| Método | Args | `data` retornado | Descrição |
|---|---|---|---|
| `start_recording()` | — | `null` | Inicia captura de áudio |
| `stop_recording()` | — | `{ "text": str, "duration": float }` | Para gravação, transcreve, copia para clipboard |
| `get_config()` | — | objeto `config.json` | Retorna configuração atual |
| `save_language(lang)` | `lang: str` | `null` | Persiste idioma em `config.json` |
| `close()` | — | — | Destrói a janela (sem envelope) |

### Detalhes

**`stop_recording()`**
- Bloqueia até a transcrição concluir (2–10s dependendo do modelo e áudio)
- Já copia para clipboard se `auto_copy: true`
- Retorna `text: ""` se nada foi detectado (não é erro)
- O JS deve atualizar UI para "processando" **antes** de chamar este método

**`save_language(lang)`**
- Valores válidos: `"pt"`, `"en"`, `"es"`, `"fr"`, `"de"`, `"auto"`
- Persiste em `config.json`; aplica na próxima transcrição

**`close()`**
- Chama `self.window.destroy()`
- Não retorna envelope — chamada fire-and-forget

## Eventos Python → JS

pywebview permite `window.evaluate_js()` para push do Python ao frontend.

| Evento | Trigger | Implementação |
|---|---|---|
| — | — | Não há push events nesta versão; considerar para progresso de transcrição em v2 |

## Sequência de uma Gravação

```
JS: toggleRecord()
  → await api.start_recording()       # retorna imediatamente
  [usuário fala]
  → [usuário para]
  → setStatus("processando")          # atualiza UI antes
  → await api.stop_recording()        # bloqueia 2-10s
  ← { ok: true, data: { text, duration } }
  → typeText(text)
  → scheduleClose()
```
