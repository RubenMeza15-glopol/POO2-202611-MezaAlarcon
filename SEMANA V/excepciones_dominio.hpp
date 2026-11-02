// ── excepciones_dominio.hpp — Actividad 1, Parte A ─────────────────────
#pragma once
#include <algorithm>
#include <string>
#include <vector>

#include "errores_academicos.hpp"

class ErrorMatriculaDuplicada : public ErrorValidacion {
    std::string codigo_estudiante_;

public:
    explicit ErrorMatriculaDuplicada(const std::string& codigo)
        : ErrorValidacion("Estudiante " + codigo + " ya está matriculado"),
          codigo_estudiante_(codigo) {}

    const std::string& codigo_estudiante() const noexcept { return codigo_estudiante_; }
};

inline void validar_matricula(int codigo, std::vector<int>& matriculados) {
    if (std::find(matriculados.begin(), matriculados.end(), codigo) != matriculados.end())
        throw ErrorMatriculaDuplicada(std::to_string(codigo));
    matriculados.push_back(codigo);
}

inline void registrar_nota(float cal) {
    if (cal < 0.0f || cal > 20.0f)
        throw ErrorCalificacion(cal);   // lanza excepción de dominio
}
