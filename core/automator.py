import random

from core.domain import SORTEOS
from core.vision import vision_robot
from core.utils import dormir
from core.killswitch import iniciar, detener, fue_matado
import pyautogui
import pyperclip


class Automator:
    """Orquesta el flujo completo de automatizacion usando el dominio y la vision."""

    @staticmethod
    def navegar_a(url):
        """Pega una URL en la barra de navegacion y pulsa Enter."""
        if not vision_robot.buscar_y_clickear("barraURL"):
            return False
        pyperclip.copy(url)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")
        return True

    @staticmethod
    def escribir_comentario(comentario):
        """Hace click en el campo de comentario y pega el texto."""
        if not vision_robot.buscar_y_clickear("barraComentado"):
            return False
        pyperclip.copy(comentario)
        pyautogui.hotkey("ctrl", "v")
        return True

    @staticmethod
    def enviar_comentario():
        """Busca el boton de publicar y hace click."""
        return vision_robot.buscar_y_clickear("botonPublicar")

    @staticmethod
    def construir_comentario(sorteo):
        """Construye el texto a publicar con lo que haya disponible.

        - Etiquetados: combina 1-3 aleatorios.
        - Comentarios: elige uno al azar.
        - Si hay ambos, los concatena.
        """
        tags = None
        texto = None

        if sorteo.etiquetados:
            cantidad = random.randint(1, min(3, len(sorteo.etiquetados)))
            elegidos = random.sample(sorteo.etiquetados, cantidad)
            tags = " ".join(elegidos)

        if sorteo.comentarios:
            texto = random.choice(sorteo.comentarios)

        if tags and texto:
            return "{0} {1}".format(texto, tags).strip()
        if tags:
            return tags
        if texto:
            return texto
        return None

    def ejecutar(self):
        """Ejecuta la automatizacion sobre todos los sorteos y sus URLs."""
        if not vision_robot.confirmar_inicio():
            print("[AUTOMATOR] Automatizacion cancelada.")
            return

        print("[AUTOMATOR] Iniciando automatizacion...")
        print("[PANIC] Presiona 'q' para detener en cualquier momento.")
        print()

        iniciar()

        for clave, sorteo in SORTEOS.items():
            if fue_matado():
                print()
                print("[AUTOMATOR] Automatizacion interrumpida.")
                return

            print()
            print("--- {0} ---".format(sorteo.nombre))

            # Pre-flight: si no hay contenido que publicar, saltar
            if not sorteo.etiquetados and not sorteo.comentarios:
                print("[SKIP] No hay etiquetados ni comentarios configurados. Saltando dominio.")
                continue

            for i, url_doc in enumerate(sorteo.urls, 1):
                if fue_matado():
                    print()
                    print("[AUTOMATOR] Automatizacion interrumpida.")
                    return

                restantes = url_doc["limite"] - url_doc["realizados"]
                if restantes <= 0:
                    print("[SKIP] URL {0}: ya completada ({1}/{2})".format(
                        i, url_doc["realizados"], url_doc["limite"]))
                    continue

                print()
                print("[URL {0}] Navegando a {1}".format(i, url_doc["url"]))

                pagina_cargada = False
                for intento in range(3):
                    if fue_matado():
                        print()
                        print("[AUTOMATOR] Automatizacion interrumpida.")
                        return

                    if self.navegar_a(url_doc["url"]):
                        if vision_robot.esperar_elemento("barraComentado", timeout=15):
                            pagina_cargada = True
                            break

                    if intento < 2:
                        print("  [RETRY] La pagina no cargo. Reintento {}/3...".format(intento + 2))

                if fue_matado():
                    print()
                    print("[AUTOMATOR] Automatizacion interrumpida.")
                    return
                if not pagina_cargada:
                    print("[FAIL] No se pudo cargar la pagina tras 3 intentos. Saltando URL.")
                    continue

                for j in range(restantes):
                    if fue_matado():
                        print()
                        print("[AUTOMATOR] Automatizacion interrumpida.")
                        return

                    comentario = self.construir_comentario(sorteo)
                    if not comentario:
                        print("[SKIP] No hay comentarios configurados. Saltando.")
                        break

                    print('  Comentario {0}/{1}: "{2}..."'.format(
                        j + 1, restantes, comentario[:50]))
                    if dormir(random.uniform(1, 3)):
                        print()
                        print("[AUTOMATOR] Automatizacion interrumpida.")
                        return

                    if not self.escribir_comentario(comentario):
                        print("  [FAIL] No se encontro el campo de comentario.")
                        break

                    if dormir(random.uniform(0.5, 1.5)):
                        print()
                        print("[AUTOMATOR] Automatizacion interrumpida.")
                        return

                    if not self.enviar_comentario():
                        print("  [FAIL] No se pudo enviar el comentario.")
                        break

                    url_doc["realizados"] += 1
                    sorteo.guardar()
                    print("  [OK] Comentario enviado. ({0}/{1})".format(
                        url_doc["realizados"], url_doc["limite"]))

                    if j < restantes - 1:
                        espera = random.uniform(3, 7)
                        print("  Esperando {0:.1f}s antes del siguiente comentario...".format(espera))
                        if dormir(espera):
                            print()
                            print("[AUTOMATOR] Automatizacion interrumpida.")
                            return

        detener()
        print()
        print("[AUTOMATOR] Automatizacion finalizada.")


if __name__ == "__main__":
    automator = Automator()
    automator.ejecutar()
