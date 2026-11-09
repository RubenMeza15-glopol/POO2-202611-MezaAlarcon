
#include <iostream>     // Permite mostrar información en la terminal.
#include <fstream>      // Permite crear y escribir archivos.
#include <string>       // Permite trabajar con cadenas de texto.
#include <mutex>        // Permite proteger operaciones entre hilos.
#include <chrono>       // Permite obtener la fecha y hora actual.
#include <iomanip>      // Permite dar formato a la fecha y hora.
#include <sstream>      // Permite construir cadenas de texto.
#include <ctime>        // Permite convertir fechas y horas.
#include <stdexcept>    // Permite utilizar excepciones estándar.
#include <cassert>      // Permite realizar pruebas mediante assert.

// Enumeración que define los niveles de importancia de los registros.
enum class NivelLog {
    DEBUG,              // Mensajes para depuración.
    INFO,               // Mensajes informativos.
    WARN,               // Mensajes de advertencia.
    ERROR               // Mensajes de error.
};

// Declaración de la clase Logger.
class Logger {

private: // Sección privada: contiene datos y métodos internos.

    std::ofstream archivo_; // Archivo donde se guardarán los registros.
    std::mutex mtx_;        // Protege la escritura simultánea.
    NivelLog nivelMinimo_;  // Define el nivel mínimo que se registrará.

    // Constructor privado: impide crear objetos directamente desde fuera.
    explicit Logger(const std::string& ruta = "app.log")
        : nivelMinimo_(NivelLog::DEBUG) { // Inicializa el nivel mínimo.

        // Abre el archivo en modo append para conservar registros anteriores.
        archivo_.open(ruta, std::ios::app);

        // Comprueba si el archivo se abrió correctamente.
        if (!archivo_.is_open()) {

            // Lanza una excepción si no se pudo abrir el archivo.
            throw std::runtime_error("No se puede abrir: " + ruta);
        }
    }

    // Elimina el constructor de copia para impedir duplicar el Singleton.
    Logger(const Logger&) = delete;

    // Elimina la asignación por copia.
    Logger& operator=(const Logger&) = delete;

    // Elimina el constructor de movimiento.
    Logger(Logger&&) = delete;

    // Elimina la asignación por movimiento.
    Logger& operator=(Logger&&) = delete;

    // Método privado que obtiene la fecha y hora actual.
    std::string timestamp() const {

        // Obtiene el instante actual del sistema.
        auto now = std::chrono::system_clock::now();

        // Convierte el instante a tiempo de calendario.
        auto t = std::chrono::system_clock::to_time_t(now);

        // Crea un objeto para construir una cadena de texto.
        std::ostringstream oss;

        // Convierte la fecha y hora al formato año-mes-día.
        oss << std::put_time(
            std::localtime(&t),
            "%Y-%m-%d %H:%M:%S"
        );

        // Devuelve la fecha y hora como una cadena.
        return oss.str();
    }

    // Convierte el nivel de registro en una palabra.
    static std::string nivelStr(NivelLog nivel) {

        // Evalúa el nivel recibido.
        switch (nivel) {

            case NivelLog::DEBUG: return "DEBUG"; // Devuelve DEBUG.
            case NivelLog::INFO:  return "INFO";  // Devuelve INFO.
            case NivelLog::WARN:  return "WARN";  // Devuelve WARN.
            case NivelLog::ERROR: return "ERROR"; // Devuelve ERROR.
        }

        // Devuelve este texto si no coincide con ningún nivel.
        return "UNKNOWN";
    }

public: // Sección pública: contiene métodos accesibles desde otras clases.

    // Método estático que proporciona el acceso único al Logger.
    static Logger& instancia(
        const std::string& ruta = "app.log"
    ) {

        // Crea una única instancia local estática de Logger.
        static Logger inst(ruta);

        // Devuelve una referencia al mismo objeto.
        return inst;
    }

    // Método general que registra mensajes.
    void log(
        NivelLog nivel,                  // Recibe el nivel del mensaje.
        const std::string& modulo,       // Recibe el nombre del módulo.
        const std::string& mensaje       // Recibe el contenido del mensaje.
    ) {

        // Ignora mensajes inferiores al nivel mínimo configurado.
        if (nivel < nivelMinimo_) {
            return;                      // Termina el método.
        }

        // Bloquea temporalmente el acceso para proteger la escritura.
        std::lock_guard<std::mutex> lock(mtx_);

        // Construye el mensaje con fecha, nivel, módulo y contenido.
        std::string entrada =
            "[" + timestamp() + "] [" +
            nivelStr(nivel) + "] [" +
            modulo + "] " + mensaje;

        // Escribe el registro en el archivo.
        archivo_ << entrada << "\n";

        // Fuerza el envío del contenido al archivo.
        archivo_.flush();

        // Muestra el mismo registro en la terminal.
        std::cout << entrada << "\n";
    }

    // Método para registrar mensajes de depuración.
    void debug(const std::string& mod, const std::string& msg) {
        log(NivelLog::DEBUG, mod, msg); // Registra un mensaje DEBUG.
    }

    // Método para registrar mensajes informativos.
    void info(const std::string& mod, const std::string& msg) {
        log(NivelLog::INFO, mod, msg); // Registra un mensaje INFO.
    }

    // Método para registrar advertencias.
    void warn(const std::string& mod, const std::string& msg) {
        log(NivelLog::WARN, mod, msg); // Registra un mensaje WARN.
    }

    // Método para registrar errores.
    void error(const std::string& mod, const std::string& msg) {
        log(NivelLog::ERROR, mod, msg); // Registra un mensaje ERROR.
    }
};

// Clase que representa el servicio de matrícula.
class ServicioMatricula {

public: // Permite utilizar el método desde main.

    // Método que simula la matrícula de un estudiante.
    void matricular(
        const std::string& estudiante, // Recibe el código o nombre.
        const std::string& curso       // Recibe el curso.
    ) {

        // Registra el inicio del proceso de matrícula.
        Logger::instancia().info(
            "ServicioMatricula",
            "Matriculando " + estudiante + " en " + curso
        );

        // Registra que la matrícula se realizó correctamente.
        Logger::instancia().info(
            "ServicioMatricula",
            "Matricula exitosa"
        );
    }
};

// Función principal: punto de inicio del programa.
int main() {

    // Obtiene la primera referencia al Singleton.
    Logger& log1 = Logger::instancia();

    // Registra un mensaje de depuración.
    log1.debug("Main", "Iniciando depuracion");

    // Registra que el sistema ha iniciado.
    log1.info("Main", "Sistema iniciado");

    // Registra una advertencia.
    log1.warn("Main", "Carga alta detectada");

    // Registra un mensaje de error de ejemplo.
    log1.error("Main", "Ejemplo de mensaje de error");

    // Crea un objeto del servicio de matrícula.
    ServicioMatricula servicio;

    // Ejecuta la matrícula del estudiante.
    servicio.matricular("2023001", "SIS206");

    // Obtiene una segunda referencia al Singleton.
    Logger& log2 = Logger::instancia();

    // Comprueba que ambas referencias apuntan al mismo objeto.
    assert(&log1 == &log2);

    // Muestra el resultado de la comparación como true o false.
    std::cout << "\nMisma instancia: "
              << std::boolalpha
              << (&log1 == &log2)
              << std::endl;

    // Informa que la prueba de Singleton fue satisfactoria.
    std::cout << "Prueba Singleton C++ correcta."
              << std::endl;

    // Finaliza el programa correctamente.
    return 0;
}
