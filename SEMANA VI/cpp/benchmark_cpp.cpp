// ── benchmark_cpp.cpp — comparación vector vs unordered_map ─────────────
// g++ -std=c++17 -Wall -Wextra -O2 -o bench benchmark_cpp.cpp
#include <vector>
#include <unordered_map>
#include <chrono>
#include <iostream>
#include <iomanip>
#include <numeric>
#include <algorithm>

using Clock = std::chrono::high_resolution_clock;
using Ms = std::chrono::duration<double, std::milli>;   // ms con decimales

void benchmarkBusqueda(int n) {
    // Datos: n enteros
    std::vector<int> vec(n);
    std::iota(vec.begin(), vec.end(), 0);

    std::unordered_map<int, int> umap;
    for (int i = 0; i < n; ++i) umap[i] = i;

    volatile int buscar = n / 2;   // volatile: el compilador no puede precalcular la búsqueda
    int repeticiones = 10000;
    long long encontrados = 0;     // se usa el resultado para que -O2 no elimine el bucle

    // ── Benchmark vector (búsqueda lineal) ──────────────────────────────
    auto t0 = Clock::now();
    for (int r = 0; r < repeticiones; ++r) {
        const int clave = buscar;   // lectura volatile en cada repetición
        encontrados += std::find(vec.begin(), vec.end(), clave) != vec.end();
    }
    auto t1 = Clock::now();
    double vec_ms = Ms(t1 - t0).count();

    // ── Benchmark unordered_map (hash) ──────────────────────────────────
    auto t2 = Clock::now();
    for (int r = 0; r < repeticiones; ++r) {
        const int clave = buscar;
        encontrados += umap.find(clave) != umap.end();
    }
    auto t3 = Clock::now();
    double map_ms = Ms(t3 - t2).count();

    std::cout << std::fixed << std::setprecision(3) << "n=" << n << ": vector=" << vec_ms
              << "ms  unordered_map=" << map_ms << "ms  (encontrados=" << encontrados << ")\n";
}

int main() {
    for (int n : {1000, 10000, 100000, 1000000})
        benchmarkBusqueda(n);
    return 0;
}
