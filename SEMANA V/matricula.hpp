// ── matricula.hpp — clase Matricula con DbC completo ────────────────────
#pragma once
#include "errores_academicos.hpp"
#include <vector>
#include <string>
#include <algorithm>
#include <cassert>
#include <chrono>

class Matricula {
    /*
     * INVARIANTE de clase:
     *   !estudiante_codigo_.empty()
     *   1 <= cursos_.size() <= MAX_CURSOS
     *   No hay duplicados en cursos_
     *   anulada_ == true  =>  cursos_ no se modifica
     */
    static constexpr int MAX_CURSOS = 6;

    std::string estudiante_codigo_;
    std::vector<std::string> cursos_;
    bool anulada_ = false;

    void verificarInvariante() const {
        assert(!estudiante_codigo_.empty() && "INV: código vacío");
        assert(cursos_.size() >= 1 && "INV: sin cursos");
        assert((int)cursos_.size() <= MAX_CURSOS && "INV: excede máximo");
        // Verificar ausencia de duplicados (O(n²) — aceptable para n <= 6)
        for (int i = 0; i < (int)cursos_.size(); ++i)
            for (int j = i + 1; j < (int)cursos_.size(); ++j)
                assert(cursos_[i] != cursos_[j] && "INV: cursos duplicados");
    }

    bool contiene(const std::string& curso) const {
        return std::find(cursos_.begin(), cursos_.end(), curso) != cursos_.end();
    }

public:
    Matricula(std::string codigoEst, std::vector<std::string> cursos) {
        // ── PRECONDICIONES ──────────────────────────────────────────────
        if (codigoEst.empty())
            throw ErrorValidacion("Código de estudiante vacío");
        if (cursos.empty() || (int)cursos.size() > MAX_CURSOS)
            throw ErrorCapacidad((int)cursos.size(), MAX_CURSOS, "matricula");
        for (std::size_t i = 0; i < cursos.size(); ++i)
            if (std::find(cursos.begin() + i + 1, cursos.end(), cursos[i]) != cursos.end())
                throw ErrorValidacion("Curso duplicado en la matrícula: " + cursos[i]);

        estudiante_codigo_ = std::move(codigoEst);
        cursos_ = std::move(cursos);
        verificarInvariante();   // POST-constructor
    }

    void agregarCurso(const std::string& curso) {
        // PRECONDICIONES
        if (anulada_)
            throw ErrorAcademico("Matrícula anulada — no se puede modificar");
        if ((int)cursos_.size() >= MAX_CURSOS)
            throw ErrorCapacidad((int)cursos_.size(), MAX_CURSOS, "matricula");
        if (contiene(curso))
            throw ErrorValidacion("Curso " + curso + " ya está en la matrícula");

        const std::size_t antes = cursos_.size();
        cursos_.push_back(curso);

        // POSCONDICIÓN
        assert(contiene(curso) && "POST: curso no agregado");
        assert(cursos_.size() == antes + 1 && "POST: tamaño incorrecto");
        (void)antes;
        // INVARIANTE
        verificarInvariante();
    }

    void anular() {
        if (anulada_)
            throw ErrorAcademico("Matrícula ya está anulada");
        anulada_ = true;
        // No se llama verificarInvariante — anular no rompe la invariante
    }

    std::string diagnostico() const {
        return std::string("Matrícula [") + (anulada_ ? "ANULADA" : "ACTIVA") + "] — "
               + std::to_string(cursos_.size()) + "/" + std::to_string(MAX_CURSOS)
               + " cursos";
    }

    // Getters
    bool anulada() const noexcept { return anulada_; }
    int numCursos() const noexcept { return (int)cursos_.size(); }
    const auto& cursos() const noexcept { return cursos_; }
};
