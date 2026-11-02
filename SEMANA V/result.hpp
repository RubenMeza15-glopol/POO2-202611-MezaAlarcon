
#ifndef RESULT_HPP
#define RESULT_HPP

#include <string>  // Permite guardar mensajes de error.
#include <utility> // Permite mover valores.
#include <variant> // Permite representar éxito o fallo.

// Representa el resultado de una operación: un valor o un error.
template <typename T>
class Result {
private:
    // El resultado almacena un valor T o un mensaje de error.
    std::variant<T, std::string> resultado_;

    // Construye el resultado a partir del valor o mensaje recibido.
    explicit Result(std::variant<T, std::string> resultado)
        : resultado_(std::move(resultado)) {}

public:
    // Crea un resultado exitoso.
    static Result ok(T valor) {
        // Guarda el valor como primera alternativa del variant.
        return Result(std::variant<T, std::string>(
            std::in_place_index<0>, std::move(valor)));
    }

    // Crea un resultado fallido.
    static Result fallo(std::string mensaje) {
        // Guarda el mensaje como segunda alternativa del variant.
        return Result(std::variant<T, std::string>(
            std::in_place_index<1>, std::move(mensaje)));
    }

    // Indica si el resultado contiene un valor válido.
    bool esExito() const noexcept {
        // La alternativa cero corresponde al valor T.
        return std::holds_alternative<T>(resultado_);
    }

    // Devuelve el valor cuando el resultado es exitoso.
    const T& valor() const {
        // Accede a la alternativa T.
        return std::get<T>(resultado_);
    }

    // Devuelve el mensaje cuando el resultado es fallido.
    const std::string& error() const {
        // Accede a la alternativa que contiene el mensaje.
        return std::get<std::string>(resultado_);
    }

    // Aplica una función al valor solo si existe éxito.
    template <typename F>
    auto map(F funcion) const
        -> Result<decltype(funcion(std::declval<const T&>()))> {
        // Determina el tipo que devuelve la función.
        using U = decltype(funcion(std::declval<const T&>()));

        // Si hay error, propaga el mensaje sin ejecutar la función.
        if (!esExito()) {
            return Result<U>::fallo(error());
        }

        // Ejecuta la función únicamente cuando existe un valor.
        return Result<U>::ok(funcion(valor()));
    }
};

#endif // RESULT_HPP
