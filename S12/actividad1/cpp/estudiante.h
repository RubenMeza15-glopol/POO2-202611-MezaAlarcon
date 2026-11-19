
#pragma once

// Permite trabajar con cadenas de texto.
#include <string>

// Evita escribir std:: repetidamente.
using namespace std;

// Representa los datos de un estudiante.
struct Estudiante {

    // Código único del estudiante.
    int codigo;

    // Nombre completo del estudiante.
    string nombre;

    // Promedio ponderado acumulado.
    double ppa;

    // Ciclo académico.
    int ciclo;

    // Convierte los datos del estudiante en texto.
    string to_string() const {
        return "[" + std::to_string(codigo) + "] " +
               nombre + " - PPA: " +
               std::to_string(ppa);
    }
};
