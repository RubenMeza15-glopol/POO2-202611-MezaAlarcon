// ── pipeline.cpp — Actividad 3: Result<T> y pipeline encadenado ────────
// g++ -std=c++17 -Wall -Wextra -o pipeline pipeline.cpp
#include <iostream>
#include <unordered_map>

#include "result.hpp"

struct Estudiante {
    int codigo;
    std::string nombre;
    float ppa;
};

const std::unordered_map<int, Estudiante> db = {
    {1001, {1001, "Juan Mamani", 15.0f}},
    {1002, {1002, "Rosa Quispe", 11.5f}},
};

constexpr float PPA_MINIMO = 12.0f;

Result<Estudiante> buscar_estudiante(int codigo) {
    auto it = db.find(codigo);
    if (it == db.end())
        return Result<Estudiante>::fallo("Código " + std::to_string(codigo) + " no encontrado");
    return Result<Estudiante>::ok(it->second);
}

Result<Estudiante> validar_ppa_minimo(const Estudiante& est) {
    if (est.ppa < PPA_MINIMO)
        return Result<Estudiante>::fallo(est.nombre + ": PPA " + std::to_string(est.ppa).substr(0, 5)
                                         + " < " + std::to_string(PPA_MINIMO).substr(0, 5));
    return Result<Estudiante>::ok(est);
}

Result<std::string> inscribir(const Estudiante& est, const std::string& curso) {
    return Result<std::string>::ok(est.nombre + " inscrito en " + curso);
}

void procesar(int codigo) {
    auto resultado = buscar_estudiante(codigo)
                         .map(validar_ppa_minimo)
                         .map([](const Estudiante& e) { return inscribir(e, "SIS206"); });
    if (resultado.esExito())
        std::cout << "[OK]    " << resultado.valor() << "\n";
    else
        std::cout << "[FALLO] " << resultado.error() << "\n";
}

int main() {
    procesar(1001);   // éxito
    procesar(9999);   // falla en el paso 1 (no existe)
    procesar(1002);   // falla en el paso 2 (PPA insuficiente)

    // map con una función que retorna un valor simple (no Result)
    auto longitud = buscar_estudiante(1001).map([](const Estudiante& e) { return e.nombre.size(); });
    std::cout << "Longitud del nombre: " << longitud.valor() << "\n";

    try {
        buscar_estudiante(9999).valor();   // acceder al valor de un fallo
    } catch (const std::logic_error& e) {
        std::cout << "Error esperado: " << e.what() << "\n";
    }
    return 0;
}
