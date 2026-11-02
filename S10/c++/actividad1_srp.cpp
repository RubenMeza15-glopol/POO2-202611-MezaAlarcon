
/*
====================================================================
CURSO: PROGRAMACION ORIENTADA A OBJETOS II - POO II
UNIDAD: SEGUNDA UNIDAD
SEMANA: 10
ACTIVIDAD 1: SRP - DE ESTUDIANTEGOD A 4 CLASES
LENGUAJE: C++17
====================================================================

PREGUNTA DEL INGENIERO:

La siguiente clase viola el SRP porque tiene al menos cuatro
razones para cambiar. Identificalas antes de ver la solucion.

¿QUE NOS PIDE RESOLVER?

1. Identificar las cuatro responsabilidades de EstudianteGod.
2. Separar el calculo del promedio academico.
3. Separar la persistencia de los datos.
4. Separar la serializacion de la informacion a JSON.
5. Separar el envio de notificaciones por correo.

ANALISIS:

La clase EstudianteGod concentra cuatro responsabilidades
diferentes en una sola clase.

Esto significa que un cambio en cualquiera de esas tareas
obligaria a modificar la misma clase.

SOLUCION:

Aplicaremos el principio SRP separando cada responsabilidad
en una clase especializada.

La clase Estudiante almacenara los datos del alumno.
CalculadoraPPA calculara el promedio.
RepositorioEstudiante guardara la informacion.
SerializadorJSON convertira los datos a JSON.
NotificadorCorreo gestionara las notificaciones.

OBJETIVO:

Conseguir que cada clase tenga una responsabilidad definida
y que los cambios en una tarea no afecten a las demas.

====================================================================
*/

// Incluimos iostream para mostrar mensajes en la terminal.
#include <iostream>

// Incluimos string para trabajar con cadenas de texto.
#include <string>

// Incluimos vector para almacenar las notas del estudiante.
#include <vector>

// Incluimos fstream para guardar informacion en archivos.
#include <fstream>

// Incluimos numeric para utilizar la funcion accumulate.
#include <numeric>

// Incluimos sstream para construir cadenas de texto JSON.
#include <sstream>

// ================================================================
// CLASE 1: ESTUDIANTE
// RESPONSABILIDAD: almacenar los datos del estudiante.
// ================================================================

class Estudiante {

private:

    // Almacena el codigo unico del estudiante.
    int codigo;

    // Almacena el nombre completo del estudiante.
    std::string nombre;

    // Almacena el promedio ponderado academico.
    float ppa;

    // Almacena las notas obtenidas por el estudiante.
    std::vector<float> notas;

public:

    // Constructor que recibe e inicializa los datos del estudiante.
    Estudiante(int cod, std::string nom, std::vector<float> n)
        : codigo(cod), nombre(nom), ppa(0.0f), notas(n) {
    }

    // Devuelve el codigo del estudiante.
    int obtenerCodigo() const {
        return codigo;
    }

    // Devuelve el nombre del estudiante.
    std::string obtenerNombre() const {
        return nombre;
    }

    // Devuelve el promedio academico del estudiante.
    float obtenerPPA() const {
        return ppa;
    }

    // Devuelve las notas del estudiante sin permitir modificarlas.
    const std::vector<float>& obtenerNotas() const {
        return notas;
    }

    // Actualiza el promedio academico despues de calcularlo.
    void establecerPPA(float nuevoPPA) {
        ppa = nuevoPPA;
    }
};

// ================================================================
// CLASE 2: CALCULADORA PPA
// RESPONSABILIDAD: calcular el promedio de las notas.
// ================================================================

class CalculadoraPPA {

public:

    // Recibe las notas y devuelve el promedio academico.
    float calcular(const std::vector<float>& notas) {

        // Comprueba si el estudiante no tiene notas registradas.
        if (notas.empty()) {

            // Devuelve cero para evitar una division entre cero.
            return 0.0f;
        }

        // Suma todas las notas del estudiante.
        float suma = std::accumulate(notas.begin(), notas.end(), 0.0f);

        // Divide la suma entre la cantidad de notas.
        return suma / notas.size();
    }
};

// ================================================================
// CLASE 3: REPOSITORIO ESTUDIANTE
// RESPONSABILIDAD: guardar los datos en un archivo.
// ================================================================

class RepositorioEstudiante {

public:

    // Recibe un estudiante y la ruta del archivo donde se guardara.
    void guardarEnArchivo(const Estudiante& estudiante,
                          const std::string& ruta) {

        // Abre el archivo en modo de añadir para conservar registros.
        std::ofstream archivo(ruta, std::ios::app);

        // Comprueba si el archivo se abrio correctamente.
        if (!archivo.is_open()) {

            // Muestra un mensaje de error si no se pudo abrir.
            std::cerr << "Error al abrir el archivo.\n";

            // Finaliza el metodo si no se puede guardar.
            return;
        }

        // Escribe el codigo, nombre y PPA separados por comas.
        archivo << estudiante.obtenerCodigo() << ","
                << estudiante.obtenerNombre() << ","
                << estudiante.obtenerPPA() << "\n";

        // Cierra el archivo despues de guardar los datos.
        archivo.close();
    }
};

