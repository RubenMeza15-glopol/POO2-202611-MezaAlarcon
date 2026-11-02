// repositorio.cpp - Repositorio generico en un solo archivo
// Compilar: g++ -std=c++17 repositorio.cpp -o repositorio.exe

#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
#include <functional>
#include <algorithm>
#include <numeric>
#include <utility>
#include <cstddef>

template<typename Entidad, typename TipoID>
class Repositorio {
private:
    std::unordered_map<TipoID, Entidad> datos_;
    std::function<TipoID(const Entidad&)> fn_id_;

public:
    explicit Repositorio(std::function<TipoID(const Entidad&)> fn)
        : fn_id_(std::move(fn)) {}

    void guardar(Entidad entidad) {
        datos_[fn_id_(entidad)] = std::move(entidad);
    }

    // Devuelve true si encuentra el registro y copia el resultado.
    // Esta version no usa std::optional.
    bool buscar(const TipoID& id, Entidad& resultado) const {
        auto it = datos_.find(id);
        if (it == datos_.end()) return false;
        resultado = it->second;
        return true;
    }

    bool eliminar(const TipoID& id) {
        return datos_.erase(id) > 0;
    }

    std::vector<Entidad> todos() const {
        std::vector<Entidad> resultado;
        resultado.reserve(datos_.size());
        for (const auto& par : datos_) {
            resultado.push_back(par.second);
        }
        return resultado;
    }

    template<typename Pred>
    std::vector<Entidad> filtrar(Pred pred) const {
        std::vector<Entidad> resultado;
        for (const auto& par : datos_) {
            if (pred(par.second)) resultado.push_back(par.second);
        }
        return resultado;
    }

    template<typename Comp>
    std::vector<Entidad> ordenar(Comp comp) const {
        std::vector<Entidad> resultado = todos();
        std::sort(resultado.begin(), resultado.end(), comp);
        return resultado;
    }

    template<typename U, typename F>
    U acumular(U inicial, F funcion) const {
        U resultado = inicial;
        for (const auto& par : datos_) {
            resultado = funcion(resultado, par.second);
        }
        return resultado;
    }

    std::size_t tamano() const noexcept { return datos_.size(); }
    bool vacio() const noexcept { return datos_.empty(); }
};

struct Estudiante {
    int codigo;
    std::string nombre;
    float ppa;
    std::string escuela;
};

struct Curso {
    std::string codigo;
    std::string nombre;
    int creditos;
};

int main() {
    Repositorio<Estudiante, int> estudiantes(
        [](const Estudiante& e) { return e.codigo; }
    );

    estudiantes.guardar({1001, "Juan Carlos Mamani", 15.2f, "Ing. Sistemas"});
    estudiantes.guardar({1002, "Maria Elena Quispe", 18.5f, "Ing. Sistemas"});
    estudiantes.guardar({1003, "Pedro Flores", 9.8f, "Ciencias Comp."});

    Estudiante encontrado{};
    if (estudiantes.buscar(1002, encontrado)) {
        std::cout << "Encontrado: " << encontrado.nombre << "\n";
    }

    auto destacados = estudiantes.filtrar(
        [](const Estudiante& e) { return e.ppa >= 14.0f; }
    );
    std::cout << "Destacados: " << destacados.size() << "\n";

    auto ranking = estudiantes.ordenar(
        [](const Estudiante& a, const Estudiante& b) {
            return a.ppa > b.ppa;
        }
    );

    std::cout << "\nRanking por PPA:\n";
    int posicion = 1;
    for (const auto& e : ranking) {
        std::cout << posicion++ << ". " << e.nombre
                  << " - " << e.ppa << "\n";
    }

    float suma = estudiantes.acumular(
        0.0f, [](float acumulado, const Estudiante& e) {
            return acumulado + e.ppa;
        }
    );
    if (!estudiantes.vacio()) {
        std::cout << "PPA promedio: "
                  << suma / static_cast<float>(estudiantes.tamano()) << "\n";
    }

    Repositorio<Curso, std::string> cursos(
        [](const Curso& c) { return c.codigo; }
    );
    cursos.guardar({"SIS206", "Programacion Orientada a Objetos II", 4});
    cursos.guardar({"MAT101", "Matematica", 3});

    std::cout << "\nCursos registrados: " << cursos.tamano() << "\n";
    Curso curso{};
    if (cursos.buscar("SIS206", curso)) {
        std::cout << "Curso encontrado: " << curso.nombre << "\n";
    }

    return 0;
}
