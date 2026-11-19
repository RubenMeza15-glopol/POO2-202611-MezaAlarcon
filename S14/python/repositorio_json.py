# SEMANA 14 - REPOSITORIO JSON

import json
from pathlib import Path
from dataclasses import asdict

from estudiante import Estudiante


class RepositorioJSON:

    def __init__(self, ruta: str):

        self.ruta = Path(ruta)
        self.datos = {}

        self.cargar()

    def cargar(self):

        if not self.ruta.exists():
            return

        with self.ruta.open(
            "r", encoding="utf-8"
        ) as archivo:

            lista = json.load(archivo)

            for item in lista:
                estudiante = Estudiante(**item)

                self.datos[estudiante.codigo] = estudiante

    def persistir(self):

        lista = [
            asdict(e)
            for e in self.datos.values()
        ]

        with self.ruta.open(
            "w", encoding="utf-8"
        ) as archivo:

            json.dump(
                lista,
                archivo,
                indent=4,
                ensure_ascii=False
            )

    def guardar(self, estudiante: Estudiante):

        self.datos[estudiante.codigo] = estudiante
        self.persistir()

    def buscar(self, codigo: int):

        return self.datos.get(codigo)

    def listar(self):

        return list(self.datos.values())

    def eliminar(self, codigo: int):

        if codigo in self.datos:
            del self.datos[codigo]
            self.persistir()
            return True

        return False