
// =====================================================
// ACTIVIDAD 1: PATRON OBSERVER - C++17
// Sistema de notificaciones de estudiantes.
// =====================================================

// Incluye el servicio de estudiantes.
#include "servicio_estudiante.h"

// Permite utilizar punteros inteligentes.
#include <memory>

// Permite mostrar mensajes en la terminal.
#include <iostream>

// =====================================================
// FUNCION PRINCIPAL
// =====================================================

int main() {

    // Muestra el titulo de la actividad.
    std::cout << "====================================\n";
    std::cout << " SISTEMA OBSERVER - UNAP\n";
    std::cout << "====================================\n";

    // Crea el repositorio observable.
    RepositorioObservable repositorio;

    // Crea el observador Logger.
    auto logger = std::make_shared<LoggerObserver>();

    // Crea el observador Consola.
    auto consola = std::make_shared<ConsolaObserver>();

    // Suscribe el Logger al repositorio.
    repositorio.suscribir(logger);

    // Suscribe la Consola al repositorio.
    repositorio.suscribir(consola);

    // Crea el servicio de estudiantes.
    ServicioEstudiante servicio(repositorio);

    // Crea el primer estudiante.
    Estudiante estudiante1{
        1001, "Ana Quispe", 15.5, 3
    };

    // Crea el segundo estudiante.
    Estudiante estudiante2{
        1002, "Luis Mamani", 16.8, 4
    };

    // Registra al primer estudiante.
    servicio.registrar(estudiante1);

    // Registra al segundo estudiante.
    servicio.registrar(estudiante2);

    // Comprueba la búsqueda de un estudiante.
    servicio.consultar(1001);

    // Muestra la cantidad de estudiantes registrados.
    std::cout << "\nTotal de estudiantes registrados: "
              << repositorio.listar().size() << "\n";

    // Indica que el programa terminó correctamente.
    std::cout << "\nPRUEBA OBSERVER FINALIZADA\n";

    return 0;
}

