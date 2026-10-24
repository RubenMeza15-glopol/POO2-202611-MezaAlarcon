    #include <iostream>   // Permite mostrar información en pantalla.
    #include <string>     // Permite utilizar el tipo string.
    #include <stdexcept>  // Permite lanzar excepciones con invalid_argument.

    using namespace std;  // Evita escribir std:: antes de cada elemento.

    // ==================================================
    // CLASE ESTUDIANTE
    // ==================================================

    class Estudiante {
    private:
        int codigo_;       // Código privado del estudiante.
        string nombre_;    // Nombre privado del estudiante.
        string apellido_;  // Apellido privado del estudiante.

    public:
        // Constructor: inicializa los datos del estudiante.
        Estudiante(int codigo, string nombre, string apellido) {
            setCodigo(codigo);          // Valida y guarda el código.
            setNombre(nombre);          // Valida y guarda el nombre.
            setApellido(apellido);      // Valida y guarda el apellido.
        }

        // Getter: devuelve el código sin modificar el objeto.
        int getCodigo() const {
            return codigo_;
        }

        // Setter: valida que el código sea positivo.
        void setCodigo(int valor) {
            if (valor <= 0)
                throw invalid_argument("El codigo debe ser positivo");

            codigo_ = valor;  // Guarda el código válido.
        }

        // Getter: devuelve el nombre.
        string getNombre() const {
            return nombre_;
        }

        // Setter: valida que el nombre no esté vacío.
        void setNombre(string valor) {
            if (valor.empty() || valor.find_first_not_of(' ') == string::npos)
                throw invalid_argument("El nombre no puede estar vacio");

            nombre_ = valor;  // Guarda el nombre válido.
        }

        // Getter: devuelve el apellido.
        string getApellido() const {
            return apellido_;
        }

        // Setter: valida que el apellido no esté vacío.
        void setApellido(string valor) {
            if (valor.empty() || valor.find_first_not_of(' ') == string::npos)
                throw invalid_argument("El apellido no puede estar vacio");

            apellido_ = valor;  // Guarda el apellido válido.
        }
    };

    // ==================================================
    // CLASE CURSO
    // ==================================================

    class Curso {
    private:
        string codigo_;       // Código privado del curso.
        string nombre_;       // Nombre privado del curso.
        int credito_;         // Créditos del curso.
        int ciclo_;           // Ciclo académico.
        string descripcion_;  // Descripción del curso.

    public:
        // Constructor: inicializa y valida los datos del curso.
        Curso(string codigo, string nombre, int credito,
            int ciclo, string descripcion) {
            setCodigo(codigo);              // Valida el código.
            setNombre(nombre);              // Valida el nombre.
            setCredito(credito);            // Valida los créditos.
            setCiclo(ciclo);                // Valida el ciclo.
            setDescripcion(descripcion);    // Valida la descripción.
        }

        // Getter: devuelve el código.
        string getCodigo() const {
            return codigo_;
        }

        // Setter: evita que el código esté vacío.
        void setCodigo(string valor) {
            if (valor.empty() || valor.find_first_not_of(' ') == string::npos)
                throw invalid_argument("El codigo no puede estar vacio");

            codigo_ = valor;  // Guarda el código válido.
        }

        // Getter: devuelve el nombre.
        string getNombre() const {
            return nombre_;
        }

        // Setter: valida el nombre.
        void setNombre(string valor) {
            if (valor.empty() || valor.find_first_not_of(' ') == string::npos)
                throw invalid_argument("El nombre no puede estar vacio");

            nombre_ = valor;  // Guarda el nombre válido.
        }

        // Getter: devuelve los créditos.
        int getCredito() const {
            return credito_;
        }

        // Setter: permite de 1 a 6 créditos.
        void setCredito(int valor) {
            if (valor < 1 || valor > 6)
                throw invalid_argument("Los creditos deben estar entre 1 y 6");

            credito_ = valor;  // Guarda los créditos válidos.
        }

        // Getter: devuelve el ciclo.
        int getCiclo() const {
            return ciclo_;
        }

        // Setter: valida que el ciclo sea positivo.
        void setCiclo(int valor) {
            if (valor < 1)
                throw invalid_argument("El ciclo debe ser positivo");

            ciclo_ = valor;  // Guarda el ciclo válido.
        }

        // Getter: devuelve la descripción.
        string getDescripcion() const {
            return descripcion_;
        }

        // Setter: valida que la descripción no esté vacía.
        void setDescripcion(string valor) {
            if (valor.empty() || valor.find_first_not_of(' ') == string::npos)
                throw invalid_argument("La descripcion no puede estar vacia");

            descripcion_ = valor;  // Guarda la descripción válida.
        }
    };

    // ==================================================
    // CLASE NOTA
    // ==================================================

    class Nota {
    private:
        string curso_;       // Curso asociado a la nota.
        float calificacion_; // Calificación del estudiante.

    public:
        // Constructor: inicializa y valida los datos de la nota.
        Nota(string curso, float calificacion) {
            setCurso(curso);                  // Valida el curso.
            setCalificacion(calificacion);    // Valida la calificación.
        }

        // Getter: devuelve el curso asociado.
        string getCurso() const {
            return curso_;
        }

        // Setter: valida que el curso no esté vacío.
        void setCurso(string valor) {
            if (valor.empty() || valor.find_first_not_of(' ') == string::npos)
                throw invalid_argument("El curso no puede estar vacio");

            curso_ = valor;  // Guarda el curso válido.
        }

        // Getter: devuelve la calificación.
        float getCalificacion() const {
            return calificacion_;
        }

        // Setter: acepta calificaciones entre 0 y 20.
        void setCalificacion(float valor) {
            if (valor < 0 || valor > 20)
                throw invalid_argument("La nota debe estar entre 0 y 20");

            calificacion_ = valor;  // Guarda la calificación válida.
        }
    };

    // ==================================================
    // PROGRAMA PRINCIPAL
    // ==================================================

    int main() {
        try {
            // Crea un estudiante.
            Estudiante est(20261101, "Juan", "Mamani");

            // Crea un curso.
            Curso cur("SIS206", "POO II", 4, 2,
                    "Programacion orientada a objetos");

            // Crea una nota asociada al curso.
            Nota nota("POO II", 16.0f);

            // Muestra los datos del estudiante.
            cout << "ESTUDIANTE" << endl;
            cout << "Codigo: " << est.getCodigo() << endl;
            cout << "Nombre: " << est.getNombre() << endl;
            cout << "Apellido: " << est.getApellido() << endl;

            // Muestra los datos del curso.
            cout << "\nCURSO" << endl;
            cout << "Codigo: " << cur.getCodigo() << endl;
            cout << "Nombre: " << cur.getNombre() << endl;
            cout << "Creditos: " << cur.getCredito() << endl;
            cout << "Ciclo: " << cur.getCiclo() << endl;
            cout << "Descripcion: " << cur.getDescripcion() << endl;

            // Muestra los datos de la nota.
            cout << "\nNOTA" << endl;
            cout << "Curso: " << nota.getCurso() << endl;
            cout << "Calificacion: " << nota.getCalificacion() << endl;

        } catch (const invalid_argument& error) {
            // Captura y muestra cualquier error de validación.
            cout << "Error: " << error.what() << endl;
        }

        return 0;  // Finaliza el programa correctamente.
    }
