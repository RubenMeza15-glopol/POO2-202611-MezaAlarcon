# ── benchmark_python.py — comparación list vs dict vs set ───────────────
import timeit


def benchmark(n: int) -> dict:
    datos = list(range(n))
    buscar = n // 2   # elemento del medio, igual que en el benchmark C++
    # Las estructuras se construyen UNA vez: se mide solo la búsqueda
    como_dict = dict.fromkeys(datos)
    como_set = set(datos)

    t_list = timeit.timeit(lambda: buscar in datos, number=5000)
    t_dict = timeit.timeit(lambda: buscar in como_dict, number=5000)
    t_set = timeit.timeit(lambda: buscar in como_set, number=5000)

    return {"n": n, "list_ms": t_list * 1000,
            "dict_ms": t_dict * 1000, "set_ms": t_set * 1000}


if __name__ == "__main__":
    print(f"{"N":>10} {"list(ms)":>12} {"dict(ms)":>12} {"set(ms)":>12}")
    print("-" * 48)
    for n in [1_000, 10_000, 100_000, 1_000_000]:
        r = benchmark(n)
        print(f"{r["n"]:>10,} {r["list_ms"]:>12.3f} {r["dict_ms"]:>12.3f} {r["set_ms"]:>12.3f}")

# Pregunta: ¿por qué dict y set tienen tiempo constante independiente de n?
# Pregunta: ¿en qué situación sería preferible list ordenado + bisect.bisect?
