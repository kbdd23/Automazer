#Este módulo está encargado de gestionar la información de los objetos. 
#gestiona el JSON.
import json
import os

class Storage:
    """Gestiona la persistencia en JSON. Los archivos se almacenan junto al módulo."""
    def __init__(self, nombre_archivo="datos_sorteos.json"):
        directorio = os.path.dirname(os.path.abspath(__file__))
        self.archivo = os.path.join(directorio, nombre_archivo)

    def guardar(self, diccionario_dominios):
        """Toma el diccionario que crea el objeto Dominio con el método serializar y lo guarda en un archivo JSON"""
        datos_para_json = {}

        for i, dominio_objeto in diccionario_dominios.items():
            datos_para_json[i] = dominio_objeto.serializar()
        
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f: #as f viene de 'file' -> archivo.
                json.dump(datos_para_json, f, ensure_ascii=False, indent=4) #emojis e interoperabilidad
            print(f"[INFO storage.py]: Datos guardados exitosamente en {self.archivo}")
        except Exception as e:
            print(f"[ERROR storage.py]: Fallo al intentar los datos serializados: \n{e}")

    def cargar(self):
        """Lee el archivo JSON y devuelve los datos"""
        #Si no existe, devuelve un diccionario vacio. luego se guardará uno. 
        if not os.path.exists(self.archivo):
            return None #Esto es para la primera ejecución. así no explota en la primera ejecución.
        #Si existe, leelo.
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            print(f"[INFO storage.py]: Datos cargados con éxito desde {self.archivo}")
            return datos #Esto devuelve un diccionario de diccionarios
        except Exception as e:
            print(f"[ERROR storage.py]: Error crítico al leer el archivo JSON: \n{e}")
            return None