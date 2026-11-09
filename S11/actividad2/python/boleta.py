
# ACTIVIDAD 2: FACTORY METHOD - GENERADOR DE BOLETAS.
# Implementación en Python 3.12.

# Importa json para leer el archivo de configuración.
import json

# Importa ABC y abstractmethod para crear clases abstractas.
from abc import ABC, abstractmethod

# Importa dataclass y field para facilitar el almacenamiento de datos.
from dataclasses import dataclass, field

# Importa Path para construir rutas de archivos.
from pathlib import Path

# Importa Callable para indicar que un atributo almacena una función creadora.
from typing import Callable


# ==========================================================
# 1. PRODUCTO ABSTRACTO
# ==========================================================

# Define el contrato que deben cumplir todas las boletas.
class BoletaNotas(ABC):

    # Obliga a las clases concretas a implementar este método.
    @abstractmethod
    def agregar_nota(self, asignatura: str, valor: float) -> None:
        pass

    # Obliga a generar el contenido de la boleta.
    @abstractmethod
    def generar(self, estudiante: str, promedio: float) -> str:
        pass

    # Obliga a indicar la extensión del documento.
    @property
    @abstractmethod
    def extension(self) -> str:
        pass


# ==========================================================
# 2. PRODUCTOS CONCRETOS
# ==========================================================

# Genera una boleta en formato TXT.
@dataclass
class BoletaTXT(BoletaNotas):

    # Lista donde se guardarán las asignaturas y sus notas.
    notas: list[tuple[str, float]] = field(default_factory=list)

    # Agrega una asignatura y su calificación.
    def agregar_nota(self, asignatura: str, valor: float) -> None:
        self.notas.append((asignatura, valor))

    # Genera el documento en texto plano.
    def generar(self, estudiante: str, promedio: float) -> str:

        # Crea las primeras líneas del documento.
        lineas = [
            "BOLETA DE NOTAS",
            f"Estudiante: {estudiante}",
            "----------------------------"
        ]

        # Recorre las notas almacenadas.
        for asignatura, valor in self.notas:

            # Agrega cada asignatura con dos decimales.
            lineas.append(f"{asignatura}: {valor:.2f}")

        # Agrega el promedio final.
        lineas.append(f"Promedio: {promedio:.2f}")

        # Une las líneas y devuelve el documento.
        return "\n".join(lineas)

    # Devuelve la extensión del formato.
    @property
    def extension(self) -> str:
        return ".txt"


# Genera una boleta en formato CSV.
@dataclass
class BoletaCSV(BoletaNotas):

    # Almacena las notas.
    notas: list[tuple[str, float]] = field(default_factory=list)

    # Agrega una asignatura y su calificación.
    def agregar_nota(self, asignatura: str, valor: float) -> None:
        self.notas.append((asignatura, valor))

    # Genera el contenido separado por comas.
    def generar(self, estudiante: str, promedio: float) -> str:

        # Define los encabezados de las columnas.
        lineas = ["Estudiante,Asignatura,Nota"]

        # Recorre todas las notas.
        for asignatura, valor in self.notas:

            # Agrega una fila al documento CSV.
            lineas.append(
                f"{estudiante},{asignatura},{valor:.2f}"
            )

        # Agrega una fila con el promedio.
        lineas.append(
            f"{estudiante},Promedio,{promedio:.2f}"
        )

        # Devuelve el documento completo.
        return "\n".join(lineas)

    # Devuelve la extensión CSV.
    @property
    def extension(self) -> str:
        return ".csv"


# Genera una boleta en formato HTML.
@dataclass
class BoletaHTML(BoletaNotas):

    # Almacena las notas.
    notas: list[tuple[str, float]] = field(default_factory=list)

    # Agrega una asignatura y su calificación.
    def agregar_nota(self, asignatura: str, valor: float) -> None:
        self.notas.append((asignatura, valor))

    # Genera el documento HTML.
    def generar(self, estudiante: str, promedio: float) -> str:

        # Crea una lista para almacenar las filas de la tabla.
        filas = []

        # Recorre las notas registradas.
        for asignatura, valor in self.notas:

            # Construye una fila HTML para cada nota.
            filas.append(
                f"<tr><td>{asignatura}</td>"
                f"<td>{valor:.2f}</td></tr>"
            )

        # Une todas las filas HTML.
        tabla = "\n".join(filas)

        # Devuelve la página HTML completa.
        return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Boleta de notas</title>
</head>
<body>
    <h1>Boleta de notas</h1>
    <p><strong>Estudiante:</strong> {estudiante}</p>

    <table border="1">
        <tr>
            <th>Asignatura</th>
            <th>Nota</th>
        </tr>
        {tabla}
    </table>

    <p><strong>Promedio:</strong> {promedio:.2f}</p>
