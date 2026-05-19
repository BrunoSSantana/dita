import logging
import sys
from pathlib import Path

import webview
from screeninfo import get_monitors

from dita.backend import Backend
from dita.config import load_config
from dita.hotkey import make_toggle, start_listener
from dita.tray import start_tray

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger(__name__)


def main() -> None:
    cfg = load_config()
    backend = Backend()

    w, h = 400, 320
    monitor = get_monitors()[0]
    x = (monitor.width - w) // 2
    y = (monitor.height - h) // 2

    frontend = str(Path(__file__).parent.parent / "frontend" / "index.html")
    window = webview.create_window(
        title="",
        url=frontend,
        js_api=backend,
        width=w,
        height=h,
        x=x,
        y=y,
        frameless=True,
        transparent=True,
        on_top=True,
        resizable=False,
        shadow=False,
    )
    backend.set_window(window)

    listener = start_listener(cfg["hotkey"], make_toggle(window))
    tray = start_tray(on_quit=window.destroy)

    log.info("starting dita")
    webview.start(debug=False)

    if listener is not None:
        listener.stop()
    log.info("dita exited")


if __name__ == "__main__":
    main()
