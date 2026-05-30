import pyautogui
import time
import os
from core.utils import dormir


class VisionRobot:
    """Implementa la visión por reconocimiento de imágenes y prompts de control."""

    def __init__(self, folder_assets="assets"):
        # Resuelve la carpeta assets respecto a la raíz del proyecto (un nivel arriba de core/)
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assets = os.path.join(base, folder_assets)
        if not os.path.exists(self.assets):
            os.makedirs(self.assets)
            print(f"[INFO Vision]: Carpeta '{self.assets}' creada. Guarda tus capturas .png aquí.")

    def confirmar_inicio(self):
        """Muestra una ventana emergente para que el usuario prepare el navegador."""
        respuesta = pyautogui.confirm(
            text=("¿Está todo listo para empezar?\n"
                  "Asegúrate de tener el navegador visible."),
            title="Automaz(h)er - Control de Usuario",
            buttons=['¡Sí, adelante!', 'No, espera']
        )
        return respuesta == '¡Sí, adelante!'

    def buscar_y_clickear(self, carpeta, confianza=0.6, reintentos=5, click=True):
        """Busca una imagen dentro de una carpeta de variantes y hace click (o solo mueve).

        Escanea todos los .png dentro de assets/<carpeta>/ y los prueba uno por uno.

        Args:
            carpeta: nombre de la subcarpeta dentro de assets/ (ej: "barraURL").
            confianza: umbral de coincidencia (0-1).
            reintentos: cuántas veces reintentar antes de fallar.
            click: si True hace click, si False solo mueve el mouse.
        """
        dir_carpeta = os.path.join(self.assets, carpeta)
        if not os.path.isdir(dir_carpeta):
            print(f"[ERROR Vision]: No existe la carpeta '{dir_carpeta}'")
            return False

        imagenes = sorted(f for f in os.listdir(dir_carpeta)
                          if f.lower().endswith(".png"))
        if not imagenes:
            print(f"[ERROR Vision]: No hay imágenes .png en '{dir_carpeta}'")
            return False

        print(f"[INFO Vision]: Buscando en '{carpeta}/' ({len(imagenes)} variante(s))...")

        for intento in range(reintentos):
            for nombre_img in imagenes:
                ruta = os.path.join(dir_carpeta, nombre_img)
                try:
                    punto = pyautogui.locateCenterOnScreen(ruta, confidence=confianza)
                    if punto:
                        print(f"[OK Vision]: '{carpeta}/{nombre_img}' en {punto}")
                        pyautogui.moveTo(punto, duration=0.5)
                        if click:
                            pyautogui.click()
                        return True
                except Exception as e:
                    print(f"[DEBUG Vision]: '{carpeta}/{nombre_img}' intento {intento+1}: {e}")

            if dormir(1.0):
                print("[INFO Vision]: Killswitch activado durante busqueda.")
                return False

        print(f"[FAIL Vision]: Ninguna imagen en '{carpeta}/' coincidio tras {reintentos} intentos.")
        return False

    def esperar_elemento(self, carpeta, timeout=15, intervalo=1.0):
        """Espera activa: escanea cada <intervalo> segundos hasta que
        el elemento aparece o se alcanza el <timeout>.

        Retorna True si encontró el elemento, False si expiró el tiempo.
        """
        dir_carpeta = os.path.join(self.assets, carpeta)
        if not os.path.isdir(dir_carpeta):
            return False

        imagenes = sorted(f for f in os.listdir(dir_carpeta)
                          if f.lower().endswith(".png"))
        if not imagenes:
            return False

        fin = time.time() + timeout
        while time.time() < fin:
            for nombre_img in imagenes:
                ruta = os.path.join(dir_carpeta, nombre_img)
                try:
                    punto = pyautogui.locateCenterOnScreen(ruta, confidence=0.6)
                    if punto:
                        return True
                except Exception:
                    pass
            if dormir(intervalo):
                print("[INFO Vision]: Killswitch activado durante espera.")
                return False
        return False


# Instancia global
vision_robot = VisionRobot()
