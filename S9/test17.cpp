
// ============================================================
// ACTIVIDAD 1.1: VERIFICACIÓN DEL ENTORNO C++17
// Pregunta: ¿El compilador reconoce y ejecuta características
// propias del estándar C++17?
// ============================================================

// Incluimos la biblioteca para mostrar información en pantalla.
#include <iostream>

// Incluimos optional para almacenar un valor que puede existir
// o no existir. Esta característica está disponible desde C++17.
#include <optional>

// Incluimos string para trabajar con cadenas de texto.
#include <string>

// Incluimos string_view para crear una vista de una cadena
// sin copiar su contenido. Está disponible desde C++17.
#include <string_view>

// Función principal donde comienza la ejecución del programa.
int main() {

    // Creamos una variable optional que almacena el nombre UNAP.
    std::optional<std::string> nombre = "UNAP";

    // Creamos una vista de la cadena almacenada en nombre.
    // value() obtiene el contenido del optional.
    std::string_view vista = nombre.value();

    // Mostramos el resultado de la prueba en la terminal.
    std::cout << "C++17 OK: " << vista << std::endl;

    // Devolvemos cero para indicar que el programa terminó bien.
    return 0;
}
