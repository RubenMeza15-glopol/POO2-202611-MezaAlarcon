
#include <iostream>   // Permite mostrar resultados en pantalla.
#include <string>     // Permite trabajar con textos.
#include <vector>     // Permite almacenar varios objetos.
#include <memory>     // Permite usar unique_ptr y make_unique.

using namespace std;  // Simplifica el uso de elementos de la biblioteca estándar.

// Definimos la clase base de las personas académicas.
class PersonaAcademica {
protected:
    string nombre_;   // Guarda el nombre de la persona.

public:
    // Inicializamos el nombre de la persona.
    PersonaAcademica(string nombre) : nombre_(nombre) {}

    // Declaramos un destructor virtual para la herencia polimórfica.
    virtual ~PersonaAcademica() = default;

    // Declaramos un método virtual puro que implementan las subclases.
    virtual string mostrarRol() const = 0;
};

// Definimos Estudiante como subclase de PersonaAcademica.
class Estudiante : public PersonaAcademica {
public:
    // Reutilizamos el constructor de la clase base.
    Estudiante(string nombre) : PersonaAcademica(nombre) {}

    // Sobrescribimos el método para indicar el rol del estudiante.
    string mostrarRol() const override {
        return nombre_ + " es estudiante y lleva cursos.";
    }
};

// Definimos Docente como subclase de PersonaAcademica.
class Docente : public PersonaAcademica {
public:
    // Reutilizamos el constructor de la clase base.
    Docente(string nombre) : PersonaAcademica(nombre) {}

    // Sobrescribimos el método para indicar el rol del docente.
    string mostrarRol() const override {
        return nombre_ + " es docente y dicta cursos.";
    }
};

// Mostramos una lista con distintos tipos de personas académicas.
void mostrarPersonas(
    const vector<unique_ptr<PersonaAcademica>>& personas) {

    // Recorremos los objetos usando referencias a la clase base.
    for (const auto& persona : personas) {
        // Se ejecuta el método de la subclase correspondiente.
        cout << persona->mostrarRol() << '\n';
    }
}

// Función principal del programa.
int main() {
    // Creamos una lista polimórfica de personas académicas.
    vector<unique_ptr<PersonaAcademica>> personas;

    // Agregamos un estudiante a la lista.
    personas.push_back(make_unique<Estudiante>("Juan"));

    // Agregamos un docente a la misma lista.
    personas.push_back(make_unique<Docente>("Maria"));

    // Mostramos los roles usando polimorfismo dinámico.
    mostrarPersonas(personas);

    // Finalizamos correctamente el programa.
    return 0;
}