// ================================================================
// CLASE 4: SERIALIZADOR JSON
// RESPONSABILIDAD: convertir los datos del estudiante a JSON.
// ================================================================

class SerializadorJSON {

public:

    // Recibe un estudiante y devuelve sus datos en formato JSON.
    std::string convertir(const Estudiante& estudiante) {

        // Crea un flujo de texto para construir el JSON.
        std::ostringstream json;

        // Escribe la apertura del objeto y el codigo del estudiante.
        json << "{\"codigo\":"
             << estudiante.obtenerCodigo();

        // Escribe el nombre del estudiante en formato JSON.
        json << ",\"nombre\":\""
             << estudiante.obtenerNombre() << "\"";

        // Escribe el promedio academico del estudiante.
        json << ",\"ppa\":"
             << estudiante.obtenerPPA();

        // Cierra el objeto JSON.
        json << "}";

        // Devuelve el texto JSON que se ha construido.
        return json.str();
    }
};

// ================================================================
// CLASE 5: NOTIFICADOR CORREO
// RESPONSABILIDAD: gestionar las notificaciones por correo.
// ================================================================

class NotificadorCorreo {

public:

    // Recibe la direccion de correo del destinatario.
    void enviarCorreo(const std::string& destinatario) {

        // Muestra un mensaje que representa el envio del correo.
        std::cout << "Enviando correo a: "
                  << destinatario << "\n";
    }
};

// ================================================================
// PROGRAMA PRINCIPAL
// RESPONSABILIDAD: probar el funcionamiento de las clases.
// ================================================================

int main() {

    // Muestra el titulo de la actividad en la terminal.
    std::cout << "====================================\n";

    // Identifica la actividad que estamos ejecutando.
    std::cout << "ACTIVIDAD 1 - PRINCIPIO SRP\n";

    // Muestra el nombre de la practica.
    std::cout << "DE ESTUDIANTEGOD A CLASES SEPARADAS\n";

    // Muestra una linea para separar el encabezado.
    std::cout << "====================================\n\n";

    // Crea un estudiante con codigo, nombre y tres notas.
    Estudiante estudiante(1001, "Ana Quispe", {14, 16, 18});

    // Crea el objeto encargado de calcular el PPA.
    CalculadoraPPA calculadora;

    // Crea el objeto encargado de guardar los datos.
    RepositorioEstudiante repositorio;

    // Crea el objeto encargado de convertir los datos a JSON.
    SerializadorJSON serializador;

    // Crea el objeto encargado de gestionar las notificaciones.
    NotificadorCorreo notificador;

    // Calcula el promedio utilizando la clase especializada.
    float promedio = calculadora.calcular(estudiante.obtenerNotas());

    // Actualiza el PPA del estudiante con el resultado obtenido.
    estudiante.establecerPPA(promedio);

    // Muestra el codigo del estudiante.
    std::cout << "Codigo: " << estudiante.obtenerCodigo() << "\n";

    // Muestra el nombre del estudiante.
    std::cout << "Nombre: " << estudiante.obtenerNombre() << "\n";

    // Muestra el promedio academico calculado.
    std::cout << "PPA: " << estudiante.obtenerPPA() << "\n\n";

    // Guarda la informacion del estudiante en un archivo CSV.
    repositorio.guardarEnArchivo(estudiante, "estudiantes.csv");

    // Convierte los datos del estudiante al formato JSON.
    std::string datosJSON = serializador.convertir(estudiante);

    // Muestra la informacion JSON en la terminal.
    std::cout << "Datos en formato JSON:\n";

    // Imprime el contenido JSON generado.
    std::cout << datosJSON << "\n\n";

    // Ejecuta la notificacion con una direccion de ejemplo.
    notificador.enviarCorreo("ana@unap.edu.pe");

    // Muestra un mensaje que confirma el fin de la actividad.
    std::cout << "\nActividad 1 finalizada correctamente.\n";

    // Devuelve cero para indicar que el programa termino bien.
    return 0;
}

/*
====================================================================
CONCLUSION DE LA ACTIVIDAD 1:

Se identificaron las cuatro responsabilidades que estaban
concentradas en la clase EstudianteGod:

1. Calculo del promedio academico.
2. Persistencia de informacion.
3. Serializacion de datos.
4. Envio de notificaciones.

Posteriormente, estas responsabilidades se separaron en clases
especializadas.

De esta manera, cada clase tiene una funcion definida y los
cambios en una responsabilidad no obligan a modificar las demas.

Por lo tanto, la solucion aplica el principio SRP
(Single Responsibility Principle).

====================================================================
*/
