
# =====================================================
# ACTIVIDAD 1: PATRON OBSERVER - PYTHON 3.12
# Define los observadores y el repositorio observable.
# =====================================================

# Permite definir interfaces y contratos.
from typing import Protocol

# Importa la clase Estudiante.
from estudiante import Estudiante

# Importa el Logger Singleton que desarrollamos
# anteriormente en el proyecto final.
#from proyecto_final.singleton.logger import Logger


# =====================================================
# INTERFAZ OBSERVER
# =====================================================

class IObserverEstudiante(Protocol):

    # Todo observador debe implementar este método.
    def on_guardado(self, e: Estudiante) -> None:
        ...


# =====================================================
# OBSERVADOR LOGGER
# =====================================================

class LoggerObserver:
    def on_guardado(self, e: Estudiante) -> None:
        print(
            f"[LOGGER] Guardado: [{e.codigo}] "
            f"{e.nombre}"
        )

# =====================================================
# OBSERVADOR CONSOLA
# =====================================================

class ConsolaObserver:

    # Recibe el evento de estudiante guardado.
    def on_guardado(self, e: Estudiante) -> None:

        # Muestra el estudiante en la terminal.
        print(f"[VISTA] {e}")


# =====================================================
# SUJETO OBSERVABLE
# =====================================================

class RepositorioObservable:

    def __init__(self):

        # Lista donde se almacenan los estudiantes.
        self._estudiantes: list[Estudiante] = []

        # Lista de observadores suscritos.
        self._observadores: list[IObserverEstudiante] = []

    # Suscribe un nuevo observador.
    def suscribir(self, observador: IObserverEstudiante) -> None:
        self._observadores.append(observador)

    # Guarda un estudiante y notifica a los observadores.
    def guardar(self, estudiante: Estudiante) -> None:

        # Almacena el estudiante.
        self._estudiantes.append(estudiante)

        # Notifica a todos los observadores suscritos.
        for observador in self._observadores:
            observador.on_guardado(estudiante)

    # Busca un estudiante por su código.
    def buscar(self, codigo: int) -> Estudiante | None:

        for estudiante in self._estudiantes:
            if estudiante.codigo == codigo:
                return estudiante

        return None

    # Devuelve todos los estudiantes registrados.
    def listar(self) -> list[Estudiante]:
        return self._estudiantes.copy()
