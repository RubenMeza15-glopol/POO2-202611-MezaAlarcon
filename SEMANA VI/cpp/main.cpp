// ── main.cpp — Actividad 1: uso del Repositorio con tipos del dominio ──
// g++ -std=c++17 -Wall -Wextra -O2 -o repo main.cpp
#include "repositorio.hpp"
#include <iostream>
#include <iomanip>
#include <string>

struct Estudiante {
    int codigo;
    std::string nombre;
    float ppa;
    std::string escuela;
};

struct Curso {
    std::string codigo;
    std::string nombre;
    int creditos;
};

int main() {
    // ── Repositorio<Estudiante, int> ─────────────────────────────────────
    Repositorio<Estudiante, int> repo([](const Estudiante& e) { return e.codigo; });

    repo.guardar({1001, "Juan Carlos Mamani", 15.2f, "Ing. Sistemas"});
    repo.guardar({1002, "María Elena Quispe", 18.5f, "Ing. Sistemas"});
    repo.guardar({1003, "Pedro Flores", 9.8f, "Ciencias Comp."});
    repo.guardar({1004, "Ana Torres", 13.0f, "Ing. Sistemas"});
    repo.guardar({1005, "Luis Condori", 16.4f, "Ciencias Comp."});

    // Búsqueda — retorna std::optional
    if (auto res = repo.buscar(1001)) std::cout << "Encontrado: " << res->nombre << "\n";
    if (!repo.buscar(9999)) std::cout << "Código 9999: no existe\n";

    std::cout << std::boolalpha << "existe(1003): " << repo.existe(1003)
              << "  existe(2000): " << repo.existe(2000) << "\n";

    // Filtrar: PPA >= 14.0
    auto destacados = repo.filtrar([](const Estudiante& e) { return e.ppa >= 14.0f; });
    std::cout << "Destacados (PPA >= 14): " << destacados.size() << "\n";

    // contar: Ing. Sistemas
    std::cout << "Estudiantes de Ing. Sistemas: "
              << repo.contar([](const Estudiante& e) { return e.escuela == "Ing. Sistemas"; }) << "\n";

    // primero: alguno desaprobado
    if (auto d = repo.primero([](const Estudiante& e) { return e.ppa < 10.5f; }))
        std::cout << "Primer desaprobado encontrado: " << d->nombre << "\n";

    // Ordenar: PPA descendente (mejor primero)
    auto ranking = repo.ordenar([](const Estudiante& a, const Estudiante& b) { return a.ppa > b.ppa; });
    std::cout << "\nRanking por PPA:\n";
    int i = 0;
    for (const auto& e : ranking)
        std::cout << "  " << ++i << ". " << e.nombre << " — " << std::fixed
                  << std::setprecision(2) << e.ppa << "\n";

    // Suma total y promedio de PPA con acumular
    float suma = repo.acumular(0.0f, [](float acc, const Estudiante& e) { return acc + e.ppa; });
    std::cout << "\nSuma total de PPA: " << suma << "\n";
    std::cout << "PPA promedio: " << suma / static_cast<float>(repo.tamaño()) << "\n";

    // ── Repositorio<Curso, std::string> — mismo template, otro tipo ──────
    Repositorio<Curso, std::string> cursos([](const Curso& c) { return c.codigo; });
    cursos.guardar({"SIS206", "POO II", 4});
    cursos.guardar({"SIS207", "Base de Datos II", 4});
    cursos.guardar({"SIS210", "Redes I", 3});
    int creditos = cursos.acumular(0, [](int acc, const Curso& c) { return acc + c.creditos; });
    std::cout << "\nCursos: " << cursos.tamaño() << ", créditos totales: " << creditos << "\n";
    std::cout << "Cursos de 4 créditos: "
              << cursos.contar([](const Curso& c) { return c.creditos == 4; }) << "\n";
    std::cout << "eliminar(SIS210): " << cursos.eliminar("SIS210")
              << "  eliminar(SIS999): " << cursos.eliminar("SIS999") << "\n";
    return 0;
}
