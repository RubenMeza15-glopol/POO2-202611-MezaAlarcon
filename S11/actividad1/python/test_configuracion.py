
# Importa la clase que vamos a probar.
from configuracion import ConfiguracionApp


# Comprueba que las dos llamadas devuelven el mismo objeto.
def test_misma_instancia():

    # Crea la primera referencia.
    config1 = ConfiguracionApp()

    # Crea la segunda referencia.
    config2 = ConfiguracionApp()

    # Comprueba que ambas referencias son el mismo objeto.
    assert config1 is config2


# Comprueba que los parámetros se cargaron correctamente.
def test_carga_configuracion():

    # Obtiene la instancia Singleton.
    config = ConfiguracionApp()

    # Verifica la dirección de la base de datos.
    assert config.obtener("DB_URL") == "sqlite:///app.db"

    # Verifica el máximo de conexiones.
    assert config.obtener("MAX_CONEXIONES") == "10"

    # Verifica el modo de depuración.
    assert config.obtener("DEBUG") == "True"

    # Verifica el nombre de la aplicación.
    assert config.obtener("APP_NAME") == "Sistema Academico UNAP"


# Comprueba que las referencias comparten los mismos parámetros.
def test_mismo_contenido():

    # Obtiene la primera referencia.
    config1 = ConfiguracionApp()

    # Obtiene la segunda referencia.
    config2 = ConfiguracionApp()

    # Comprueba que ambos diccionarios contienen los mismos datos.
    assert config1.parametros == config2.parametros
