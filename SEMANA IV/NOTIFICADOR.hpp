
// Archivo: notificador.hpp
// Practica Semana 4 - Actividad 3
// Sistema de notificaciones mediante interfaces y composicion

#pragma once // Evita incluir este archivo mas de una vez.

#include <string> // Permite utilizar std::string.
#include <vector> // Permite almacenar varios notificadores.
#include <memory> // Permite utilizar std::unique_ptr y std::make_unique.
#include <stdexcept> // Permite lanzar excepciones como std::invalid_argument.
#include <iostream> // Permite mostrar mensajes en consola.
#include <utility> // Permite utilizar std::move.


// ------------------------------------------------------------
// 1. INTERFAZ ABSTRACTA: INOTIFICADOR
// ------------------------------------------------------------

class INotificador { // Define el contrato comun de los notificadores.
public: // Inicia la seccion publica de la clase.

    virtual ~INotificador() = default; // Permite destruir objetos derivados correctamente.

    virtual bool enviar( // Declara el metodo de envio como virtual.
        const std::string& destinatario, // Recibe el destinatario por referencia constante.
        const std::string& mensaje // Recibe el mensaje por referencia constante.
    ) = 0; // Lo convierte en metodo virtual puro.

    virtual bool esDisponible() const = 0; // Exige comprobar la disponibilidad del canal.

    virtual std::string nombre() const = 0; // Exige devolver el nombre del notificador.
}; // Termina la interfaz abstracta.


// ------------------------------------------------------------
// 2. IMPLEMENTACION CONCRETA: NOTIFICADOREMAIL
// ------------------------------------------------------------

class NotificadorEmail : public INotificador { // Email implementa la interfaz.
private: // Inicia los atributos privados.

    std::string servidor_; // Guarda el servidor de correo.
    bool activo_ = true; // Indica si el servicio esta activo.

public: // Inicia los metodos publicos.

    explicit NotificadorEmail(std::string servidor) // Recibe el servidor al crear el objeto.
        : servidor_(std::move(servidor)) {} // Guarda el servidor evitando una copia innecesaria.

    bool esDisponible() const override { // Implementa la consulta de disponibilidad.
        return activo_; // Devuelve el estado actual del servicio.
    } // Termina esDisponible.

    std::string nombre() const override { // Implementa el nombre del notificador.
        return "Email (" + servidor_ + ")"; // Devuelve el nombre y el servidor.
    } // Termina nombre.

    bool enviar( // Implementa el envio simulado de un correo.
        const std::string& destinatario, // Recibe el destinatario.
        const std::string& mensaje // Recibe el contenido del correo.
    ) override { // Confirma que sobrescribe el metodo de la interfaz.

        std::cout << "[EMAIL -> " << destinatario << "]: "; // Muestra el destinatario.
        std::cout << mensaje.substr(0, 50) << "...\n"; // Muestra hasta 50 caracteres.

        return true; // Indica que la simulacion del envio tuvo exito.
    } // Termina enviar.
}; // Termina NotificadorEmail.


// ------------------------------------------------------------
// 3. IMPLEMENTACION CONCRETA: NOTIFICADORSMS
// ------------------------------------------------------------

class NotificadorSMS : public INotificador { // SMS implementa la misma interfaz.
private: // Inicia los atributos privados.

    std::string proveedor_; // Guarda el proveedor del servicio SMS.
    bool activo_ = true; // Indica si el servicio esta activo.
    static constexpr std::size_t MAX_CHARS = 160; // Define el limite del mensaje.

public: // Inicia los metodos publicos.

    explicit NotificadorSMS(std::string proveedor) // Recibe el proveedor al crear el objeto.
        : proveedor_(std::move(proveedor)) {} // Guarda el proveedor.

    bool esDisponible() const override { // Implementa la consulta de disponibilidad.
        return activo_; // Devuelve el estado del servicio.
    } // Termina esDisponible.

    std::string nombre() const override { // Implementa el nombre del notificador.
        return "SMS (" + proveedor_ + ")"; // Devuelve el nombre y proveedor.
    } // Termina nombre.

    bool enviar( // Implementa el envio simulado de un SMS.
        const std::string& destinatario, // Recibe el destinatario.
        const std::string& mensaje // Recibe el contenido del SMS.
    ) override { // Confirma que sobrescribe el metodo virtual.

        if (mensaje.size() > MAX_CHARS) { // Comprueba si se supera el limite.
            throw std::invalid_argument( // Lanza un error si el mensaje es demasiado largo.
                "SMS excede 160 caracteres" // Describe el motivo del error.
            ); // Termina la excepcion.
        } // Termina la comprobacion de longitud.

        std::cout << "[SMS -> " << destinatario << "]: "; // Muestra el destinatario.
        std::cout << mensaje << '\n'; // Muestra el mensaje SMS.

        return true; // Indica que la simulacion del envio tuvo exito.
    } // Termina enviar.
}; // Termina NotificadorSMS.


// ------------------------------------------------------------
// 4. SISTEMA DE ALERTAS: COMPOSICION
// ------------------------------------------------------------

class SistemaAlertas { // Coordina los distintos canales de notificacion.
private: // Inicia los atributos privados.

    std::vector<std::unique_ptr<INotificador>> notificadores_; // Posee los notificadores.

public: // Inicia los metodos publicos.

    void agregar(std::unique_ptr<INotificador> notificador) { // Recibe la propiedad del objeto.
        notificadores_.push_back(std::move(notificador)); // Guarda el notificador en el vector.
    } // Termina agregar.

    int alertar( // Envia una alerta a todos los canales disponibles.
        const std::string& destinatario, // Recibe el destinatario de la alerta.
        const std::string& mensaje // Recibe el contenido de la alerta.
    ) const { // Indica que el metodo no modifica el estado del sistema.

        int enviados = 0; // Inicializa el contador de envios exitosos.

        for (const auto& notificador : notificadores_) { // Recorre todos los notificadores.

            if (!notificador->esDisponible()) { // Comprueba si el canal esta inactivo.
                continue; // Salta al siguiente canal cuando no esta disponible.
            } // Termina la comprobacion de disponibilidad.

            try { // Inicia el bloque que puede generar excepciones.

                if (notificador->enviar(destinatario, mensaje)) { // Envia usando polimorfismo.
                    ++enviados; // Cuenta el envio si devuelve true.
                } // Termina la comprobacion del resultado.

            } catch (const std::exception& error) { // Captura errores de envio.

                std::cerr << "Error en " << notificador->nombre(); // Identifica el canal.
                std::cerr << ": " << error.what() << '\n'; // Muestra el motivo del error.

            } // Termina el manejo de excepciones.
        } // Termina el recorrido de los notificadores.

        return enviados; // Devuelve la cantidad de envios exitosos.
    } // Termina alertar.
}; // Termina SistemaAlertas.
