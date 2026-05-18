"""
Global hotkey listener.

Toggle behavior (state machine lives in JS; Python delegates via evaluate_js):
  window hidden  → show + focus
  idle           → startRecording()
  recording      → stopRecording()
  processing     → ignore
"""

import logging
from typing import Callable

from pynput import keyboard

log = logging.getLogger(__name__)


def start_listener(hotkey: str, callback: Callable) -> keyboard.GlobalHotKeys:
    """
    Registra atalho global. Retorna o listener (chame .stop() para encerrar).
    hotkey: formato pynput, ex: '<ctrl>+<shift>+<space>'
    """

    def on_activate():
        try:
            callback()
        except Exception:
            log.exception("hotkey callback error")

    listener = keyboard.GlobalHotKeys({hotkey: on_activate})
    listener.start()
    log.info("hotkey registered: %s", hotkey)
    return listener


def make_toggle(window) -> Callable:
    """
    Retorna a função de toggle que deve ser passada para start_listener.
    window: instância do webview.Window
    """

    def toggle():
        # show() foca a janela se já visível; não falha se já estiver aberta
        window.show()
        window.evaluate_js("typeof handleHotkey !== 'undefined' && handleHotkey()")

    return toggle
