
/*
===============================================================
CURSO: PROGRAMACION ORIENTADA A OBJETOS II - POO II
UNIDAD: SEGUNDA UNIDAD
SEMANA: 10
ACTIVIDAD 1.2: REFACTORIZACION SRP EN C++17

PREGUNTA DEL INGENIERO:
Separar los datos del estudiante de las responsabilidades
de cálculo, almacenamiento y gestión del sistema.

RESOLUCION:
Crear la clase Estudiante, cuya única responsabilidad será
representar y almacenar los datos del estudiante.
===============================================================
*/

// Incluye las herramientas para trabajar con cadenas de texto.
#include <string>

// Incluye las herramientas para mostrar información en pantalla.
#include <iostream>

// =============================================================
// CLASE: Estudiante
// RESPONSABILIDAD: almacenar los datos del estudiante.
// =============================================================

class Estudiante {

public:

    // Constructor que recibe el código, nombre y promedio.
    Estudiante(int cod, std::string nom, float ppa)
        : codigo_(cod), nombre_(nom), ppa_(ppa) {
    }

    // Devuelve el código del estudiante sin modificarlo.
    int codigo() const {
        return codigo_;
    }

    // Devuelve el nombre del estudiante sin modificarlo.
    std::string nombre() const {
        return nombre_;
    }

    // Devuelve el promedio académico sin modificarlo.
    float promedio() const {
        return ppa_;
    }

    // Permite actualizar el promedio académico.
    void set_ppa(float valor) {
        ppa_ = valor;
    }

private:

    // Almacena el código único del estudiante.
    int codigo_;

    // Almacena el nombre completo del estudiante.
    std::string nombre_;

    // Almacena el promedio ponderado académico.
    float ppa_;
};

// =============================================================
// PROGRAMA PRINCIPAL: prueba de la clase Estudiante.
// =============================================================

int main() {

    // Creamos un estudiante con código, nombre y promedio.
    Estudiante estudiante(1001, "Ruben Meza", 16.0f);
    //Estudiante estudiante(1418,"Ruben Meza", 18.0f);

    // Mostramos el código del estudiante.
    std::cout << "Codigo: " << estudiante.codigo() << '\n';

    // Mostramos el nombre del estudiante.
    std::cout << "Nombre: " << estudiante.nombre() << '\n';

    // Mostramos el promedio académico.
    std::cout << "PPA: " << estudiante.promedio() << '\n';

    // Indicamos que el programa terminó correctamente.
    return 0;
}
