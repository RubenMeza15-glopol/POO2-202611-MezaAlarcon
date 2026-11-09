# Importa json para manejar datos.
import json

# Importa la interfaz del repositorio.
from .repositorio import Repositorio

# Define el repositorio basado en archivos.
class RepositorioArchivo(Repositorio):

    # Inicializa la ruta del archivo.
    def __init__(self, ruta="estudiantes.json"):
        self.ruta = ruta

    # Guarda un estudiante en el archivo.
    def guardar(self, estudiante):

        # Recupera los estudiantes existentes.
        estudiantes = self.listar()

        # Agrega el nuevo estudiante.
        estudiantes.append(estudiante)

        # Abre el archivo para escritura.
        with open(self.ruta, "w", encoding="utf-8") as archivo:

            # Guarda la lista en formato JSON.
            json.dump(
                estudiantes,
                archivo,
                ensure_ascii=False,
                indent=4
            )

    # Recupera los estudiantes del archivo.
    def listar(self):

        # Intenta abrir el archivo.
        try:
            with open(self.ruta, "r", encoding="utf-8") as archivo:

                # Devuelve los datos convertidos desde JSON.
                return json.load(archivo)

        # Si el archivo todavía no existe, devuelve una lista vacía.
        except FileNotFoundError:
            return []