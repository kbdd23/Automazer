#Este módulo está reservado para funciones "útiles" que no son
#especificamente principales, de dominio, ni de visión.
import random as r

class Util:
    """Clase ayudante. Gestiona métodos ajenos a funciones principales,
    de dominio, persistencia, y menú."""

    @staticmethod
    def generar_rango(v_min, v_max):
        """Genera un rango aleatorio dado un inicio y maximo."""
        try:
            if v_min > v_max:
                #Si el usuario se equivoca, ejemplo: v_min=10, v_max = 4. Invertimos los valores
                v_min, v_max = v_max, v_min

            return r.randint(v_min, v_max)
        except Exception:
            print(f"[ERROR Utils]: No se pudo generar el rango")
    
    @staticmethod
    def validar_usuario():
        """Pide un string, válida si existe y si tiene un @"""
        while True:
            usuario = input("Ingrese el usuario a etiquetar (con @): ").strip()
            if not "@" in usuario:
                print("Ingrese el usuario con su @ al inicio!")
            elif "@" in usuario and usuario:
                return usuario
            else:
                print("[ERROR utils.py]: Ingrese un usuario válido!. Intente otra vez.")