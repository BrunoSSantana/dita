import logging
from typing import Callable

log = logging.getLogger(__name__)


def start_tray(on_quit: Callable) -> object | None:
    try:
        import gi

        gi.require_version("AppIndicator3", "0.1")
        from gi.repository import AppIndicator3, Gtk
    except (ImportError, ValueError):
        log.warning("AppIndicator3 not available — install gir1.2-appindicator3-0.1")
        return None

    def _quit(_item):
        on_quit()

    menu = Gtk.Menu()
    item = Gtk.MenuItem(label="Sair")
    item.connect("activate", _quit)
    menu.append(item)
    menu.show_all()

    indicator = AppIndicator3.Indicator.new(
        "dita",
        "audio-input-microphone",
        AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
    )
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    indicator.set_menu(menu)

    log.info("tray indicator started")
    return indicator
