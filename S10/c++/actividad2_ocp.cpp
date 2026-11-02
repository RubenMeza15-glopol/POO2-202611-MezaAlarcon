
/*
===============================================================
CURSO: PROGRAMACION ORIENTADA A OBJETOS II - POO II
UNIDAD: SEGUNDA UNIDAD
SEMANA: 10

ACTIVIDAD 2: OCP - AGREGAR PROMEDIO MODERADO
             SIN MODIFICAR SERVICIO ESTUDIANTE

PREGUNTA DEL INGENIERO:
Agregar una nueva estrategia de cálculo llamada
PromedioModerado sin modificar el código fuente
de ServicioEstudiante.

¿QUE NOS PIDE RESOLVER?
1. Implementar PromedioModerado con sort y accumulate.
2. Cambiar solamente la estrategia en main().
3. Comprobar el PPA obtenido.
4. Probar también PromedioSimple.

RESOLUCION:
Creamos una nueva estrategia que descarta la nota
más alta y la más baja antes de calcular el promedio.
===============================================================
*/

// Permite trabajar con cadenas de texto.
#include <string>

// Permite mostrar información en la terminal.
#include <iostream>

// Permite utilizar vectores para almacenar notas.
#include <vector>

// Permite ordenar las notas de menor a mayor.
#include <algorithm>

// Permite sumar los elementos de un rango.
#include <numeric>

// ============================================================
// INTERFAZ: I estrategia de cálculo.
// Define el contrato que deben cumplir las estrategias.
// ============================================================

struct IEstrategiaCalculo {

    // Función virtual para calcular el promedio.
    virtual float calcular(
        const std::vector<float>& notas
    ) const = 0;

    // Destructor virtual para una destrucción correcta.
    virtual ~IEstrategiaCalculo() = default;
};

// ============================================================
// ESTRATEGIA 1: PROMEDIO SIMPLE.
// Calcula el promedio de todas las notas.
// ============================================================

struct PromedioSimple : IEstrategiaCalculo {

    float calcular(
        const std::vector<float>& notas
    ) const override {

        // Si no existen notas, devolvemos cero.
        if (notas.empty()) return 0.0f;

        // Sumamos todas las notas y dividimos
        // entre la cantidad total de notas.
        float suma = std::accumulate(
            notas.begin(), notas.end(), 0.0f
        );

        return suma / notas.size();
    }
};

// ============================================================
// ACTIVIDAD 2: ESTRATEGIA PROMEDIO MODERADO.
// PREGUNTA: ¿Cómo descartar la nota más alta y la más baja?
// RESOLUCION: Ordenamos, excluimos los extremos y promediamos.
// ============================================================

struct PromedioModerado : IEstrategiaCalculo {

    float calcular(
        const std::vector<float>& notas
    ) const override {

        // Con dos notas o menos no podemos descartar
        // una nota alta y una baja y conservar datos.
        if (notas.size() <= 2) return 0.0f;

        // Copiamos las notas para no modificar el vector original.
        auto ordenadas = notas;

        // Ordenamos las notas de menor a mayor.
        std::sort(ordenadas.begin(), ordenadas.end());

        // Sumamos desde la segunda nota hasta la penúltima.
        // Así descartamos la nota menor y la nota mayor.
        float suma = std::accumulate(
            ordenadas.begin() + 1,
            ordenadas.end() - 1,
            0.0f
        );

        // Calculamos cuántas notas quedaron.
        float cantidad = ordenadas.size() - 2;

        // Devolvemos el promedio de las notas restantes.
        return suma / cantidad;
    }
};

// ============================================================
// REPOSITORIO: almacenamiento temporal de estudiantes.
// ============================================================

struct RepositorioMemoria {

    // Guarda el código, nombre y promedio del estudiante.
    void guardar(int codigo, const std::string& nombre,
                 float ppa) {

        std::cout << "\nEstudiante guardado correctamente."
                  << '\n';

        std::cout << "Codigo: " << codigo << '\n';
        std::cout << "Nombre: " << nombre << '\n';
        std::cout << "PPA almacenado: " << ppa << '\n';
    }
};

// ============================================================
// SERVICIO ESTUDIANTE.
// IMPORTANTE: no modificamos esta clase para agregar
// PromedioModerado. Recibe cualquier estrategia compatible.
// ============================================================

class ServicioEstudiante {

private:

    // Referencia a la estrategia de cálculo seleccionada.
    const IEstrategiaCalculo& calculadora_;

    // Referencia al repositorio de almacenamiento.
    RepositorioMemoria& repositorio_;

public:

    // Constructor: recibe la estrategia y el repositorio.
    ServicioEstudiante(
        RepositorioMemoria& repo,
        const IEstrategiaCalculo& calculadora
    )
        : repositorio_(repo),
          calculadora_(calculadora) {
    }

    // Registra un estudiante y calcula su promedio.
    void registrar(
        int codigo,
        const std::string& nombre,
        const std::vector<float>& notas
    ) {

        // Utiliza la estrategia recibida para calcular el PPA.
        float ppa = calculadora_.calcular(notas);

        // Envía los datos al repositorio.
        repositorio_.guardar(codigo, nombre, ppa);
    }
};

// ============================================================
// PROGRAMA PRINCIPAL.
// Aquí seleccionamos qué estrategia queremos utilizar.
// ============================================================

int main() {

    // Creamos el repositorio en memoria.
    RepositorioMemoria repo;

    // ACTIVIDAD 2:
    // Seleccionamos la estrategia de promedio moderado.
    PromedioModerado calc;

    // ServicioEstudiante no necesita ser modificado.
    ServicioEstudiante svc(repo, calc);

    // Creamos un estudiante con sus respectivas notas.
    std::vector<float> notas = {
        14.0f, 20.0f, 16.0f, 18.0f, 12.0f
    };

    // Registramos al estudiante.
    svc.registrar(1001, "Ana Quispe", notas);

    // Finalizamos correctamente el programa.
    return 0;
}
