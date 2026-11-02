// ── main_iterador.cpp — Actividad 3: PlanillaIterador en range-for ─────
// g++ -std=c++17 -Wall -Wextra -o iterador main_iterador.cpp
#include <iomanip>
#include <iostream>
#include <string>

#include "iterador_planilla.hpp"

class Trabajador {
    std::string nombre_;
    float base_;
    float bono_;

public:
    Trabajador(std::string nombre, float base, float bono)
        : nombre_(std::move(nombre)), base_(base), bono_(bono) {}
    const std::string& nombre() const { return nombre_; }
    float calcularRemuneracion() const { return base_ + bono_; }
};

int main() {
    PlanillaIterador<Trabajador> planilla({
        {"Mamani Quispe, Juan Carlos", 1680.0f, 0.0f},
        {"Quispe Torres, María Elena", 1620.0f, 0.0f},
        {"Huanca Lazo, Pedro", 2800.0f, 350.0f},
        {"Flores Ramos, Ana Lucía", 3000.0f, 0.0f},
    });

    std::cout << "Ranking de remuneraciones:\n";
    int i = 0;
    for (const auto& t : planilla)
        std::cout << "  " << ++i << ". " << t.nombre() << " — S/ " << std::fixed
                  << std::setprecision(2) << t.calcularRemuneracion() << "\n";
    return 0;
}
