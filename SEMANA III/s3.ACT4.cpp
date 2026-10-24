
#include <iostream>      // Permite imprimir datos por pantalla.
#include <string>        // Permite utilizar std::string.
#include <vector>        // Permite almacenar una lista de objetos.
#include <memory>        // Permite utilizar std::unique_ptr y std::make_unique.
#include <stdexcept>     // Permite lanzar excepciones de validación.
#include <iomanip>       // Permite mostrar importes con dos decimales.
#include <utility>       // Permite utilizar std::move.

using namespace std;     // Evita escribir std:: antes de cada elemento estándar.

// Clase base para todo el personal universitario.
class PersonalUniversitario {
protected:
    string dni_;         // Guarda el DNI del trabajador.
    string nombres_;     // Guarda sus nombres.
    string apellidos_;   // Guarda sus apellidos.

public:
    // Inicializa los atributos comunes del personal.
    PersonalUniversitario(string dni, string nombres, string apellidos)
        : dni_(move(dni)), nombres_(move(nombres)),
          apellidos_(move(apellidos)) {}

    // Destructor virtual para destruir correctamente objetos derivados.
    virtual ~PersonalUniversitario() = default;

    // Método virtual puro: cada subclase calcula su remuneración.
    virtual float calcularRemuneracion() const = 0;

    // Devuelve el nombre completo y el DNI del trabajador.
    virtual string identificarse() const {
        return apellidos_ + ", " + nombres_ + " (DNI: " + dni_ + ")";
    }
};

// Clase Docente que hereda públicamente del personal universitario.
class Docente : public PersonalUniversitario {
    int horas_;          // Guarda las horas de trabajo.
    float tarifa_ = 75.0f; // Define la tarifa base por hora.
    float factor_;       // Guarda el factor según la categoría.

    // Convierte la categoría en su factor de remuneración.
    static float resolverFactor(const string& categoria) {
        if (categoria == "Auxiliar") return 1.0f;  // Factor auxiliar.
        if (categoria == "Asociado") return 1.4f;  // Factor asociado.
        if (categoria == "Principal") return 1.8f; // Factor principal.
        throw invalid_argument("Categoría inválida: " + categoria);
    }

public:
    // Inicializa al docente y valida sus datos.
    Docente(string dni, string nombres, string apellidos,
            int horas, const string& categoria)
        : PersonalUniversitario(move(dni), move(nombres), move(apellidos)),
          horas_(horas), factor_(resolverFactor(categoria)) {
        if (horas_ < 1 || horas_ > 40) // Comprueba el rango de horas.
            throw invalid_argument("Las horas deben estar entre 1 y 40");
    }

    // Sobrescribe el método de remuneración de la clase base.
    float calcularRemuneracion() const override {
        return horas_ * tarifa_ * factor_; // Calcula el pago docente.
    }
};

// Clase Administrativo que hereda del personal universitario.
class Administrativo : public PersonalUniversitario {
    float salarioBase_;  // Guarda el salario base.
    float bono_;         // Guarda el bono adicional.

public:
    // Inicializa al administrativo y valida el salario y el bono.
    Administrativo(string dni, string nombres, string apellidos,
                   float salarioBase, float bono = 0.0f)
        : PersonalUniversitario(move(dni), move(nombres), move(apellidos)),
          salarioBase_(salarioBase), bono_(bono) {
        if (salarioBase_ <= 0) // El salario debe ser positivo.
            throw invalid_argument("El salario base debe ser positivo");
        if (bono_ < 0) // El bono no puede ser negativo.
            throw invalid_argument("El bono no puede ser negativo");
    }

    // Sobrescribe el cálculo de remuneración del administrativo.
    float calcularRemuneracion() const override {
        return salarioBase_ + bono_; // Suma salario y bono.
    }
};

// Imprime la planilla usando una lista polimórfica de personal.
void planilla(const vector<unique_ptr<PersonalUniversitario>>& personal) {
    float total = 0.0f; // Inicializa el acumulador de remuneraciones.

    cout << string(60, '=') << '\n'; // Imprime el encabezado.
    cout << "PLANILLA PERSONAL UNIVERSITARIO - UNAP PUNO\n";
    cout << string(60, '=') << '\n';

    // Recorre todos los trabajadores sin importar su subclase.
    for (const auto& persona : personal) {
        // Llama a los métodos correspondientes al tipo real del objeto.
        cout << fixed << setprecision(2)
             << persona->identificarse()
             << " S/ " << persona->calcularRemuneracion() << '\n';

        // Acumula la remuneración del trabajador actual.
        total += persona->calcularRemuneracion();
    }

    cout << string(60, '-') << '\n'; // Separa el total de la lista.
    cout << "TOTAL: S/ " << total << '\n'; // Muestra el total general.
}

// Función principal del programa.
int main() {
    // Creamos una lista de punteros inteligentes a la clase base.
    vector<unique_ptr<PersonalUniversitario>> personal;

    // Agregamos un docente asociado con 16 horas.
    personal.push_back(make_unique<Docente>(
        "12345678", "Juan Carlos", "Mamani Quispe", 16, "Asociado"));

    // Agregamos un administrativo con salario y bono.
    personal.push_back(make_unique<Administrativo>(
        "34567890", "Pedro", "Huanca Lazo", 2800.0f, 350.0f));

    // Generamos e imprimimos la planilla polimórfica.
    planilla(personal);

    return 0; // Finaliza el programa correctamente.
}
