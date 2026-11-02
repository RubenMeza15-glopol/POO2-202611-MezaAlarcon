// ── main.cpp — Actividad 1A: captura selectiva ─────────────────────────
// g++ -std=c++17 -Wall -Wextra -o act1 main.cpp
#include <functional>
#include <iostream>

#include "excepciones_dominio.hpp"

void ejecutar(const std::string& caso, const std::function<void()>& accion) {
    std::cout << "── " << caso << "\n";
    try {
        accion();
        std::cout << "   sin errores\n";
    }
    catch (const ErrorCalificacion& e) {          // 1.° más específico
        std::cout << "   Nota inválida: " << e.valor() << "\n   " << e.what() << "\n";
    }
    catch (const ErrorMatriculaDuplicada& e) {    // 1.° más específico
        std::cout << "   Duplicado (" << e.codigo_estudiante() << "): " << e.what() << "\n";
    }
    catch (const ErrorValidacion& e) {            // 2.° rama validación
        std::cout << "   Validación: " << e.what() << "\n";
    }
    catch (const ErrorAcademico& e) {             // 3.° cualquier dominio
        std::cout << "   Dominio: " << e.what() << "\n";
    }
    catch (const std::exception& e) {             // 4.° cualquier std
        std::cout << "   Sistema: " << e.what() << "\n";
    }
}

int main() {
    std::vector<int> matriculados = {20210500, 20210501};

    ejecutar("registrar_nota(25)", [] { registrar_nota(25.0f); });
    ejecutar("registrar_nota(18)", [] { registrar_nota(18.0f); });
    ejecutar("validar_matricula(20210502)", [&] { validar_matricula(20210502, matriculados); });
    ejecutar("validar_matricula(20210500)", [&] { validar_matricula(20210500, matriculados); });
    ejecutar("ErrorCapacidad", [] { throw ErrorCapacidad(30, 30, "SIS206"); });
    ejecutar("ErrorRecursoNoEncontrado", [] { throw ErrorRecursoNoEncontrado("Curso", 999); });
    ejecutar("std::out_of_range", [] { std::vector<int> v; (void)v.at(3); });
    return 0;
}
