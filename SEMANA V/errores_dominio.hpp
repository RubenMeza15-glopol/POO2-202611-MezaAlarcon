
#ifndef ERRORES_DOMINIO_HPP
#define ERRORES_DOMINIO_HPP

#include <stdexcept> // Proporciona std::runtime_error.
#include <string>    // Permite trabajar con std::string.

// Excepción base para los errores del dominio académico.
class ErrorAcademico : public std::runtime_error {
public:
    // Inicializa el mensaje de la excepción base.
    explicit ErrorAcademico(const std::string& mensaje)
        : std::runtime_error(mensaje) {}
};

// Excepción para datos que incumplen las reglas de validación.
class ErrorValidacion : public ErrorAcademico {
public:
    // Reutiliza el mensaje de ErrorAcademico.
    explicit ErrorValidacion(const std::string& mensaje)
        : ErrorAcademico(mensaje) {}
};

// Excepción para capacidades que superan los límites permitidos.
class ErrorCapacidad : public ErrorValidacion {
public:
    // Construye un mensaje con la cantidad y el límite permitido.
    ErrorCapacidad(int cantidad, int maximo, const std::string& recurso)
        : ErrorValidacion(
            "Capacidad excedida en " + recurso + ": " +
            std::to_string(cantidad) + " solicitados; máximo " +
            std::to_string(maximo)) {}
};

// Excepción para códigos o registros duplicados.
class ErrorDuplicado : public ErrorValidacion {
public:
    // Inicializa la excepción con el mensaje descriptivo.
    explicit ErrorDuplicado(const std::string& mensaje)
        : ErrorValidacion(mensaje) {}
};

// Excepción para recursos o registros inexistentes.
class ErrorNoEncontrado : public ErrorAcademico {
public:
    // Inicializa la excepción con el mensaje descriptivo.
    explicit ErrorNoEncontrado(const std::string& mensaje)
        : ErrorAcademico(mensaje) {}
};

// Excepción para operaciones incompatibles con el estado del objeto.
class ErrorEstado : public ErrorAcademico {
public:
    // Inicializa la excepción con el mensaje descriptivo.
    explicit ErrorEstado(const std::string& mensaje)
        : ErrorAcademico(mensaje) {}
};

#endif // ERRORES_DOMINIO_HPP
