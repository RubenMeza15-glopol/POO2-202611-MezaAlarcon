    
#pragma once  // Evita que el archivo se incluya varias veces.

#include <string>      // Permite utilizar cadenas de texto.
#include <stdexcept>   // Permite generar excepciones.
#include <vector>      // Permite almacenar varias notas.
#include <numeric>     // Permite calcular la suma de notas.
#include <optional>    // Permite representar un promedio inexistente.

// Clase Estudiante: representa a un estudiante del sistema académico UNAP.
class Estudiante {
public:

    // Constructor: recibe los datos iniciales del estudiante.
    Estudiante(int codigo, std::string nombre, float ppa, int ciclo)
        : codigo_(codigo),
          nombre_(std::move(nombre)),
          ppa_(ppa),
          ciclo_(ciclo) {

        // Validamos que el código sea positivo.
        if (codigo_ <= 0)
            throw std::invalid_argument("Codigo debe ser positivo");

        // Validamos que el nombre no esté vacío.
        if (nombre_.empty())
            throw std::invalid_argument("Nombre no puede estar vacio");

        // Validamos que el PPA esté entre 0 y 20.
        if (ppa_ < 0.0f || ppa_ > 20.0f)
            throw std::out_of_range("PPA debe estar entre 0 y 20");
    }

    // Getters: permiten consultar los atributos sin modificarlos.
    [[nodiscard]] int codigo() const { return codigo_; }
    [[nodiscard]] std::string nombre() const { return nombre_; }
    [[nodiscard]] float ppa() const { return ppa_; }
    [[nodiscard]] int ciclo() const { return ciclo_; }

    // Agrega una nota al registro del estudiante.
    void agregar_nota(float nota) {
        // Comprobamos que la nota esté entre 0 y 20.
        if (nota < 0.0f || nota > 20.0f)
            throw std::out_of_range("Nota fuera de rango");

        // Guardamos la nota en el vector.
        notas_.push_back(nota);
    }

    // Calcula el promedio de las notas registradas.
    // Si no existen notas, devuelve nullopt.
    [[nodiscard]] std::optional<float> calcular_promedio() const {
        if (notas_.empty())
            return std::nullopt;

        // Sumamos todas las notas.
        float suma = std::accumulate(
            notas_.begin(), notas_.end(), 0.0f
        );

        // Dividimos la suma entre la cantidad de notas.
        return suma / static_cast<float>(notas_.size());
    }

    // Devuelve true si el PPA es igual o superior a 11.
    [[nodiscard]] bool es_aprobado() const {
        return ppa_ >= 11.0f;
    }

    // Convierte los datos del estudiante en una cadena de texto.
    [[nodiscard]] std::string to_string() const {
        return "[" + std::to_string(codigo_) + "] " + nombre_
               + " - PPA: " + std::to_string(ppa_)
               + " - Ciclo: " + std::to_string(ciclo_);
    }

private:
    // Atributos privados: protegen los datos del estudiante.
    int codigo_;
    std::string nombre_;
    float ppa_;
    int ciclo_;

    // Vector que almacena las notas del estudiante.
    std::vector<float> notas_;
};
