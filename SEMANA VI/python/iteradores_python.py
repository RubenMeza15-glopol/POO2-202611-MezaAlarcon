# ── iteradores_python.py — Actividad 3: generador, ColaAtencion y benchmark ──
import timeit
from collections import deque
from typing import Iterator


# ── Generador: más idiomático y eficiente en memoria ─────────────────────
def ventana_deslizante(datos: list, k: int) -> Iterator[list]:
    """
    Genera ventanas de tamaño k sobre una secuencia.
    Útil para promedios móviles de calificaciones.

    Ejemplo:
        list(ventana_deslizante([12, 15, 18, 14, 16], k=3))
        → [[12,15,18], [15,18,14], [18,14,16]]
    """
    if k > len(datos):
        raise ValueError(f"Ventana k={k} mayor que datos={len(datos)}")
    for i in range(len(datos) - k + 1):
        yield datos[i: i + k]  # yield suspende y retorna la ventana


# ── ColaAtencion con deque — FIFO O(1) en ambos extremos ─────────────────
class ColaAtencion:
    """
    Cola de atención FIFO para matrícula.
    deque es preferible a list porque append/popleft son O(1).
    list.pop(0) es O(n) porque desplaza todos los elementos.
    """

    def __init__(self):
        self._cola: deque = deque()

    def encolar(self, elemento) -> None:
        self._cola.append(elemento)  # O(1)

    def atender(self) -> object | None:
        return self._cola.popleft() if self._cola else None  # O(1)

    def __len__(self) -> int: return len(self._cola)
    def __iter__(self): return iter(self._cola)
    def __bool__(self) -> bool: return bool(self._cola)


def benchmark_cola(n: int = 10_000, repeticiones: int = 20) -> tuple[float, float]:
    """Vacía una cola de n elementos con deque.popleft() y con list.pop(0)."""
    def vaciar_deque():
        d = deque(range(n))
        while d:
            d.popleft()

    def vaciar_list():
        lst = list(range(n))
        while lst:
            lst.pop(0)

    t_deque = timeit.timeit(vaciar_deque, number=repeticiones) / repeticiones * 1000
    t_list = timeit.timeit(vaciar_list, number=repeticiones) / repeticiones * 1000
    return t_deque, t_list


if __name__ == "__main__":
    calificaciones = [10.0, 14.5, 18.0, 12.5, 16.0, 11.0, 19.0]
    print("Promedios móviles (ventana=3):")
    for ventana in ventana_deslizante(calificaciones, k=3):
        prom = sum(ventana) / len(ventana)
        print(f"  {ventana} → promedio: {prom:.2f}")

    cola = ColaAtencion()
    for nombre in ["Juan Mamani", "María Quispe", "Pedro Flores", "Ana Torres"]:
        cola.encolar(nombre)
    print(f"\nAtención en orden FIFO ({len(cola)} en cola):")
    while cola:
        print(f"  → Atendido: {cola.atender()}")

    for n in (10_000, 20_000, 40_000):
        t_deque, t_list = benchmark_cola(n)
        print(f"\nVaciar {n:,} elementos: deque.popleft() = {t_deque:.3f} ms | "
              f"list.pop(0) = {t_list:.3f} ms | list es {t_list / t_deque:.1f}x más lento")
