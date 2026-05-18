---
id: T01
title: audio.py — gravação de microfone
status: done
depends_on: []
files_to_create:
  - audio.py
---

## Goal

Implementar `AudioRecorder` — captura áudio do microfone padrão e retorna numpy array pronto para o Whisper.

## Contexto

- Spec: [docs/spec.md](../docs/spec.md) — seção "Áudio"
- Arquitetura: [docs/architecture.md](../docs/architecture.md)
- Convenções: [docs/conventions.md](../docs/conventions.md)

## Interface Esperada

```python
class AudioRecorder:
    duration: float  # duração do último áudio gravado em segundos

    def start(self) -> None: ...
    def stop(self) -> np.ndarray: ...  # float32 mono 16kHz
```

## Requisitos

- Sample rate: 16000 Hz, mono, dtype `float32` (requerido pelo faster-whisper)
- Usar `sounddevice.InputStream` com callback acumulador
- `stop()` deve parar o stream, concatenar frames e calcular `self.duration`
- Não deve depender de `backend.py`, `hotkey.py` ou qualquer módulo de UI

## Acceptance Criteria

- [ ] `start()` inicia stream sem bloquear
- [ ] `stop()` retorna `np.ndarray` shape `(N,)` dtype `float32`
- [ ] `self.duration` correto após `stop()`
- [ ] Chamadas consecutivas `start()` / `stop()` funcionam sem reinicializar objeto
- [ ] Sem vazamento de stream (sempre fecha com `stream.close()`)

## Notas

- Se `start()` for chamado enquanto já há stream ativo, fechar o anterior antes de abrir novo
- Não logar frames individuais — apenas início e fim da gravação

---

## Log

| Data | Status | Observação |
|---|---|---|
| 2026-05-18 | `done` | Implementado AudioRecorder com sounddevice.InputStream |
