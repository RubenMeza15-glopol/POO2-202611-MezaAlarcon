#include <stdexcept>
#pragma once

// Incluye la definición de Estudiante.
#include "estudiante.h"

// Permite utilizar vectores para almacenar observadores.
#include <vector>

// Permite utilizar punteros inteligentes.
#include <memory>

// Permite mostrar mensajes en la consola.
#include <iostream>

// =====================================================
// 1. INTERFAZ DEL OBSERVADOR
// =====================================================

// Define el contrato que deben cumplir los observadores.
struct IObserverEstudiante {

    // Método que se ejecuta cuando se guarda un estudiante.
    virtual void on_guardado(const Estudiante& e) = 0;

    // Destructor virtual para permitir una destrucción correcta.
    virtual ~IObserverEstudiante() = default;
};

// =====================================================
// 2. OBSERVADOR LOGGER
// =====================================================

// Recibe notificaciones y registra el estudiante en el Logger.
struct LoggerObserver : IObserverEstudiante {

    // Implementa el método de notificación.
    void on_guardado(const Estudiante& e) override {

        // Registra los datos del estudiante.
        std::cout << "[LOGGER] Guardado: "
                  << e.to_string() << std::endl;
    }
};

// =====================================================
// 3. OBSERVADOR DE CONSOLA
// =====================================================

// Muestra directamente los datos del estudiante.
struct ConsolaObserver : IObserverEstudiante {

    // Implementa el método de notificación.
    void on_guardado(const Estudiante& e) override {

        // Muestra la información recibida.
        std::cout << "[VISTA] " << e.to_string()
                  << std::endl;
    }
};

// =====================================================
// 4. REPOSITORIO OBSERVABLE
// =====================================================

// Administra los estudiantes y notifica a los observadores.
class RepositorioObservable {

private:

    // Guarda los estudiantes.
    std::vector<Estudiante> estudiantes_;

    // Almacena los observadores registrados.
    std::vector<std::shared_ptr<IObserverEstudiante>> observadores_;

public:

    // Registra un nuevo observador.
    void suscribir(
        std::shared_ptr<IObserverEstudiante> observador
    ) {

        // Agrega el observador a la lista.
        observadores_.push_back(observador);
    }

    // Guarda un estudiante y notifica a los observadores.
    void guardar(const Estudiante& e) {

        // Almacena el estudiante.
        estudiantes_.push_back(e);

        // Notifica a todos los observadores registrados.
        for (const auto& observador : observadores_) {

            // Envía los datos del estudiante.
            observador->on_guardado(e);
        }
    }

    // Busca un estudiante por su código.
    Estudiante buscar(int codigo) const {

        // Recorre la lista de estudiantes.
        for (const auto& e : estudiantes_) {

            // Comprueba si coincide el código.
            if (e.codigo == codigo) {
                return e;
            }
        }

        // Indica que no se encontró el estudiante.
        throw std::runtime_error("Estudiante no encontrado");
    }

    // Devuelve todos los estudiantes registrados.
    const std::vector<Estudiante>& listar() const {

        return estudiantes_;
    }
};
