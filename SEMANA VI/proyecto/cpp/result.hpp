// ── result.hpp — patrón Result con std::variant (C++17) ────────────────
#pragma once
#include <variant>
#include <string>
#include <stdexcept>
#include <type_traits>
#include <utility>

template<typename T> class Result;

template<typename X> struct EsResult : std::false_type {};
template<typename X> struct EsResult<Result<X>> : std::true_type {};

template<typename T>
class Result {
    struct Error { std::string mensaje; };   // tipo distinto de T aunque T sea std::string
    std::variant<T, Error> dato_;

public:
    // ── Constructores de fábrica (no se construye directamente) ─────────
    static Result ok(T valor) { return Result(std::move(valor)); }
    static Result fallo(std::string e) { return Result(Error{std::move(e)}); }

    // ── Consulta ─────────────────────────────────────────────────────────
    bool esExito() const noexcept {
        return std::holds_alternative<T>(dato_);
    }

    const T& valor() const {
        if (!esExito())
            throw std::logic_error("Result fallido: " + error());
        return std::get<T>(dato_);
    }

    const std::string& error() const {
        if (esExito())
            throw std::logic_error("Result exitoso: no tiene error");
        return std::get<Error>(dato_).mensaje;
    }

    // ── Composición (encadenamiento sin try/catch) ────────────────────────
    // Si f retorna Result<U>, se encadena directamente; si retorna U, se envuelve.
    template<typename F>
    auto map(F f) const {
        using R = std::invoke_result_t<F, const T&>;
        if constexpr (EsResult<R>::value) {
            if (esExito()) return f(valor());
            return R::fallo(error());
        } else {
            if (esExito()) return Result<R>::ok(f(valor()));
            return Result<R>::fallo(error());
        }
    }

private:
    explicit Result(T v) : dato_(std::move(v)) {}
    explicit Result(Error e) : dato_(std::move(e)) {}
};
