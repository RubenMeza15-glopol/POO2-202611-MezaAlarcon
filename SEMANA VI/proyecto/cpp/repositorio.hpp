// ── repositorio.hpp — Repositorio genérico con template C++17 ──────────
#pragma once
#include <unordered_map>
#include <vector>
#include <optional>
#include <functional>
#include <algorithm>
#include <iterator>
#include <numeric>
#include <stdexcept>

/*
 * Template: Repositorio<Entidad, TipoID>
 *
 * Ejemplo de instanciación:
 *   Repositorio<Estudiante, int>    repo([](const Estudiante& e){ return e.getCodigo(); });
 *   Repositorio<Curso, std::string> repo([](const Curso& c){ return c.getCodigo(); });
 *
 * CERO duplicación: el mismo código sirve para CUALQUIER par (Entidad, TipoID).
 */
template<typename Entidad, typename TipoID>
class Repositorio {
    // std::unordered_map: O(1) amortizado en búsqueda — ideal para repositorio
    std::unordered_map<TipoID, Entidad> datos_;
    // Función que extrae el ID de una Entidad — inyectada en el constructor
    std::function<TipoID(const Entidad&)> fn_id_;

public:
    // Constructor: recibe la función de extracción de ID (inyección de dependencia)
    explicit Repositorio(std::function<TipoID(const Entidad&)> fn)
        : fn_id_(std::move(fn)) {}

    // ── CRUD básico ──────────────────────────────────────────────────────
    void guardar(Entidad entidad) {
        TipoID id = fn_id_(entidad);
        datos_.insert_or_assign(std::move(id), std::move(entidad));
    }

    std::optional<Entidad> buscar(const TipoID& id) const {
        auto it = datos_.find(id);
        // std::optional: retorna "vacío" si no existe (no lanza)
        if (it == datos_.end()) return std::nullopt;
        return it->second;
    }

    bool eliminar(const TipoID& id) {
        return datos_.erase(id) > 0;   // retorna true si existía
    }

    // existe: usa find() — O(1) amortizado
    bool existe(const TipoID& id) const {
        return datos_.find(id) != datos_.end();
    }

    // ── CONSULTAS ────────────────────────────────────────────────────────
    std::vector<Entidad> todos() const {
        std::vector<Entidad> resultado;
        resultado.reserve(datos_.size());
        for (const auto& [id, ent] : datos_)   // structured binding C++17
            resultado.push_back(ent);
        return resultado;
    }

    // filtrar: recibe predicado (función o lambda), retorna vector filtrado
    template<typename Pred>
    std::vector<Entidad> filtrar(Pred pred) const {
        auto todos_ = todos();
        std::vector<Entidad> resultado;
        // std::copy_if: copia los elementos que satisfacen pred
        std::copy_if(todos_.begin(), todos_.end(),
                     std::back_inserter(resultado), pred);
        return resultado;
    }

    // ordenar: recibe comparador, retorna vector ordenado
    template<typename Comp>
    std::vector<Entidad> ordenar(Comp comp) const {
        auto resultado = todos();
        std::sort(resultado.begin(), resultado.end(), comp);
        return resultado;
    }

    // Estadísticas: acumulador genérico
    template<typename U, typename F>
    U acumular(U init, F f) const {
        return std::accumulate(datos_.begin(), datos_.end(), init,
            [&f](U acc, const auto& par) { return f(acc, par.second); });
    }

    // contar: cuántos elementos satisfacen pred — std::count_if
    template<typename Pred>
    std::size_t contar(Pred pred) const {
        return static_cast<std::size_t>(std::count_if(datos_.begin(), datos_.end(),
            [&pred](const auto& par) { return pred(par.second); }));
    }

    // primero: primer elemento que satisface pred — std::find_if
    template<typename Pred>
    std::optional<Entidad> primero(Pred pred) const {
        auto it = std::find_if(datos_.begin(), datos_.end(),
            [&pred](const auto& par) { return pred(par.second); });
        if (it == datos_.end()) return std::nullopt;
        return it->second;
    }

    std::size_t tamaño() const noexcept { return datos_.size(); }
    bool vacio() const noexcept { return datos_.empty(); }
};
