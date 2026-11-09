# Importa sqlite3 para trabajar con SQLite.
import sqlite3

# Importa la interfaz del repositorio.
from .repositorio import Repositorio

# Define el repositorio basado en base de datos.
class RepositorioBD(Repositorio):

    # Inicializa la conexión y crea la tabla.
    def __init__(self, ruta="academico.db"):

        # Guarda la ruta de la base de datos.
        self.ruta = ruta

        # Abre la conexión con SQLite.
        with sqlite3.connect(self.ruta) as conexion:

            # Crea la tabla si todavía no existe.
            conexion.execute("""
                CREATE TABLE IF NOT EXISTS estudiantes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL
                )
            """)

    # Guarda un estudiante en la base de datos.
    def guardar(self, estudiante):

        # Abre una conexión.
        with sqlite3.connect(self.ruta) as conexion:

            # Inserta el nombre de forma segura.
            conexion.execute(
                "INSERT INTO estudiantes (nombre) VALUES (?)",
                (estudiante,)
            )

    # Recupera los estudiantes registrados.
    def listar(self):

        # Abre la conexión con SQLite.
        with sqlite3.connect(self.ruta) as conexion:

            # Ejecuta la consulta SQL.
            resultado = conexion.execute(
                "SELECT nombre FROM estudiantes"
            ).fetchall()

            # Devuelve una lista con los nombres.
            return [fila[0] for fila in resultado]