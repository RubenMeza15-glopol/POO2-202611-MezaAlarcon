# Importa threading para controlar el acceso entre hilos.
import threading

# Define la clase Logger.
class Logger:

    # Guarda la única instancia de la clase.
    _instancia = None

    # Crea un bloqueo para evitar instancias duplicadas.
    _bloqueo = threading.Lock()

    # Método especial para controlar la creación del objeto.
    def __new__(cls):

        # Comprueba si todavía no existe una instancia.
        if cls._instancia is None:

            # Bloquea temporalmente el acceso concurrente.
            with cls._bloqueo:

                # Comprueba nuevamente después de adquirir el bloqueo.
                if cls._instancia is None:

                    # Crea la única instancia de Logger.
                    cls._instancia = super().__new__(cls)

        # Devuelve siempre la misma instancia.
        return cls._instancia

    # Método que registra mensajes.
    def info(self, modulo, mensaje):

        # Muestra el mensaje informativo.
        print(f"[INFO] [{modulo}] {mensaje}")

    # Método que registra advertencias.
    def warn(self, modulo, mensaje):

        # Muestra la advertencia.
        print(f"[WARN] [{modulo}] {mensaje}")

    # Método que registra errores.
    def error(self, modulo, mensaje):

        # Muestra el error.
        print(f"[ERROR] [{modulo}] {mensaje}")