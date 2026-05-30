from core.domain import SORTEOS


class Menu:
    """Clase para abstraer todos métodos relacionados a un menú y/o submenú"""

    @staticmethod
    def mostrar_menu_principal():

        print("-- Bienvenida/o a Automiz(h)er --")
        while True:
            print("1.-Iniciar automatización")
            print("2.-Configurar Sorteos(URLs)")
            print("0.-Salir")

            opcion = input("Ingrese una opción: ")

            if opcion == "1":
                from core.automator import Automator
                automator = Automator()
                automator.ejecutar()
            elif opcion == "2":
                Menu.gestionarURL()
            elif opcion == "0":
                print("[INFO]: Programa terminado.")
                exit()
            else:
                print("Ingrese una opción válida.")
                continue

    @staticmethod
    def gestionarURL():
        while True:
            print("-- Gestión de URL's --")

            print("1.-Ver URL's")
            print("2.-Añadir URL's")
            print("3.-Editar URL's")
            print("4.-Eliminar URL's")
            print("5.-Editar comentarios")
            print("6.-Editar etiquetados")
            print("0.-Volver")

            opcion = input("Ingrese una opción: ")

            if opcion == "1":
                Menu.ver_dominio()
            elif opcion == "2":
                Menu.agregar_url()
            elif opcion == "3":
                Menu.editar_url()
            elif opcion == "4":
                Menu.eliminar_url()
            elif opcion == "5":
                Menu.gestionar_comentarios_global()
            elif opcion == "6":
                Menu.gestionar_etiquetados_global()
            elif opcion == "0":
                return
            else:
                print("Ingrese una opción válida")

    @staticmethod
    def gestionar_comentarios_global():
        """Pregunta el dominio y redirige a gestionar_comentarios."""
        print("-- Editar comentarios --")
        print("[INFO]: Selecciona un dominio:")
        for clave, sorteo in SORTEOS.items():
            print("{0}.-{1}".format(clave, sorteo.nombre))
        print("0.-Volver")

        opcion = input("Ingrese una opcion: ")
        if opcion in SORTEOS:
            Menu.gestionar_comentarios(SORTEOS[opcion])

    @staticmethod
    def gestionar_etiquetados_global():
        """Pregunta el dominio y redirige a gestionar_etiquetados."""
        print("-- Editar etiquetados --")
        print("[INFO]: Selecciona un dominio:")
        for clave, sorteo in SORTEOS.items():
            print("{0}.-{1}".format(clave, sorteo.nombre))
        print("0.-Volver")

        opcion = input("Ingrese una opcion: ")
        if opcion in SORTEOS:
            Menu.gestionar_etiquetados(SORTEOS[opcion])

    @staticmethod
    def ver_dominio():
        """Función que muestra un reporte de los enlaces cargados en un dominio (etiquetar, comentar, mixto, etc).
        Esta función permite ver las 'colecciones' de URL's separadas por dominio"""
        while True:
            print("-- Ver URL's --")
            print("[INFO]: Mostrando dominios"
                  "")
            for clave, sorteo in SORTEOS.items():
                completadas, total = sorteo.mostrar_resumen()
                print(f"{clave}.-{sorteo.nombre}: {completadas}/{total}")
            print("0.-Volver")

            opcion = input("Ingrese una opción para ver su detalles: ")

            if opcion in SORTEOS:
                SORTEOS[opcion].listar_urls()
            elif opcion == "0":
                return
            else:
                print("Ingrese una opción válida.")

    @staticmethod
    def agregar_url():
        print("-- Añadir URL's")
        while True:
            print("Tipos de URL - Dominios")
            print("1.-Etiqueta a un conocido")
            print("2.-Etiqueta a un seguidor")
            print("3.-Etiqueta X cantidad de personas")
            print("4.-Comentar")
            print("0.-Volver")

            opcion = input("Ingrese una opción: ")

            if opcion in SORTEOS:
                Menu.sub_agregar_url(SORTEOS[opcion])
            elif opcion == "0":
                return
            else:
                print("Ingrese una opción válida")

    @staticmethod
    def sub_agregar_url(sorteo):
        print(f"-- Añadir URLs a {sorteo.nombre} --")
        continuar = True

        while continuar:
            url = input("Introduce la URL del sorteo (0 para cancelar): ").strip()
            if url == "0":
                print("[INFO] Operación cancelada.")
                return

            sorteo.agregar_url(url)
            print(f"URL guardada con éxito en el sorteo de {sorteo.nombre}")

            while True:
                respuesta = input("[INPUT]: ¿Quiere añadir otro enlace? (s/n): ").strip().lower()
                if respuesta == "s":
                    break
                elif respuesta == "n":
                    continuar = False
                    break
                else:
                    print("Ingrese una opción válida.")

    @staticmethod
    def editar_url():
        """Muestra dominios, elige uno, y permite editar una URL."""
        print("-- Editar URL's --")
        print("[INFO]: Selecciona un dominio:")
        for clave, sorteo in SORTEOS.items():
            print("{0}.-{1}".format(clave, sorteo.nombre))
        print("0.-Volver")

        opcion = input("Ingrese una opcion: ")
        if opcion in SORTEOS:
            SORTEOS[opcion].modificar_url()

    @staticmethod
    def eliminar_url():
        """Muestra dominios, elige uno, y permite eliminar una URL."""
        print("-- Eliminar URL's --")
        print("[INFO]: Selecciona un dominio:")
        for clave, sorteo in SORTEOS.items():
            print("{0}.-{1}".format(clave, sorteo.nombre))
        print("0.-Volver")

        opcion = input("Ingrese una opcion: ")
        if opcion in SORTEOS:
            SORTEOS[opcion].eliminar_url()

    @staticmethod
    def gestionar_etiquetados(sorteo):
        if not sorteo.requiere_etiquetar:
            print()
            print(f"[ERROR]: El sorteo de '{sorteo.nombre}' no requiere etiquetados.")
            return

        print()
        print(f" -- Gesti\u00f3n de etiquetados para el sorteo de {sorteo.nombre} --")
        while True:
            sorteo.mostrar_etiquetados()

            print()
            print("1.- A\u00f1adir | 2.- Editar | 3.- Eliminar | 4.- Limpiar | 0.- Volver")

            opcion = input("Ingrese una opción: ")

            if opcion == "1":
                sorteo.ingresar_etiquetado()
            elif opcion == "2":
                if sorteo.etiquetados:
                    sorteo.modificar_etiquetado()
                else:
                    print("[ERROR]: No hay usuarios para editar.")
            elif opcion == "3":
                sorteo.eliminar_etiquetado()
            elif opcion == "4":
                sorteo.limpiar_etiquetados()
            elif opcion == "0":
                return
            else:
                print("Ingrese una opción válida.")

    @staticmethod
    def gestionar_comentarios(sorteo):
        """Gestiona la lista de comentarios en un sorteo."""
        print()
        print(f" -- Gesti\u00f3n de comentarios del sorteo de {sorteo.nombre} --")

        while True:
            sorteo.mostrar_comentarios()
            print()
            print("1.- A\u00f1adir | 2.- Editar | 3.- Eliminar uno | 4.- Limpiar | 0.- Volver")

            opcion = input("Ingrese una opción: ")

            if opcion == "1":
                sorteo.agregar_comentario()
            elif opcion == "2":
                sorteo.modificar_comentario()
            elif opcion == "3":
                sorteo.eliminar_comentario()
            elif opcion == "4":
                sorteo.limpiar_comentarios()
            elif opcion == "0":
                return
            else:
                print("Ingrese una opción válida.")

