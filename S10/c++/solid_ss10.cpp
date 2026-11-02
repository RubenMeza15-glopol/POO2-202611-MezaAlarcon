
/*
================================================================
CURSO: PROGRAMACIÓN ORIENTADA A OBJETOS II - POO II
UNIDAD: SEGUNDA UNIDAD
SEMANA: 10
ACTIVIDAD 1A: IDENTIFICAR Y REFACTORIZAR ESTUDIANTE GOD
PRINCIPIO: SRP - PRINCIPIO DE RESPONSABILIDAD ÚNICA

PREGUNTA DEL INGENIERO:
La siguiente clase viola el SRP porque tiene al menos cuatro
razones para cambiar. Identifica sus responsabilidades antes
de realizar la refactorización.

¿QUÉ NOS PIDE REALIZAR?
1. Identificar las cuatro responsabilidades de EstudianteGod.
2. Separar los datos del estudiante de las demás tareas.
3. Crear una estrategia independiente para calcular el PPA.
4. Crear un repositorio para guardar los datos.
5. Crear un servicio que coordine el cálculo y almacenamiento.
6. Ejecutar y verificar que el PPA se calcule correctamente.

RESOLUCIÓN:
Separamos las responsabilidades en clases independientes:
- Estudiante: almacena los datos.
- PromedioSimple: calcula el promedio.
- RepositorioArchivo: guarda los datos en CSV.
- ServicioEstudiante: coordina las operaciones.

NOTA:
La serialización JSON y el envío de correo se identifican
en la clase original, pero no se implementan en esta versión.
================================================================
*/

// Incluimos iostream para mostrar mensajes en la terminal.
#include <iostream>

// Incluimos string para trabajar con nombres de estudiantes.
#include <string>

// Incluimos vector para almacenar las notas académicas.
#include <vector>

// Incluimos fstream para escribir información en archivos.
#include <fstream>


// ================================================================
// 1. CLASE ESTUDIANTE
// RESPONSABILIDAD: almacenar únicamente los datos del estudiante.
// ================================================================

class Estudiante {

private:

    // Guarda el código único que identifica al estudiante.
    int codigo_;

    // Guarda el nombre completo del estudiante.
    std::string nombre_;

    // Guarda el promedio ponderado académico.
    float ppa_;

public:

    // Constructor: inicializa los datos del estudiante.
    Estudiante(int codigo, std::string nombre, float ppa = 0.0f)
        : codigo_(codigo), nombre_(nombre), ppa_(ppa) {
    }

    // Devuelve el código del estudiante.
    int codigo() const {
        return codigo_;
    }

    // Devuelve el nombre del estudiante.
    std::string nombre() const {
        return nombre_;
    }

    // Devuelve el promedio académico.
    float promedio() const {
        return ppa_;
    }

    // Actualiza el promedio académico del estudiante.
    void set_ppa(float valor) {
        ppa_ = valor;
    }
};


// ================================================================
// 2. INTERFAZ Y ESTRATEGIA DE CÁLCULO
// RESPONSABILIDAD: definir y realizar el cálculo del promedio.
// ================================================================

// Esta interfaz establece el contrato de las estrategias.
struct IEstrategiaCalculo {

    // Toda estrategia debe implementar el método calcular().
    virtual float calcular(
        const std::vector<float>& notas
    ) const = 0;

    // Destructor virtual para permitir herencia segura.
    virtual ~IEstrategiaCalculo() = default;
};


// ================================================================
// CLASE PROMEDIO SIMPLE
// RESPONSABILIDAD: calcular la media aritmética.
// ================================================================

class PromedioSimple : public IEstrategiaCalculo {

public:

    // Implementamos el método calcular definido en la interfaz.
    float calcular(
        const std::vector<float>& notas
    ) const override {

        // Si no existen notas, devolvemos cero.
        if (notas.empty()) {
            return 0.0f;
        }

        // Variable que acumula la suma de todas las notas.
        float suma = 0.0f;

        // Recorremos cada nota del vector.
        for (float nota : notas) {
            suma += nota;
        }

        // Dividimos la suma entre la cantidad de notas.
        return suma / notas.size();
    }
};


