
// ACTIVIDAD 2: FACTORY METHOD - GENERADOR DE BOLETAS.
// Implementación en C++17.

// Permite mostrar información en la terminal.
#include <iostream>

// Permite leer y escribir archivos.
#include <fstream>

// Permite trabajar con cadenas de texto.
#include <string>

// Permite almacenar notas en vectores.
#include <vector>

// Permite utilizar punteros inteligentes.
#include <memory>

// Permite almacenar los generadores en un mapa.
#include <map>

// Permite almacenar funciones creadoras.
#include <functional>

// Permite dar formato a los números decimales.
#include <iomanip>

// Permite construir cadenas de texto.
#include <sstream>

// Permite lanzar excepciones.
#include <stdexcept>

// Permite utilizar el tipo JSON.
#include <nlohmann/json.hpp>

// Crea un nombre corto para el tipo JSON.
using json = nlohmann::json;


// =====================================================
// 1. ESTRUCTURA PARA ALMACENAR UNA NOTA
// =====================================================

// Representa una asignatura y su calificación.
struct Nota {

    // Guarda el nombre de la asignatura.
    std::string asignatura;

    // Guarda la calificación obtenida.
    double valor;
};


// =====================================================
// 2. PRODUCTO ABSTRACTO
// =====================================================

// Define las operaciones que tendrá toda boleta.
class BoletaNotas {

public:

    // Destructor virtual para las clases derivadas.
    virtual ~BoletaNotas() = default;

    // Método abstracto para agregar una nota.
    virtual void agregar_nota(
        const std::string& asignatura,
        double valor
    ) = 0;

    // Método abstracto para generar el documento.
    virtual std::string generar(
        const std::string& estudiante,
        double promedio
    ) const = 0;

    // Método abstracto que devuelve la extensión.
    virtual std::string extension() const noexcept = 0;
};


// =====================================================
// 3. PRODUCTOS CONCRETOS
// =====================================================


// PRODUCTO TXT: genera una boleta de texto plano.
class BoletaTXT : public BoletaNotas {

private:

    // Vector que almacena las notas.
    std::vector<Nota> notas_;

public:

    // Agrega una nota al vector.
    void agregar_nota(
        const std::string& asignatura,
        double valor
    ) override {

        // Inserta la asignatura y su nota.
        notas_.push_back({asignatura, valor});
    }

    // Genera el contenido en formato TXT.
    std::string generar(
        const std::string& estudiante,
        double promedio
    ) const override {

        // Crea un flujo para construir el documento.
        std::ostringstream salida;

        // Escribe el título.
        salida << "BOLETA DE NOTAS\n";

        // Escribe el nombre del estudiante.
        salida << "Estudiante: " << estudiante << "\n";

        // Escribe una línea separadora.
        salida << "-----------------------------\n";

        // Establece dos decimales.
        salida << std::fixed << std::setprecision(2);

        // Recorre las notas almacenadas.
        for (const auto& nota : notas_) {

            // Escribe la asignatura y su calificación.
            salida << nota.asignatura
                   << ": "
                   << nota.valor
                   << "\n";
        }

        // Escribe el promedio.
        salida << "Promedio: " << promedio << "\n";

        // Devuelve el documento completo.
        return salida.str();
    }

    // Devuelve la extensión TXT.
    std::string extension() const noexcept override {
        return ".txt";
    }
};


// PRODUCTO CSV: genera una boleta separada por comas.
class BoletaCSV : public BoletaNotas {

private:

    // Vector que almacena las notas.
    std::vector<Nota> notas_;

public:

    // Agrega una nota al vector.
    void agregar_nota(
        const std::string& asignatura,
        double valor
    ) override {

        // Inserta la asignatura y su calificación.
        notas_.push_back({asignatura, valor});
    }

    // Genera el contenido en formato CSV.
    std::string generar(
        const std::string& estudiante,
        double promedio
    ) const override {

        // Crea un flujo para construir el CSV.
        std::ostringstream salida;

        // Escribe los encabezados.
        salida << "Estudiante,Asignatura,Nota\n";

        // Establece dos decimales.
        salida << std::fixed << std::setprecision(2);

        // Recorre las notas almacenadas.
        for (const auto& nota : notas_) {

            // Escribe una fila del archivo CSV.
            salida << estudiante << ","
                   << nota.asignatura << ","
                   << nota.valor << "\n";
        }

        // Agrega el promedio al final.
        salida << estudiante
               << ",Promedio,"
               << promedio << "\n";

        // Devuelve el contenido CSV.
        return salida.str();
    }

