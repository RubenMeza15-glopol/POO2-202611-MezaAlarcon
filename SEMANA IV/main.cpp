
// Archivo: main.cpp
// Practica Semana 4 - Actividad 3
// Prueba del sistema de notificaciones.

#include "notificador.hpp" // Incluye las clases definidas en el encabezado.
#include <iostream> // Permite mostrar el resultado final.
#include <memory> // Permite utilizar std::make_unique.
#include <string> // Permite trabajar con cadenas de texto.

int main() { // Inicia la funcion principal.

    SistemaAlertas sistema; // Crea el sistema de alertas.

    sistema.agregar( // Agrega el canal de correo al sistema.
        std::make_unique<NotificadorEmail>("smtp.unap.edu.pe") // Crea un notificador Email.
    ); // Termina la llamada a agregar.

    sistema.agregar( // Agrega el canal SMS al sistema.
        std::make_unique<NotificadorSMS>("Movistar") // Crea un notificador SMS.
    ); // Termina la llamada a agregar.

    const std::string destinatario = "jmamani@unap.edu.pe"; // Define el destinatario.
    const std::string mensaje = // Declara el mensaje de alerta.
        "ALERTA: Temperatura del Lago Titicaca supera 18 grados"; // Asigna el contenido.

    int enviados = sistema.alertar(destinatario, mensaje); // Envia la alerta por los canales.

    std::cout << "Alerta enviada por " << enviados; // Muestra el total de envios.
    std::cout << " canal(es).\n"; // Completa el mensaje de salida.

    return 0; // Finaliza el programa indicando exito.
} // Termina main.
