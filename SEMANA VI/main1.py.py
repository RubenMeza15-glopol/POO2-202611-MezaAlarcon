# repositorio.py - Repositorio generico en un solo archivo
from typing import TypeVar, Generic, Callable, Dict, List, Optional
from dataclasses import dataclass

T = TypeVar("T")       # Tipo de entidad
ID = TypeVar("ID")     # Tipo del identificador


class Repositorio(Generic[T, ID]):
    def __init__(self, fn_id: Callable[[T], ID]):
        self._fn_id = fn_id
        self._datos: Dict[ID, T] = {}

    def guardar(self, entidad: T) -> None:
        self._datos[self._fn_id(entidad)] = entidad

    def buscar(self, identificador: ID) -> Optional[T]:
        return self._datos.get(identificador)

    def eliminar(self, identificador: ID) -> bool:
        return self._datos.pop(identificador, None) is not None

    def todos(self) -> List[T]:
        return list(self._datos.values())

    def filtrar(self, predicado: Callable[[T], bool]) -> List[T]:
        return [e for e in self._datos.values() if predicado(e)]

    def ordenar(self, clave: Callable[[T], object],
                descendente: bool = False) -> List[T]:
        return sorted(self._datos.values(), key=clave, reverse=descendente)

    def acumular(self, inicial, funcion: Callable):
        resultado = inicial
        for entidad in self._datos.values():
            resultado = funcion(resultado, entidad)
        return resultado

    def tamano(self) -> int:
        return len(self._datos)

    def vacio(self) -> bool:
        return len(self._datos) == 0


@dataclass
class Estudiante:
    codigo: int
    nombre: str
    ppa: float
    escuela: str


@dataclass
class Curso:
    codigo: str
    nombre: str
    creditos: int


def main():
    estudiantes = Repositorio[Estudiante, int](lambda e: e.codigo)
    estudiantes.guardar(Estudiante(1001, "Juan Carlos Mamani", 15.2, "Ing. Sistemas"))
    estudiantes.guardar(Estudiante(1002, "Maria Elena Quispe", 18.5, "Ing. Sistemas"))
    estudiantes.guardar(Estudiante(1003, "Pedro Flores", 9.8, "Ciencias Comp."))

    encontrado = estudiantes.buscar(1002)
    if encontrado is not None:
        print("Encontrado:", encontrado.nombre)

    destacados = estudiantes.filtrar(lambda e: e.ppa >= 14.0)
    print("Destacados:", len(destacados))

    ranking = estudiantes.ordenar(lambda e: e.ppa, descendente=True)
    print("\nRanking por PPA:")
    for posicion, e in enumerate(ranking, start=1):
        print(f"{posicion}. {e.nombre} - {e.ppa:.1f}")

    suma = estudiantes.acumular(0.0, lambda acumulado, e: acumulado + e.ppa)
    if not estudiantes.vacio():
        print(f"PPA promedio: {suma / estudiantes.tamano():.2f}")

    cursos = Repositorio[Curso, str](lambda c: c.codigo)
    cursos.guardar(Curso("SIS206", "Programacion Orientada a Objetos II", 4))
    cursos.guardar(Curso("MAT101", "Matematica", 3))

    print("\nCursos registrados:", cursos.tamano())
    curso = cursos.buscar("SIS206")
    if curso is not None:
        print("Curso encontrado:", curso.nombre)


if __name__ == "__main__":
    main()
