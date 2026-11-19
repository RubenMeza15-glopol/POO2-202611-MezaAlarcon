
# SEMANA 13 - ACTIVIDAD 3
# REPOSITORIO SQLITE

# Importa SQLite para trabajar con bases de datos.
import sqlite3

# Permite convertir listas de notas a texto JSON.
import json

# Permite indicar que una búsqueda puede devolver None.
from typing import Optional

# Importa el modelo Estudiante.
from estudiante import Estudiante


# Instrucción SQL para crear la tabla de estudiantes.
CREATE_SQL = """
CREATE TABLE IF NOT EXISTS estudiante(
    codigo INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    ppa REAL NOT NULL DEFAULT 0,
    notas TEXT NOT NULL DEFAULT '[]'
)
"""


# Repositorio que almacena estudiantes en SQLite.
class RepositorioSQLite:

    # Constructor: recibe la ruta de la base de datos.
    def __init__(self, ruta: str) -> None:

        # Abre la conexión con la base de datos.
        self._con = sqlite3.connect(
            ruta,
            check_same_thread=False
        )

        # Crea la tabla si todavía no existe.
        self._con.execute(CREATE_SQL)

        # Confirma los cambios.
        self._con.commit()

    # Guarda o actualiza un estudiante.
    def guardar(self, e: Estudiante) -> None:

        # Ejecuta una inserción o sustitución.
        self._con.execute(
            """
            INSERT OR REPLACE INTO estudiante
            (codigo, nombre, ppa, notas)
            VALUES (?, ?, ?, ?)
            """,
            (
                e.codigo,
                e.nombre,
                e.ppa,
                json.dumps(e.notas)
            )
        )

        # Confirma el registro en la base de datos.
        self._con.commit()

    # Busca un estudiante por su código.
    def buscar(self, cod: int) -> Optional[Estudiante]:

        # Ejecuta la consulta SQL.
        row = self._con.execute(
            "SELECT * FROM estudiante WHERE codigo = ?",
            (cod,)
        ).fetchone()

        # Si no encuentra el registro, devuelve None.
        if row is None:
            return None

        # Convierte la fila encontrada en un objeto.
        return Estudiante(
            row[0],
            row[1],
            row[2],
            json.loads(row[3])
        )

    # Lista todos los estudiantes registrados.
    def listar(self) -> list[Estudiante]:

        # Recupera todas las filas de la tabla.
        rows = self._con.execute(
            "SELECT * FROM estudiante"
        ).fetchall()

        # Convierte las filas en objetos Estudiante.
        return [
            Estudiante(
                row[0],
                row[1],
                row[2],
                json.loads(row[3])
            )
            for row in rows
        ]

    # Cierra la conexión con SQLite.
    def cerrar(self) -> None:

        # Libera la conexión.
        self._con.close()