    // Devuelve la extensión CSV.
    std::string extension() const noexcept override {
        return ".csv";
    }
};


// PRODUCTO HTML: genera una boleta como página web.
class BoletaHTML : public BoletaNotas {

private:

    // Vector que almacena las notas.
    std::vector<Nota> notas_;

public:

    // Agrega una nota al vector.
    void agregar_nota(
        const std::string& asignatura,
        double valor
    ) override {

        // Inserta la asignatura y su calificación.
        notas_.push_back({asignatura, valor});
    }

    // Genera el documento HTML.
    std::string generar(
        const std::string& estudiante,
        double promedio
    ) const override {

        // Crea un flujo para construir el HTML.
        std::ostringstream salida;

        // Inicia el documento HTML.
        salida << "<!DOCTYPE html>\n";

        // Define el idioma español.
        salida << "<html lang=\"es\">\n";

        // Abre la sección de encabezado.
        salida << "<head>\n";

        // Define la codificación de caracteres.
        salida << "<meta charset=\"UTF-8\">\n";

        // Define el título de la página.
        salida << "<title>Boleta de notas</title>\n";

        // Cierra el encabezado.
        salida << "</head>\n";

        // Inicia el contenido visible.
        salida << "<body>\n";

        // Escribe el título principal.
        salida << "<h1>Boleta de notas</h1>\n";

        // Escribe el nombre del estudiante.
        salida << "<p>Estudiante: " << estudiante << "</p>\n";

        // Abre la tabla de notas.
        salida << "<table border=\"1\">\n";

        // Escribe los encabezados de la tabla.
        salida << "<tr><th>Asignatura</th><th>Nota</th></tr>\n";

        // Establece dos decimales.
        salida << std::fixed << std::setprecision(2);

        // Recorre todas las notas.
        for (const auto& nota : notas_) {

            // Escribe una fila de la tabla HTML.
            salida << "<tr><td>"
                   << nota.asignatura
                   << "</td><td>"
                   << nota.valor
                   << "</td></tr>\n";
        }

        // Cierra la tabla.
        salida << "</table>\n";

        // Escribe el promedio.
        salida << "<p>Promedio: " << promedio << "</p>\n";

        // Cierra el cuerpo del documento.
        salida << "</body>\n";

        // Cierra el documento HTML.
        salida << "</html>\n";

        // Devuelve el contenido HTML.
        return salida.str();
    }

    // Devuelve la extensión HTML.
    std::string extension() const noexcept override {
        return ".html";
    }
};


// =====================================================
// 4. CREADOR BASE: FACTORY METHOD
// =====================================================

// Define el creador abstracto de las boletas.
class GeneradorBoleta {

public:

    // Destructor virtual.
    virtual ~GeneradorBoleta() = default;

    // FACTORY METHOD:
    // Las subclases deciden qué producto crear.
    virtual std::unique_ptr<BoletaNotas>
    crear_boleta() const = 0;


    // TEMPLATE METHOD:
    // Define los pasos generales para generar y guardar.
    void generar_y_enviar(
        const std::string& estudiante,
        double promedio,
        const std::vector<Nota>& notas,
        const std::string& nombre_base
    ) const {

        // Crea el producto mediante Factory Method.
        auto boleta = crear_boleta();

        // Recorre todas las notas recibidas.
        for (const auto& nota : notas) {

            // Agrega cada nota al producto creado.
            boleta->agregar_nota(
                nota.asignatura,
                nota.valor
            );
        }

        // Genera el contenido del documento.
        std::string contenido =
            boleta->generar(estudiante, promedio);

        // Construye el nombre con la extensión correspondiente.
        std::string archivo =
            nombre_base + boleta->extension();

        // Abre el archivo de salida.
        std::ofstream salida(archivo);

        // Comprueba si el archivo pudo abrirse.
        if (!salida.is_open()) {

            // Informa el error si no se pudo crear.
            throw std::runtime_error(
                "No se pudo crear: " + archivo
            );
        }

        // Escribe el contenido en el archivo.
        salida << contenido;

        // Cierra el archivo.
        salida.close();

        // Informa que se generó la boleta.
        std::cout << "Boleta generada: "
                  << archivo << "\n";

        // Simula el envío al estudiante.
        std::cout << "Envio simulado al estudiante: "
                  << estudiante << "\n";
    }
};


// =====================================================
// 5. CREADORES CONCRETOS
// =====================================================


// Generador concreto para el formato TXT.
class GeneradorTXT : public GeneradorBoleta {

public:

