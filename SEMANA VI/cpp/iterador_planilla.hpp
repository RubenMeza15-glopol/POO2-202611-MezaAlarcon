// ── iterador_planilla.hpp — iterador personalizado C++17 ─────────────────
#pragma once
#include <vector>
#include <algorithm>

// Recorre el personal ordenado por remuneración (descendente)
template<typename PersonalT>
class PlanillaIterador {
    std::vector<PersonalT> ordenados_;

public:
    // Iterador sobre el vector propio: operadores *, ++ y != que usa el range-for
    class Cursor {
        typename std::vector<PersonalT>::const_iterator actual_;

    public:
        explicit Cursor(typename std::vector<PersonalT>::const_iterator it) : actual_(it) {}
        const PersonalT& operator*() const { return *actual_; }
        Cursor& operator++() { ++actual_; return *this; }
        bool operator!=(const Cursor& o) const { return actual_ != o.actual_; }
    };

    explicit PlanillaIterador(std::vector<PersonalT> personal)
        : ordenados_(std::move(personal)) {
        // Ordenar al construir — O(n log n) una sola vez
        std::sort(ordenados_.begin(), ordenados_.end(),
            [](const PersonalT& a, const PersonalT& b) {
                return a.calcularRemuneracion() > b.calcularRemuneracion();
            });
    }

    Cursor begin() const { return Cursor(ordenados_.begin()); }
    Cursor end() const { return Cursor(ordenados_.end()); }
};
