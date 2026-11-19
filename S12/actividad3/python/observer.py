
# ACTIVIDAD 3 - MVC CON OBSERVER
# Define los observadores y el repositorio observable.

from typing import Protocol
from estudiante import Estudiante
from repositorio_memoria import RepositorioMemoria

# Contrato que deben cumplir los observadores.
class IObserverEstudiante(Protocol):
    def on_guardado(self, estudiante: Estudiante) -> None:
        ...

# Observador que muestra los datos en pantalla.
class ConsolaObservador:
    def on_guardado(self, estudiante: Estudiante) -> None:
        print(
            f">> Vista: [{estudiante.codigo}] "
            f"{estudiante.nombre} - PPA: {estudiante.ppa:.1f}"
        )

# Observador que registra las notificaciones.
class LoggerObservador:
    def on_guardado(self, estudiante: Estudiante) -> None:
        print(
            f"[LOG] HH:MM:SS Guardado: "
            f"[{estudiante.codigo}] {estudiante.nombre}"
        )

# Repositorio que notifica cuando se guarda un estudiante.
class RepositorioObservable:
    def __init__(self, repositorio: RepositorioMemoria):
        self.repositorio = repositorio
        self.observadores = []

    # Suscribe un observador.
    def suscribir(self, observador: IObserverEstudiante):
        self.observadores.append(observador)

    # Guarda y notifica a todos los observadores.
    def guardar(self, estudiante: Estudiante):
        self.repositorio.guardar(estudiante)

        for observador in self.observadores:
            observador.on_guardado(estudiante)

    # Busca un estudiante.
    def buscar(self, codigo: int):
        return self.repositorio.buscar(codigo)

    # Lista los estudiantes.
    def listar(self):
        return self.repositorio.listar()
