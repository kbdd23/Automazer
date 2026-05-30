"""Killswitch global con pynput — escucha 'q' sin importar el foco."""

from pynput import keyboard

_killed = False
_listener = None


def iniciar():
    """Activa el listener global de teclado."""
    global _killed, _listener
    _killed = False

    def _on_press(tecla):
        global _killed
        try:
            if hasattr(tecla, 'char') and tecla.char and tecla.char.lower() == 'q':
                _killed = True
                print()
                print("[PANIC] Bot detenido por el usuario.")
                return False  # detiene el listener
        except Exception:
            pass

    _listener = keyboard.Listener(on_press=_on_press)
    _listener.daemon = True
    _listener.start()


def detener():
    """Detiene el listener si está activo."""
    global _listener
    if _listener and _listener.running:
        _listener.stop()


def fue_matado():
    """Retorna True si el usuario presionó 'q'."""
    return _killed
