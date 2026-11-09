# Importa Mock para simular objetos.
from unittest.mock import Mock

# Importa la fábrica Tkinter.
from ui_factory.tkinter_factory import UIFactoryTkinter

# Importa los componentes concretos Tkinter.
from ui_factory.tkinter_factory import (
    VentanaTkinter,
    MenuTkinter,
    TablaTkinter
)

# Importa la fábrica PyQt5.
from ui_factory.pyqt5_factory import UIFactoryPyQt5

# Importa los componentes concretos PyQt5.
from ui_factory.pyqt5_factory import (
    VentanaPyQt5,
    MenuPyQt5,
    TablaPyQt5
)


# Comprueba la familia de componentes Tkinter.
def test_familia_tkinter():

    # Crea la fábrica Tkinter.
    fabrica = UIFactoryTkinter()

    # Comprueba el tipo de ventana.
    assert isinstance(fabrica.crear_ventana(), VentanaTkinter)

    # Comprueba el tipo de menú.
    assert isinstance(fabrica.crear_menu(), MenuTkinter)

    # Comprueba el tipo de tabla.
    assert isinstance(fabrica.crear_tabla(), TablaTkinter)


# Comprueba la familia de componentes PyQt5.
def test_familia_pyqt5():

    # Crea la fábrica PyQt5.
    fabrica = UIFactoryPyQt5()

    # Comprueba el tipo de ventana.
    assert isinstance(fabrica.crear_ventana(), VentanaPyQt5)

    # Comprueba el tipo de menú.
    assert isinstance(fabrica.crear_menu(), MenuPyQt5)

    # Comprueba el tipo de tabla.
    assert isinstance(fabrica.crear_tabla(), TablaPyQt5)


# Comprueba una fábrica utilizando Mock.
def test_fabrica_con_mock():

    # Crea una fábrica simulada con la interfaz de Tkinter.
    fabrica = Mock(spec=UIFactoryTkinter)

    # Configura la respuesta simulada del método crear_ventana.
    fabrica.crear_ventana.return_value = VentanaTkinter()

    # Solicita una ventana a la fábrica simulada.
    ventana = fabrica.crear_ventana()

    # Comprueba que se recibió una ventana Tkinter.
    assert isinstance(ventana, VentanaTkinter)

    # Comprueba que el método se llamó exactamente una vez.
    fabrica.crear_ventana.assert_called_once()