</body>
</html>"""

    # Devuelve la extensión HTML.
    @property
    def extension(self) -> str:
        return ".html"


# ==========================================================
# 3. CREADOR BASE: FACTORY METHOD Y TEMPLATE METHOD
# ==========================================================

# Define el creador abstracto.
class GeneradorBoleta(ABC):

    # Factory Method: cada subclase decide qué boleta crear.
    @abstractmethod
    def crear_boleta(self) -> BoletaNotas:
        pass

    # Template Method: establece el proceso general de generación.
    def generar_y_enviar(
        self,
        estudiante: str,
        promedio: float,
        notas: list[dict],
        nombre_base: str
    ) -> Path:

        # Solicita al Factory Method crear el producto.
        boleta = self.crear_boleta()

        # Recorre las notas recibidas desde el JSON.
        for nota in notas:

            # Agrega cada nota a la boleta.
            boleta.agregar_nota(
                nota["asignatura"],
                float(nota["valor"])
            )

        # Genera el contenido del documento.
        contenido = boleta.generar(estudiante, promedio)

        # Construye el nombre final del archivo.
        archivo = Path(nombre_base + boleta.extension)

        # Escribe el documento utilizando codificación UTF-8.
        archivo.write_text(contenido, encoding="utf-8")

        # Informa que el documento fue creado.
        print(f"Boleta generada: {archivo}")

        # Simula el envío al estudiante.
        print(f"Envío simulado al estudiante: {estudiante}")

        # Devuelve la ruta del documento generado.
        return archivo


# ==========================================================
# 4. CREADORES CONCRETOS
# ==========================================================

# Creador que fabrica boletas TXT.
class GeneradorTXT(GeneradorBoleta):

    # Implementa el Factory Method.
    def crear_boleta(self) -> BoletaNotas:
        return BoletaTXT()


# Creador que fabrica boletas CSV.
class GeneradorCSV(GeneradorBoleta):

    # Implementa el Factory Method.
    def crear_boleta(self) -> BoletaNotas:
        return BoletaCSV()


# Creador que fabrica boletas HTML.
class GeneradorHTML(GeneradorBoleta):

    # Implementa el Factory Method.
    def crear_boleta(self) -> BoletaNotas:
        return BoletaHTML()


# ==========================================================
# 5. REGISTRO DINÁMICO DE GENERADORES
# ==========================================================

# Permite registrar y recuperar fábricas según el formato.
class RegistroGeneradores:

    # Constructor del registro.
    def __init__(self) -> None:

        # Diccionario que relaciona formato con creador.
        self._registro: dict[
            str, Callable[[], GeneradorBoleta]
        ] = {}

    # Registra una fábrica.
    def registrar(
        self,
        formato: str,
        creador: Callable[[], GeneradorBoleta]
    ) -> None:

        # Guarda el creador usando el formato como clave.
        self._registro[formato.lower()] = creador

    # Crea el generador solicitado.
    def crear(self, formato: str) -> GeneradorBoleta:

        # Convierte el formato a minúsculas.
        clave = formato.lower()

        # Comprueba que el formato esté registrado.
        if clave not in self._registro:
            raise ValueError(
                f"Formato no registrado: {formato}"
            )

        # Ejecuta la fábrica y devuelve el generador.
        return self._registro[clave]()


# ==========================================================
# 6. FUNCIÓN PRINCIPAL
# ==========================================================

def main() -> None:

    # Busca config.json en la misma carpeta que este programa.
    ruta_config = Path(__file__).resolve().parent / "config.json"

    # Abre el archivo de configuración.
    with ruta_config.open("r", encoding="utf-8") as archivo:

        # Convierte el JSON en un diccionario Python.
        config = json.load(archivo)

    # Obtiene el nombre del estudiante.
    estudiante = config["estudiante"]

    # Obtiene el promedio como número decimal.
    promedio = float(config["promedio"])

    # Obtiene el nombre base de los documentos.
    nombre_base = config.get("nombre_base", "boleta")

    # Obtiene la lista de notas.
    notas = config["notas"]

    # Crea el registro de generadores.
    registro = RegistroGeneradores()

    # Registra el generador TXT.
    registro.registrar("txt", GeneradorTXT)

    # Registra el generador CSV.
    registro.registrar("csv", GeneradorCSV)

    # Registra el generador HTML.
    registro.registrar("html", GeneradorHTML)

    # Recorre los formatos indicados en el JSON.
    for formato in config["formatos"]:

        # Obtiene el generador adecuado.
        generador = registro.crear(formato)

        # Ejecuta el proceso completo de generación.
        generador.generar_y_enviar(
            estudiante,
            promedio,
            notas,
            nombre_base
        )


# Comprueba si el archivo se ejecuta directamente.
if __name__ == "__main__":

    # Inicia el programa.
    main()