    // Implementa el Factory Method para TXT.
    std::unique_ptr<BoletaNotas>
    crear_boleta() const override {

        // Crea y devuelve una BoletaTXT.
        return std::make_unique<BoletaTXT>();
    }
};


// Generador concreto para el formato CSV.
class GeneradorCSV : public GeneradorBoleta {

public:

    // Implementa el Factory Method para CSV.
    std::unique_ptr<BoletaNotas>
    crear_boleta() const override {

        // Crea y devuelve una BoletaCSV.
        return std::make_unique<BoletaCSV>();
    }
};


// Generador concreto para el formato HTML.
class GeneradorHTML : public GeneradorBoleta {

public:

    // Implementa el Factory Method para HTML.
    std::unique_ptr<BoletaNotas>
    crear_boleta() const override {

        // Crea y devuelve una BoletaHTML.
        return std::make_unique<BoletaHTML>();
    }
};


// =====================================================
// 6. REGISTRO DE GENERADORES
// =====================================================

// Relaciona cada formato con su fábrica correspondiente.
class RegistroGeneradores {

private:

    // Define el tipo de función que crea un generador.
    using Creador =
        std::function<std::unique_ptr<GeneradorBoleta>()>;

    // Mapa que almacena las fábricas por formato.
    std::map<std::string, Creador> registro_;

public:

    // Registra una fábrica con el nombre de su formato.
    void registrar(
        const std::string& formato,
        Creador creador
    ) {

        // Guarda la fábrica en el mapa.
        registro_[formato] = std::move(creador);
    }

    // Recupera y ejecuta la fábrica solicitada.
    std::unique_ptr<GeneradorBoleta>
    crear(const std::string& formato) const {

        // Busca el formato en el mapa.
        auto it = registro_.find(formato);

        // Comprueba si el formato no está registrado.
        if (it == registro_.end()) {

            // Lanza una excepción indicando el formato desconocido.
            throw std::invalid_argument(
                "Formato no registrado: " + formato
            );
        }

        // Ejecuta la función creadora y devuelve el generador.
        return it->second();
    }
};


// =====================================================
// 7. FUNCIÓN PRINCIPAL
// =====================================================

int main() {

    // Captura posibles errores durante la ejecución.
    try {

        // Abre el archivo JSON de configuración.
        std::ifstream archivoConfig("config.json");

        // Comprueba si se pudo abrir.
        if (!archivoConfig.is_open()) {

            // Informa que no se encontró el archivo.
            throw std::runtime_error(
                "No se pudo abrir config.json"
            );
        }

        // Declara el objeto JSON.
        json config;

        // Lee el contenido del archivo JSON.
        archivoConfig >> config;

        // Obtiene el nombre del estudiante.
        std::string estudiante =
            config.at("estudiante").get<std::string>();

        // Obtiene el promedio.
        double promedio =
            config.at("promedio").get<double>();

        // Obtiene el nombre base de los archivos.
        std::string nombreBase =
            config.value("nombre_base", "boleta");

        // Crea un vector para almacenar las notas.
        std::vector<Nota> notas;

        // Recorre las notas del archivo JSON.
        for (const auto& item : config.at("notas")) {

            // Agrega cada asignatura y su nota al vector.
            notas.push_back({
                item.at("asignatura").get<std::string>(),
                item.at("valor").get<double>()
            });
        }

        // Crea el registro de fábricas.
        RegistroGeneradores registro;

        // Registra el generador TXT.
        registro.registrar("txt", [] {
            return std::make_unique<GeneradorTXT>();
        });

        // Registra el generador CSV.
        registro.registrar("csv", [] {
            return std::make_unique<GeneradorCSV>();
        });

        // Registra el generador HTML.
        registro.registrar("html", [] {
            return std::make_unique<GeneradorHTML>();
        });

        // Recorre los formatos solicitados en el JSON.
        for (const auto& formato : config.at("formatos")) {

            // Convierte el formato a texto.
            std::string tipo = formato.get<std::string>();

            // Obtiene el generador correspondiente.
            auto generador = registro.crear(tipo);

            // Genera y guarda la boleta.
            generador->generar_y_enviar(
                estudiante,
                promedio,
                notas,
                nombreBase
            );
        }

    }

    // Captura los errores estándar.
    catch (const std::exception& error) {

        // Muestra el mensaje del error.
        std::cerr << "Error: " << error.what() << "\n";

        // Devuelve un código de error.
        return 1;
    }

    // Indica que el programa terminó correctamente.
    return 0;
}
