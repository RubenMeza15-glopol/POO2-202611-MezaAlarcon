
#include <iostream>  // Permite mostrar información en la terminal.
#include <memory>    // Permite utilizar punteros inteligentes.
#include <string>    // Permite trabajar con cadenas de texto.

// Permite utilizar los elementos de la biblioteca estándar.
using namespace std;

// ======================================================
// PRODUCTO ABSTRACTO 1: VENTANA PRINCIPAL
// ======================================================

// Define la interfaz común para todas las ventanas.
class VentanaPrincipal {
public:

    // Destructor virtual para permitir la destrucción correcta.
    virtual ~VentanaPrincipal() = default;

    // Método abstracto que cada familia debe implementar.
    virtual void mostrar() const = 0;
};

// ======================================================
// PRODUCTO ABSTRACTO 2: MENÚ DE NAVEGACIÓN
// ======================================================

// Define la interfaz común de los menús.
class MenuNavegacion {
public:

    // Destructor virtual.
    virtual ~MenuNavegacion() = default;

    // Cada familia implementará su propio menú.
    virtual void mostrar() const = 0;
};

// ======================================================
// PRODUCTO ABSTRACTO 3: TABLA DE RESULTADOS
// ======================================================

// Define la interfaz común de las tablas.
class TablaResultados {
public:

    // Destructor virtual.
    virtual ~TablaResultados() = default;

    // Cada familia implementará su propia tabla.
    virtual void mostrar() const = 0;
};

// ======================================================
// FAMILIA 1: COMPONENTES ESTILO TKINTER
// ======================================================

// Implementa una ventana de la familia Tkinter.
class VentanaTkinter : public VentanaPrincipal {
public:
    // Muestra el nombre de la ventana Tkinter.
    void mostrar() const override {
        cout << "[Tkinter] Ventana principal mostrada.\n";
    }
};

// Implementa un menú de la familia Tkinter.
class MenuTkinter : public MenuNavegacion {
public:
    // Muestra el menú Tkinter.
    void mostrar() const override {
        cout << "[Tkinter] Menu de navegacion mostrado.\n";
    }
};

// Implementa una tabla de la familia Tkinter.
class TablaTkinter : public TablaResultados {
public:
    // Muestra la tabla Tkinter.
    void mostrar() const override {
        cout << "[Tkinter] Tabla de resultados mostrada.\n";
    }
};

// ======================================================
// FAMILIA 2: COMPONENTES ESTILO PYQT5
// ======================================================

// Implementa una ventana de la familia PyQt5.
class VentanaPyQt5 : public VentanaPrincipal {
public:
    // Muestra el nombre de la ventana PyQt5.
    void mostrar() const override {
        cout << "[PyQt5] Ventana principal mostrada.\n";
    }
};

// Implementa un menú de la familia PyQt5.
class MenuPyQt5 : public MenuNavegacion {
public:
    // Muestra el menú PyQt5.
    void mostrar() const override {
        cout << "[PyQt5] Menu de navegacion mostrado.\n";
    }
};

// Implementa una tabla de la familia PyQt5.
class TablaPyQt5 : public TablaResultados {
public:
    // Muestra la tabla PyQt5.
    void mostrar() const override {
        cout << "[PyQt5] Tabla de resultados mostrada.\n";
    }
};

// ======================================================
// FABRICA ABSTRACTA: UIFactory
// ======================================================

// Define el contrato para crear familias de componentes.
class UIFactory {
public:

    // Destructor virtual de la fabrica.
    virtual ~UIFactory() = default;

    // Metodo abstracto para crear una ventana.
    [[nodiscard]]
    virtual unique_ptr<VentanaPrincipal> crearVentana() const = 0;

    // Metodo abstracto para crear un menu.
    [[nodiscard]]
    virtual unique_ptr<MenuNavegacion> crearMenu() const = 0;

    // Metodo abstracto para crear una tabla.
    [[nodiscard]]
    virtual unique_ptr<TablaResultados> crearTabla() const = 0;

    // Devuelve el nombre de la familia de componentes.
    [[nodiscard]]
    virtual string nombre() const = 0;
};

// ======================================================
// FABRICA CONCRETA 1: TKINTER
// ======================================================

// Fabrica encargada de crear componentes de la familia Tkinter.
class UIFactoryTkinter : public UIFactory {
public:

    // Crea y devuelve una ventana Tkinter.
    unique_ptr<VentanaPrincipal> crearVentana() const override {
        return make_unique<VentanaTkinter>();
    }