// ================================================================
// 3. INTERFAZ DEL REPOSITORIO
// RESPONSABILIDAD: definir cómo se almacenan los estudiantes.
// ================================================================

struct IRepositorioEstudiante {

    // Define la operación que permite guardar un estudiante.
    virtual void guardar(const Estudiante& e) = 0;

    // Destructor virtual para permitir el uso polimórfico.
    virtual ~IRepositorioEstudiante() = default;
};


// ================================================================
// CLASE REPOSITORIO ARCHIVO
// RESPONSABILIDAD: guardar estudiantes en un archivo CSV.
// ================================================================

class RepositorioArchivo : public IRepositorioEstudiante {

public:

    // Implementamos el método guardar de la interfaz.
    void guardar(const Estudiante& e) override {

        // Abrimos el archivo en modo agregar para conservar
        // los registros anteriores.
        std::ofstream archivo(
            "estudiantes_s10.csv",
            std::ios::app
        );

        // Comprobamos si el archivo pudo abrirse correctamente.
        if (!archivo) {
            std::cerr << "Error al abrir el archivo CSV.\n";
            return;
        }

        // Escribimos código, nombre y promedio separados por comas.
        archivo << e.codigo() << ","
                << e.nombre() << ","
                << e.promedio() << '\n';

        // Confirmamos en la terminal que se guardó el registro.
        std::cout << "Estudiante guardado en CSV.\n";
    }
};


// ================================================================
// 4. SERVICIO ESTUDIANTE
// RESPONSABILIDAD: coordinar cálculo y almacenamiento.
// ================================================================

class ServicioEstudiante {

private:

    // Referencia al repositorio encargado de guardar estudiantes.
    IRepositorioEstudiante& repo_;

    // Referencia a la estrategia encargada de calcular promedios.
    const IEstrategiaCalculo& calc_;

public:

    // Constructor: recibe las dependencias necesarias.
    // Esto aplica DIP porque depende de interfaces.
    ServicioEstudiante(
        IRepositorioEstudiante& repo,
        const IEstrategiaCalculo& calc
    ) : repo_(repo), calc_(calc) {
    }

    // Registra al estudiante calculando primero su promedio.
    void registrar(
        Estudiante& e,
        const std::vector<float>& notas
    ) {

        // Calculamos el PPA utilizando la estrategia recibida.
        e.set_ppa(calc_.calcular(notas));

        // Guardamos al estudiante con su promedio actualizado.
        repo_.guardar(e);
    }
};


// ================================================================
// 5. PROGRAMA PRINCIPAL
// RESPONSABILIDAD: probar el funcionamiento de las clases.
// ================================================================

int main() {

    // Mostramos el título de la actividad.
    std::cout << "========================================\n";
    std::cout << "ACTIVIDAD 1A - REFACTORIZACION SRP\n";
    std::cout << "========================================\n";

    // Creamos la estrategia de cálculo de promedio simple.
    PromedioSimple calculadora;

    // Creamos el repositorio que guarda los datos en CSV.
    RepositorioArchivo repositorio;

    // Creamos el servicio conectando repositorio y calculadora.
    ServicioEstudiante servicio(repositorio, calculadora);

    // Creamos un estudiante con código y nombre.
    Estudiante alumno(1001, "Ana Quispe");

    // Creamos un vector con las notas académicas.
    std::vector<float> notas = {14.0f, 16.0f, 18.0f};

    // Registramos al estudiante.
    // El servicio calcula su PPA y luego lo guarda en CSV.
    servicio.registrar(alumno, notas);

    // Mostramos los datos finales del estudiante.
    std::cout << "\nDATOS DEL ESTUDIANTE\n";

    // Mostramos su código.
    std::cout << "Codigo: " << alumno.codigo() << '\n';

    // Mostramos su nombre.
    std::cout << "Nombre: " << alumno.nombre() << '\n';

    // Mostramos su promedio académico.
    std::cout << "PPA: " << alumno.promedio() << '\n';

    // Indicamos que el programa terminó correctamente.
    std::cout << "\nActividad finalizada correctamente.\n";

    // Devolvemos cero para indicar ejecución exitosa.
    return 0;
}
