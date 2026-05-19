import logging
import threading
from typing import Callable

from pynput import keyboard

log = logging.getLogger(__name__)


def start_listener(hotkey: str, callback: Callable) -> keyboard.GlobalHotKeys | None:
    """
    Registra atalho global. Retorna o listener ou None se falhar.
    hotkey: formato pynput, ex: '<ctrl>+<shift>+<space>'
    """

    def on_activate():
        try:
            callback()
        except Exception:
            log.exception("hotkey callback error")

    try:
        listener = keyboard.GlobalHotKeys({hotkey: on_activate})
        listener.start()
        log.info("hotkey registered and listener running: %s", hotkey)
        return listener
    except Exception:
        log.error("failed to register hotkey %s", hotkey, exc_info=True)
        return None


def make_toggle(window) -> Callable:
    def toggle():
        log.info("hotkey fired")
        window.show()

        # Delay garante que a janela esteja visível antes do evaluate_js no X11
        def _js():
            result = window.evaluate_js(
                "typeof handleHotkey !== 'undefined' && handleHotkey()"
            )
            log.info("evaluate_js result: %s", result)

        threading.Timer(0.05, _js).start()

    return toggle
