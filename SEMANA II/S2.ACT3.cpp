
#include <iostream>   // Permite mostrar mensajes en pantalla.
#include <string>     // Permite utilizar string.
#include <regex>      // Permite validar el código.
#include <stdexcept>  // Permite lanzar excepciones.
#include <utility>    // Permite utilizar std::move.

using namespace std;

// Clase Curso con encapsulamiento estricto.
class Curso {
private:
    string codigo_;       // Código privado del curso.
    string nombre_;       // Nombre privado del curso.
    int creditos_;        // Créditos del curso.
    int cuposMaximo_;     // Máximo de estudiantes.
    int inscritos_ = 0;   // Inicia con cero inscritos.

public:
    // Constructor que inicializa y valida los atributos.
    Curso(string codigo, string nombre, int creditos, int cuposMaximo)
        : nombre_(move(nombre)) {
        setCodigo(codigo);           // Valida el código.
        setCreditos(creditos);       // Valida los créditos.
        setCuposMaximo(cuposMaximo); // Valida los cupos.
    }

    // Setter: valida el formato del código.
    void setCodigo(const string& cod) {
        regex patron("[A-Z]{2,4}[0-9]{3}");

        if (!regex_match(cod, patron))
            throw invalid_argument("Codigo invalido");

        codigo_ = cod; // Guarda el código válido.
    }

    // Setter: permite créditos entre 1 y 6.
    void setCreditos(int c) {
        if (c < 1 || c > 6)
            throw invalid_argument("Creditos fuera de rango [1,6]");

        creditos_ = c;
    }

    // Setter: permite entre 1 y 50 cupos.
    void setCuposMaximo(int q) {
        if (q < 1 || q > 50)
            throw invalid_argument("Cupos fuera de rango [1,50]");

        cuposMaximo_ = q;
    }

    // Getter constante: devuelve el código.
    string getCodigo() const {
        return codigo_;
    }

    // Getter constante: devuelve el nombre.
    string getNombre() const {
        return nombre_;
    }

    // Getter constante: devuelve los créditos.
    int getCreditos() const {
        return creditos_;
    }

    // Getter constante: devuelve los cupos máximos.
    int getCuposMaximo() const {
        return cuposMaximo_;
    }

    // Getter constante: devuelve los inscritos.
    int getInscritos() const {
        return inscritos_;
    }

    // Calcula los cupos disponibles.
    int cuposDisponibles() const {
        return cuposMaximo_ - inscritos_;
    }

    // Comprueba si el curso está lleno.
    bool estaLleno() const {
        return inscritos_ == cuposMaximo_;
    }

    // Inscribe un estudiante si hay cupos.
    void inscribirEstudiante() {
        if (estaLleno())
            throw invalid_argument("Curso sin cupos disponibles");

        ++inscritos_; // Aumenta el número de inscritos.
    }
};

// Programa principal.
int main() {
    try {
        // Crea un curso con código, nombre, créditos y cupos.
        Curso c("SIS206", "POO II", 4, 30);

        c.inscribirEstudiante(); // Inscribe un estudiante.

        // Muestra la información del curso.
        cout << "Codigo: " << c.getCodigo() << '\n';
        cout << "Nombre: " << c.getNombre() << '\n';
        cout << "Creditos: " << c.getCreditos() << '\n';
        cout << "Cupos maximos: " << c.getCuposMaximo() << '\n';
        cout << "Inscritos: " << c.getInscritos() << '\n';
        cout << "Cupos disponibles: " << c.cuposDisponibles() << '\n';
        cout << "Esta lleno: " << (c.estaLleno() ? "Si" : "No") << '\n';

    } catch (const invalid_argument& e) {
        // Captura y muestra errores de validación.
        cout << "Error: " << e.what() << '\n';
    }

    return 0; // Finaliza el programa.
}
