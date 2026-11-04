
#include "estudiante.h"  // Incluye nuestra clase Estudiante.
#include <iostream>      // Permite mostrar resultados en pantalla.
#include <iomanip>       // Permite controlar los decimales.

// Función principal del programa.
int main() {

    // Creamos un estudiante con datos de ejemplo.
    Estudiante e{1001, "Ana Quispe", 15.5f, 3};

    // Registramos tres notas del semestre.
    e.agregar_nota(14.0f);
    e.agregar_nota(16.0f);
    e.agregar_nota(18.0f);

    // Mostramos los datos generales del estudiante.
    std::cout << e.to_string() << std::endl;

    // Configuramos la salida para mostrar dos decimales.
    std::cout << std::fixed << std::setprecision(2);

    // Calculamos y mostramos el promedio inicial.
    if (auto prom = e.calcular_promedio(); prom.has_value()) {
        std::cout << "Promedio inicial: " << prom.value() << std::endl;
    }

    // Agregamos la nota adicional solicitada por la guía.
    e.agregar_nota(20.0f);

    // Calculamos nuevamente el promedio.
    if (auto prom = e.calcular_promedio(); prom.has_value()) {
        std::cout << "Promedio con nota 20.0: "
                  << prom.value() << std::endl;
    }

    // Comprobamos si el estudiante está aprobado.
    std::cout << "Estado academico: "
              << (e.es_aprobado() ? "APROBADO" : "DESAPROBADO")
              << std::endl;

    // Probamos la validación con un código incorrecto.
    try {
        Estudiante invalido{-1, "X", 5.0f, 1};
    }
    catch (const std::invalid_argument& ex) {
        std::cout << "Error esperado: " << ex.what() << std::endl;
    }

    // Finalizamos correctamente el programa.
    return 0;
}
