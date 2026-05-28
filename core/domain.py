from core.utils import Util
from persistence.storage import Storage

storage = Storage()

MINIMO = 20
LIMITE = 65 + 78 + 65


class Dominio:

    def __init__(self, nombre, minimo_comentarios, maximo_comentarios, requiere_etiquetar=True):
        self.nombre = nombre
        self.requiere_etiquetar = requiere_etiquetar
        self.urls = []
        self.comentarios = []
        self.etiquetados = [] if requiere_etiquetar else None
        self.minimo_comentarios = minimo_comentarios
        self.maximo_comentarios = maximo_comentarios

    def serializar(self):
        return {
            "nombre": self.nombre,
            "requiere_etiquetar": self.requiere_etiquetar,
            "urls": self.urls,
            "comentarios": self.comentarios,
            "etiquetados": self.etiquetados,
        }

    def deserializar(self, datos):
        try:
            self.nombre = datos.get("nombre", self.nombre)
            self.requiere_etiquetar = datos.get("requiere_etiquetar", self.requiere_etiquetar)
            self.urls = datos.get("urls", [])
            self.comentarios = datos.get("comentarios", [])
            self.etiquetados = datos.get("etiquetados", self.etiquetados)
        except Exception as e:
            print(f"[ERROR domain.py]: Fallo al cargar {self.nombre}: {e}")

    def guardar(self):
        storage.guardar(SORTEOS)

    def agregar_url(self, url):
        limite = Util.generar_rango(self.minimo_comentarios, self.maximo_comentarios)
        self.urls.append({"url": url, "realizados": 0, "limite": limite})
        storage.guardar(SORTEOS)
        print(f"[INFO] URL anadida. Limite de comentarios: {limite}")

    def modificar_url(self):
        self.listar_urls()
        if not self.urls:
            return
        while True:
            try:
                indice = int(input("Ingrese el numero de la URL a editar (0 para cancelar): ")) - 1
                if indice == -1:
                    print("[INFO] Operacion cancelada.")
                    return
                if 0 <= indice < len(self.urls):
                    nueva_url = input("Ingrese la nueva URL (0 para cancelar): ").strip()
                    if nueva_url == "0":
                        print("[INFO] Operacion cancelada.")
                        return
                    if nueva_url:
                        self.urls[indice]["url"] = nueva_url
                        self.urls[indice]["realizados"] = 0
                        print("[INFO] URL actualizada. Contador reiniciado.")
                        self.guardar()
                        return
                    print("[ERROR] La URL no puede estar vacia.")
                else:
                    print("[ERROR] Numero invalido.")
            except ValueError:
                print("[ERROR] Debe ingresar un numero valido.")

    def eliminar_url(self):
        self.listar_urls()
        if not self.urls:
            return
        while True:
            try:
                indice = int(input("Ingrese el numero de la URL a eliminar: ")) - 1
                if 0 <= indice < len(self.urls):
                    confirmacion = input("Esta seguro de eliminar esta URL? (s/n): ").strip().lower()
                    if confirmacion == "s":
                        eliminada = self.urls.pop(indice)
                        print("[INFO] URL eliminada:", eliminada["url"])
                        self.guardar()
                    return
                print("[ERROR] Numero invalido.")
            except ValueError:
                print("[ERROR] Debe ingresar un numero valido.")

    def mostrar_resumen(self):
        completadas = sum(1 for u in self.urls if u["realizados"] >= u["limite"])
        return completadas, len(self.urls)

    def listar_urls(self):
        if not self.urls:
            print()
            print("[INFO] No hay URLs registradas en este dominio.")
            return
        print()
        print(f"--- Listando URLs del sorteo de {self.nombre} ---")
        for i, url_doc in enumerate(self.urls, 1):
            print(f"{i}.- {url_doc['url']} >> ({url_doc['realizados']}/{url_doc['limite']})")
            print("-" * 44)

    def mostrar_etiquetados(self):
        if not self.etiquetados:
            print()
            print(f"[INFO] La lista de etiquetados de '{self.nombre}' esta vacia.")
            return
        print()
        print(f"-- Usuarios etiquetados en {self.nombre} --")
        for i, usuario in enumerate(self.etiquetados, 1):
            print(f"{i}.- {usuario}")

    def ingresar_etiquetado(self):
        usuario = Util.validar_usuario()
        self.etiquetados.append(usuario)
        print(f"[INFO] Usuario {usuario} anadido.")
        self.guardar()

    def modificar_etiquetado(self):
        while True:
            try:
                indice = int(input("Ingrese el numero del usuario a editar: ")) - 1
                if 0 <= indice < len(self.etiquetados):
                    anterior = self.etiquetados[indice]
                    nuevo = Util.validar_usuario()
                    self.etiquetados[indice] = nuevo
                    print(f"[INFO] {anterior} cambiado a {nuevo}")
                    self.guardar()
                    return
                print("[ERROR] Numero invalido.")
            except ValueError:
                print("[ERROR] Debe ingresar un numero valido.")

    def eliminar_etiquetado(self):
        self.mostrar_etiquetados()
        if not self.etiquetados:
            return
        while True:
            try:
                indice = int(input("Ingrese el numero del usuario a eliminar: ")) - 1
                if 0 <= indice < len(self.etiquetados):
                    eliminado = self.etiquetados.pop(indice)
                    print(f"[INFO] Usuario {eliminado} eliminado correctamente")
                    self.guardar()
                    return
                print("[ERROR] Numero invalido.")
            except ValueError:
                print("[ERROR] Debe ingresar un numero valido.")

    def limpiar_etiquetados(self):
        if not self.etiquetados:
            print()
            print("[INFO] La lista ya esta vacia.")
            return
        confirmacion = input(f"Eliminar los {len(self.etiquetados)} usuarios de '{self.nombre}'? (s/n): ").strip().lower()
        if confirmacion == "s":
            cantidad = len(self.etiquetados)
            self.etiquetados.clear()
            print(f"[INFO] {cantidad} usuarios eliminados.")
            self.guardar()

    def mostrar_comentarios(self):
        if not self.comentarios:
            print()
            print("[INFO] La lista de comentarios esta vacia.")
            return
        print()
        print(f"-- Comentarios de {self.nombre} --")
        print(self.comentarios)

    def agregar_comentario(self):
        while True:
            comentario = input("Ingrese el comentario (puede incluir emojis): ").strip()
            if comentario:
                self.comentarios.append(comentario)
                print("[INFO] Comentario anadido.")
                self.guardar()
                while True:
                    resp = input("[INFO] Desea anadir otro comentario? (s/n): ").strip().lower()
                    if resp == "s":
                        break
                    elif resp == "n":
                        return
                    print("[ERROR] Opcion invalida.")

    def modificar_comentario(self):
        if not self.comentarios:
            print("[INFO] No hay comentarios para editar.")
            return
        for i, c in enumerate(self.comentarios, 1):
            print(f"{i}.- {c}")
        while True:
            try:
                indice = int(input("Numero del comentario a modificar: ")) - 1
                if 0 <= indice < len(self.comentarios):
                    nuevo = input("Nuevo comentario: ").strip()
                    if nuevo:
                        self.comentarios[indice] = nuevo
                        print("[INFO] Comentario modificado.")
                        self.guardar()
                        return
                    print("[ERROR] El comentario no puede estar vacio.")
                else:
                    print(f"[ERROR] Numero entre 1 y {len(self.comentarios)}.")
            except ValueError:
                print("[ERROR] Numero valido.")

    def eliminar_comentario(self):
        if not self.comentarios:
            print("[INFO] No hay comentarios para eliminar.")
            return
        for i, c in enumerate(self.comentarios, 1):
            print(f"{i}.- {c}")
        while True:
            try:
                indice = int(input(f"Numero del comentario a eliminar (1-{len(self.comentarios)}): ")) - 1
                if 0 <= indice < len(self.comentarios):
                    eliminado = self.comentarios.pop(indice)
                    print(f"[INFO] Comentario eliminado: '{eliminado}'")
                    self.guardar()
                    resp = input("[INFO] Eliminar otro? (s/n): ").strip().lower()
                    if resp != "s":
                        return
                    break
                print("[ERROR] Numero invalido.")
            except ValueError:
                print("[ERROR] Numero valido.")

    def limpiar_comentarios(self):
        if not self.comentarios:
            print("[INFO] La lista ya esta vacia.")
            return
        print(f"Comentarios actuales: {self.comentarios}")
        confirmacion = input(f"ELIMINAR TODOS los comentarios de '{self.nombre}'? (s/n): ").strip().lower()
        if confirmacion == "s":
            cantidad = len(self.comentarios)
            self.comentarios.clear()
            print(f"[INFO] {cantidad} comentarios eliminados.")
            self.guardar()

    def __repr__(self):
        n_et = len(self.etiquetados) if self.etiquetados else 0
        return f"<Dominio: {self.nombre} | URLs: {len(self.urls)} | Etiquetados: {n_et}>"


# -- Instancias --
sorteo_conocidos = Dominio("Etiquetar conocido", MINIMO, LIMITE)
sorteo_seguidor = Dominio("Etiquetar seguidor", MINIMO, LIMITE)
sorteo_personas = Dominio("Etiquetar personas", MINIMO, LIMITE)
sorteo_comentar = Dominio("Solo comentar", MINIMO, LIMITE, requiere_etiquetar=False)

SORTEOS = {
    "1": sorteo_conocidos,
    "2": sorteo_seguidor,
    "3": sorteo_personas,
    "4": sorteo_comentar,
}

carga = storage.cargar()
if carga:
    for clave, datos in carga.items():
        if clave in SORTEOS:
            SORTEOS[clave].deserializar(datos)
    print("[INFO] Datos cargados desde archivo correctamente.")
else:
    print("[INFO] No se encontraron datos previos. Usando configuracion por defecto.")
