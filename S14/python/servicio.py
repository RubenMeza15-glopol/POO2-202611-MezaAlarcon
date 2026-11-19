# SEMANA 14 - SERVICIO DE ESTUDIANTES

from estudiante import Estudiante


class ServicioEstudiante:

    def __init__(self, repo, calculadora):

        self.repo = repo
        self.calculadora = calculadora

    def registrar(self, estudiante: Estudiante):

        if self.repo.buscar(estudiante.codigo):
            raise ValueError(
                "El código ya está registrado."
            )

        estudiante.ppa = self.calculadora.calcular(
            estudiante.notas
        )

        self.repo.guardar(estudiante)

    def buscar(self, codigo: int):

        return self.repo.buscar(codigo)

    def listar(self):

        return self.repo.listar()

    def actualizar(self, estudiante: Estudiante):

        if not self.repo.buscar(estudiante.codigo):
            raise ValueError(
                "El estudiante no existe."
            )

        estudiante.ppa = self.calculadora.calcular(
            estudiante.notas
        )

        self.repo.guardar(estudiante)

    def eliminar(self, codigo: int):

        return self.repo.eliminar(codigo)