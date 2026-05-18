---
id: T02
title: transcriber.py — transcrição faster-whisper
status: done
depends_on: []
files_to_create:
  - transcriber.py
---

## Goal

Implementar `Transcriber` — wrapper do `faster-whisper` que recebe numpy array de áudio e retorna texto.

## Contexto

- Spec: [docs/spec.md](../docs/spec.md) — seção "Transcrição"
- Arquitetura: [docs/architecture.md](../docs/architecture.md)
- Convenções: [docs/conventions.md](../docs/conventions.md)

## Interface Esperada

```python
class Transcriber:
    language: str  # atualizável em runtime (save_language no backend)

    def __init__(self, model: str, device: str, compute_type: str, language: str): ...
    def transcribe(self, audio: np.ndarray, sample_rate: int = 16000) -> str: ...
```

## Requisitos

- Usar `WhisperModel` do `faster_whisper`
- `vad_filter=True` com `min_silence_duration_ms=500`
- `beam_size=5`
- Retornar string vazia se nenhum segmento detectado (não é erro)
- Não deve depender de `backend.py`, `hotkey.py` ou módulos de UI
- Carregar o modelo no `__init__` — não carregar a cada transcrição

## Acceptance Criteria

- [ ] Modelo carregado uma única vez no `__init__`
- [ ] `transcribe()` retorna `str` (vazia se silêncio)
- [ ] `self.language` pode ser alterado entre transcrições
- [ ] Funciona com `device='cpu'` e `compute_type='int8'`
- [ ] Não lança exceção para áudio vazio ou muito curto — retorna `""`

## Notas

- O carregamento do modelo (`medium`) leva alguns segundos na primeira execução — é esperado
- Para `device='cuda'`, o caller passa `compute_type='float16'` via config
- Não pré-processar o áudio aqui — responsabilidade do `audio.py` garantir float32 16kHz

---

## Log

| Data | Status | Observação |
|---|---|---|
| 2026-05-18 | `done` | Implementado |
