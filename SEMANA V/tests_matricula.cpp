// ── tests_matricula.cpp ─────────────────────────────────────────────────
// g++ -std=c++17 -Wall -Wextra -o tests tests_matricula.cpp && ./tests
#include "matricula.hpp"
#include <iostream>
#include <cassert>

void test_constructor_valido() {
    Matricula m("20210500", {"SIS206", "SIS207", "SIS208"});
    assert(m.numCursos() == 3);
    assert(!m.anulada());
    std::cout << "[PASS] constructor válido\n";
}

void test_constructor_sin_cursos() {
    try {
        Matricula m("20210500", {});   // debe lanzar
        assert(false && "No lanzó excepción");
    } catch (const ErrorCapacidad& e) {
        std::cout << "[PASS] constructor sin cursos: " << e.what() << "\n";
    }
}

void test_constructor_demasiados_cursos() {
    try {
        Matricula m("20210500", {"C1", "C2", "C3", "C4", "C5", "C6", "C7"});
        assert(false && "No lanzó excepción");
    } catch (const ErrorCapacidad& e) {
        assert(e.actual() == 7 && e.maximo() == 6);
        std::cout << "[PASS] demasiados cursos: " << e.what() << "\n";
    }
}

void test_constructor_duplicados() {
    try {
        Matricula m("20210500", {"SIS206", "SIS206"});
        assert(false && "No lanzó excepción");
    } catch (const ErrorValidacion& e) {
        std::cout << "[PASS] constructor con duplicados: " << e.what() << "\n";
    }
}

void test_agregar_curso_exitoso() {
    Matricula m("20210500", {"SIS206"});
    m.agregarCurso("SIS207");
    assert(m.numCursos() == 2);
    assert(m.cursos().back() == "SIS207");
    std::cout << "[PASS] agregar curso: " << m.diagnostico() << "\n";
}

void test_agregar_curso_duplicado() {
    Matricula m("20210500", {"SIS206"});
    try {
        m.agregarCurso("SIS206");   // duplicado — debe lanzar
        assert(false && "No lanzó excepción");
    } catch (const ErrorValidacion& e) {
        std::cout << "[PASS] duplicado: " << e.what() << "\n";
    }
}

void test_anular_y_modificar() {
    Matricula m("20210500", {"SIS206"});
    m.anular();
    try {
        m.agregarCurso("SIS207");   // anulada — debe lanzar
        assert(false && "No lanzó excepción");
    } catch (const ErrorAcademico& e) {
        assert(m.numCursos() == 1);
        std::cout << "[PASS] anulada: " << e.what() << " — " << m.diagnostico() << "\n";
    }
}

int main() {
    test_constructor_valido();
    test_constructor_sin_cursos();
    test_constructor_demasiados_cursos();
    test_constructor_duplicados();
    test_agregar_curso_exitoso();
    test_agregar_curso_duplicado();
    test_anular_y_modificar();
    std::cout << "\nTodas las pruebas pasaron.\n";
    return 0;
}
