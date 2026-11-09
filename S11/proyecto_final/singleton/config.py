# Importa os para leer variables de entorno.
import os

# Importa threading para proteger la creación.
import threading

# Define la clase de configuración.
class Config:

    # Guarda la instancia única.
    _instancia = None

    # Crea un bloqueo para controlar la concurrencia.
    _bloqueo = threading.Lock()

    # Controla la creación del objeto.
    def __new__(cls):

        # Comprueba si todavía no existe.
        if cls._instancia is None:

            # Bloquea el acceso durante la creación.
            with cls._bloqueo:

                # Comprueba nuevamente.
                if cls._instancia is None:

                    # Crea la instancia.
                    cls._instancia = super().__new__(cls)

                    # Indica que todavía no se cargó la configuración.
                    cls._instancia._cargada = False

        # Devuelve la misma instancia.
        return cls._instancia

    # Inicializa la configuración una sola vez.
    def __init__(self):

        # Evita cargar el archivo repetidamente.
        if self._cargada:
            return

        # Define la ruta del archivo de configuración.
        ruta = os.path.join(
            os.path.dirname(__file__),
            "..",
            "archivo.env"
        )

        # Abre el archivo de configuración.
        with open(ruta, "r", encoding="utf-8") as archivo:

            # Lee cada línea del archivo.
            for linea in archivo:

                # Elimina espacios y saltos de línea.
                linea = linea.strip()

                # Ignora líneas vacías y comentarios.
                if not linea or linea.startswith("#"):
                    continue

                # Separa el nombre y el valor.
                clave, valor = linea.split("=", 1)

                # Guarda el valor como variable de entorno.
                os.environ[clave.strip()] = valor.strip()

        # Marca la configuración como cargada.
        self._cargada = True

    # Obtiene un parámetro de configuración.
    def obtener(self, clave, defecto=None):

        # Devuelve el valor o el valor predeterminado.
        return os.getenv(clave, defecto)