
#pragma once

// Incluye el repositorio observable y sus observadores.
#include "observer.h"

// Permite utilizar mensajes en la terminal.
#include <iostream>

// =====================================================
// SERVICIO DE ESTUDIANTES
// =====================================================

// Coordina el registro y la búsqueda de estudiantes.
class ServicioEstudiante {

private:

    // Referencia al repositorio que almacena los estudiantes.
    RepositorioObservable& repositorio_;

public:

    // Recibe el repositorio al construir el servicio.
    explicit ServicioEstudiante(RepositorioObservable& repo)
        : repositorio_(repo) {
    }

    // Registra un estudiante mediante el repositorio.
    void registrar(const Estudiante& estudiante) {

        std::cout << "\nRegistrando estudiante...\n";

        // Guarda el estudiante y activa las notificaciones.
        repositorio_.guardar(estudiante);
    }

    // Busca un estudiante por su código.
    void consultar(int codigo) const {

        try {

            // Recupera el estudiante del repositorio.
            Estudiante e = repositorio_.buscar(codigo);

            // Muestra el resultado de la consulta.
            std::cout << "\nEstudiante encontrado: "
                      << e.to_string() << "\n";

        } catch (const std::exception& error) {

            // Informa si no se encontró el estudiante.
            std::cout << "Error: " << error.what() << "\n";
        }
    }
};
