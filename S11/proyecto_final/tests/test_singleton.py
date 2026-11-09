# Importa Logger desde el módulo Singleton.
from singleton.logger import Logger

# Importa Config desde el módulo Singleton.
from singleton.config import Config


# Comprueba que Logger devuelve siempre el mismo objeto.
def test_logger_misma_instancia():

    # Crea la primera instancia.
    logger1 = Logger()

    # Solicita una segunda instancia.
    logger2 = Logger()

    # Comprueba que ambas referencias apuntan al mismo objeto.
    assert logger1 is logger2


# Comprueba que Config devuelve siempre el mismo objeto.
def test_config_misma_instancia():

    # Crea la primera instancia.
    config1 = Config()

    # Solicita una segunda instancia.
    config2 = Config()

    # Comprueba que ambas referencias apuntan al mismo objeto.
    assert config1 is config2