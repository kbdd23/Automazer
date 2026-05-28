import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.vision import vision_robot
import pyautogui
import pyperclip

if __name__ == "__main__":
    if not vision_robot.confirmar_inicio():
        print("[TEST] Prueba cancelada.")
        exit()

    url = "https://www.instagram.com/p/DY2fXc5x7nk/"
    comentario = "Prueba de automatizacion 🤖"

    print("[1/6] Buscando barra de URL...")
    if not vision_robot.buscar_y_clickear("barraURL", confianza=0.5):
        print("[FAIL] No se encontro la barra de URL.")
        exit()

    print("[2/6] Pegando URL...")
    pyperclip.copy(url)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")

    print("[3/6] Esperando 4 segundos a que cargue la pagina...")
    time.sleep(4)

    print("[4/6] Buscando campo de comentario...")
    if not vision_robot.buscar_y_clickear("barraComentado", confianza=0.8):
        print("[FAIL] No se encontro el campo de comentario.")
        exit()

    print("[5/6] Pegando comentario...")
    pyperclip.copy(comentario)
    pyautogui.hotkey("ctrl", "v")

    print("[6/6] Moviendo al boton de publicar (sin clickear)...")
    if not vision_robot.buscar_y_clickear("botonPublicar", confianza=0.5, click=False):
        print("[--] No se detecto el boton de publicar.")