    // Crea y devuelve un menu Tkinter.
    unique_ptr<MenuNavegacion> crearMenu() const override {
        return make_unique<MenuTkinter>();
    }

    // Crea y devuelve una tabla Tkinter.
    unique_ptr<TablaResultados> crearTabla() const override {
        return make_unique<TablaTkinter>();
    }

    // Identifica la familia utilizada.
    string nombre() const override {
        return "Tkinter";
    }
};

// ======================================================
// FABRICA CONCRETA 2: PYQT5
// ======================================================

// Fabrica encargada de crear componentes de la familia PyQt5.
class UIFactoryPyQt5 : public UIFactory {
public:

    // Crea y devuelve una ventana PyQt5.
    unique_ptr<VentanaPrincipal> crearVentana() const override {
        return make_unique<VentanaPyQt5>();
    }

    // Crea y devuelve un menu PyQt5.
    unique_ptr<MenuNavegacion> crearMenu() const override {
        return make_unique<MenuPyQt5>();
    }

    // Crea y devuelve una tabla PyQt5.
    unique_ptr<TablaResultados> crearTabla() const override {
        return make_unique<TablaPyQt5>();
    }

    // Identifica la familia utilizada.
    string nombre() const override {
        return "PyQt5";
    }
};

// ======================================================
// CLIENTE: FORMULARIO DE BUSQUEDA
// ======================================================

// El formulario trabaja con la fabrica abstracta.
// No necesita conocer las clases concretas.
class FormularioBusqueda {
private:

    // Puntero a la ventana que proporciona la fabrica.
    unique_ptr<VentanaPrincipal> ventana_;

    // Puntero al menu que proporciona la fabrica.
    unique_ptr<MenuNavegacion> menu_;

    // Puntero a la tabla que proporciona la fabrica.
    unique_ptr<TablaResultados> tabla_;

    // Guarda el nombre de la familia seleccionada.
    string familia_;

public:

    // Constructor que recibe una fabrica mediante inyeccion.
    explicit FormularioBusqueda(const UIFactory& fabrica) {

        // Obtiene la ventana de la familia seleccionada.
        ventana_ = fabrica.crearVentana();

        // Obtiene el menu de la misma familia.
        menu_ = fabrica.crearMenu();

        // Obtiene la tabla de la misma familia.
        tabla_ = fabrica.crearTabla();

        // Guarda el nombre de la familia utilizada.
        familia_ = fabrica.nombre();
    }

    // Muestra todos los componentes del formulario.
    void mostrar() const {

        // Informa qué familia de componentes se está utilizando.
        cout << "\nFamilia seleccionada: " << familia_ << "\n";

        // Muestra la ventana.
        ventana_->mostrar();

        // Muestra el menu de navegacion.
        menu_->mostrar();

        // Muestra la tabla de resultados.
        tabla_->mostrar();
    }
};


// ======================================================
// FUNCION PRINCIPAL: MAIN
// ======================================================

// Punto de entrada del programa.
int main() {

    // Muestra el titulo de la actividad.
    cout << "====================================\n";
    cout << "   ABSTRACT FACTORY - UI ACADEMICA\n";
    cout << "====================================\n";

    // --------------------------------------------------
    // PRUEBA 1: FAMILIA TKINTER
    // --------------------------------------------------

    // Crea la fabrica concreta Tkinter.
    UIFactoryTkinter fabricaTkinter;

    // Crea el formulario utilizando la fabrica Tkinter.
    FormularioBusqueda formularioTkinter(fabricaTkinter);

    // Muestra los componentes de la familia Tkinter.
    formularioTkinter.mostrar();

    // --------------------------------------------------
    // PRUEBA 2: FAMILIA PYQT5
    // --------------------------------------------------

    // Crea la fabrica concreta PyQt5.
    UIFactoryPyQt5 fabricaPyQt5;

    // Crea el formulario utilizando la fabrica PyQt5.
    FormularioBusqueda formularioPyQt5(fabricaPyQt5);

    // Muestra los componentes de la familia PyQt5.
    formularioPyQt5.mostrar();

    // --------------------------------------------------
    // FINALIZACION DEL PROGRAMA
    // --------------------------------------------------

    // Informa que ambas pruebas terminaron.
    cout << "\n====================================\n";
    cout << "   PRUEBAS FINALIZADAS CORRECTAMENTE\n";
    cout << "====================================\n";

    // Devuelve cero para indicar ejecucion correcta.
    return 0;
}
