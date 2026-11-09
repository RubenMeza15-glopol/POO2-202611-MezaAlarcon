
# Importa Lock para proteger la creación de la instancia.
from threading import Lock

# Importa Path para trabajar con rutas de archivos.
from pathlib import Path

# Importa Any para indicar tipos de datos generales.
from typing import Any


# Define la metaclase que controla la creación de instancias.
class SingletonMeta(type):

    # Diccionario que almacena una instancia por cada clase.
    _instancias: dict[type, Any] = {}

    # Bloqueo para evitar crear instancias simultáneamente.
    _lock = Lock()

    # Método especial que controla la creación de objetos.
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:

        # Bloquea el acceso mientras se verifica la instancia.
        with cls._lock:

            # Comprueba si todavía no existe una instancia.
            if cls not in cls._instancias:

                # Crea la instancia y la guarda en el diccionario.
                cls._instancias[cls] = super().__call__(
                    *args, **kwargs
                )

        # Devuelve siempre la misma instancia.
        return cls._instancias[cls]


# Define la clase de configuración de la aplicación.
class ConfiguracionApp(metaclass=SingletonMeta):

    # Constructor que recibe el nombre del archivo de configuración.
    def __init__(self, ruta: str = "archivo.env"):

        # Obtiene la carpeta donde se encuentra este archivo Python.
        carpeta_actual = Path(__file__).resolve().parent

        # Construye la ruta completa del archivo archivo.env.
        ruta_completa = carpeta_actual / ruta

        # Crea un diccionario vacío para guardar los parámetros.
        self.parametros = {}

        # Abre el archivo de configuración para leer sus datos.
        with open(ruta_completa, "r", encoding="utf-8") as archivo:

            # Recorre todas las líneas del archivo.
            for linea in archivo:

                # Elimina espacios y saltos de línea.
                linea = linea.strip()

                # Ignora las líneas vacías y los comentarios.
                if not linea or linea.startswith("#"):
                    continue

                # Separa la clave y el valor utilizando el primer igual.
                clave, valor = linea.split("=", 1)

                # Guarda la clave y el valor en el diccionario.
                self.parametros[clave.strip()] = valor.strip()

    # Método que permite consultar un parámetro.
    def obtener(self, clave: str, defecto: str = "") -> str:

        # Devuelve el valor encontrado o el valor por defecto.
        return self.parametros.get(clave, defecto)


# Comprueba si el archivo se está ejecutando directamente.
if __name__ == "__main__":

    # Crea la primera referencia a la configuración.
    config1 = ConfiguracionApp()

    # Crea una segunda referencia a la configuración.
    config2 = ConfiguracionApp()

    # Muestra la dirección de la base de datos.
    print("URL de base de datos:", config1.obtener("DB_URL"))

    # Muestra el máximo de conexiones.
    print("Máximo de conexiones:", config1.obtener("MAX_CONEXIONES"))

    # Muestra el modo de depuración.
    print("Modo DEBUG:", config1.obtener("DEBUG"))

    # Muestra el nombre de la aplicación.
    print("Nombre de aplicación:", config1.obtener("APP_NAME"))

    # Comprueba que ambas referencias apuntan al mismo objeto.
    assert config1 is config2

    # Muestra el resultado de la comprobación.
    print("Misma instancia:", config1 is config2)

    # Confirma que la prueba Singleton fue correcta.
    print("Prueba Singleton Python correcta.")
