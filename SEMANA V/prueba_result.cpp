
#include "result.hpp" // Incluye la implementación de Result.
#include <iostream>   // Permite mostrar los resultados.
#include <string>     // Permite usar cadenas.

// Función principal de la prueba independiente.
int main() {
    // Crea un resultado exitoso con una cadena.
    Result<std::string> correcto = Result<std::string>::ok("Estudiante encontrado");

    // Comprueba si la operación fue exitosa.
    if (correcto.esExito()) {
        // Muestra el valor almacenado.
        std::cout << "[EXITO] " << correcto.valor() << '\n';
    }

    // Crea un resultado fallido sin lanzar una excepción de búsqueda.
    Result<std::string> fallido =
        Result<std::string>::fallo("Estudiante no encontrado: 9999");

    // Comprueba si la operación falló.
    if (!fallido.esExito()) {
        // Muestra el mensaje de error.
        std::cout << "[ERROR] " << fallido.error() << '\n';
    }

    // Finaliza la prueba correctamente.
    return 0;
}
