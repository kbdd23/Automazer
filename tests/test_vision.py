import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.vision import vision_robot
import pyautogui

if __name__ == "__main__":
    if not vision_robot.confirmar_inicio():
        print("[TEST] Prueba cancelada por el usuario.")
        exit()

    print("[TEST] Escaneando elementos en pantalla...
")

    carpetas = ["barraURL", "barraComentado", "botonPublicar"]
    nombres = {
        "barraURL": "Barra de URL",
        "barraComentado": "Campo de comentario",
        "botonPublicar": "Boton de publicar",
    }

    for carpeta in carpetas:
        dir_carpeta = os.path.join(vision_robot.assets, carpeta)
        if not os.path.isdir(dir_carpeta):
            print(f"[X] {nombres[carpeta]}: no existe la carpeta '{carpeta}/'")
            continue

        imagenes = sorted(f for f in os.listdir(dir_carpeta) if f.lower().endswith(".png"))
        if not imagenes:
            print(f"[X] {nombres[carpeta]}: no hay .png en '{carpeta}/'")
            continue

        print(f"  {nombres[carpeta]} ({len(imagenes)} variante(s)):")

        encontrada = False
        for img in imagenes:
            ruta = os.path.join(dir_carpeta, img)
            try:
                punto = pyautogui.locateCenterOnScreen(ruta, confidence=0.7)
                if punto:
                    print(f"    [OK] '{carpeta}/{img}' -> x={punto.x}, y={punto.y}")
                    encontrada = True
                    break
            except Exception as e:
                print(f"    [!] '{carpeta/{img}}': error -> {e}")

        if not encontrada:
            print(f"    [--] ninguna variante detectada en pantalla")
