// ── errores_dominio.hpp — jerarquía de errores de la Tienda en Línea Local ──
#pragma once
#include <iomanip>
#include <sstream>
#include <stdexcept>
#include <string>

class ErrorTienda : public std::runtime_error {
public:
    explicit ErrorTienda(const std::string& msg) : std::runtime_error("[Tienda] " + msg) {}
    ~ErrorTienda() override = default;
};

class ErrorValidacion : public ErrorTienda {
    std::string campo_;

public:
    ErrorValidacion(std::string campo, const std::string& regla)
        : ErrorTienda("[Validación] " + campo + " inválido: " + regla), campo_(std::move(campo)) {}
    const std::string& campo() const noexcept { return campo_; }
};

class ErrorStockInsuficiente : public ErrorTienda {
    std::string codigo_;
    int disponible_, solicitado_;

public:
    ErrorStockInsuficiente(std::string codigo, int disponible, int solicitado)
        : ErrorTienda("Stock insuficiente de " + codigo + " (disponible " + std::to_string(disponible)
                      + ", solicitado " + std::to_string(solicitado) + ")"),
          codigo_(std::move(codigo)), disponible_(disponible), solicitado_(solicitado) {}
    const std::string& codigo() const noexcept { return codigo_; }
    int disponible() const noexcept { return disponible_; }
    int solicitado() const noexcept { return solicitado_; }
};

class ErrorEstadoPedido : public ErrorTienda {
    int numero_;

public:
    ErrorEstadoPedido(int numero, const std::string& estado, const std::string& operacion)
        : ErrorTienda("Pedido #" + std::to_string(numero) + ": no se puede " + operacion
                      + " en estado " + estado),
          numero_(numero) {}
    int numero() const noexcept { return numero_; }
};

class ErrorPago : public ErrorTienda {
    double monto_;

    static std::string formatear(const std::string& metodo, double monto, const std::string& motivo) {
        std::ostringstream out;
        out << "Pago rechazado por " << metodo << " (S/ " << std::fixed << std::setprecision(2)
            << monto << "): " << motivo;
        return out.str();
    }

public:
    ErrorPago(const std::string& metodo, double monto, const std::string& motivo)
        : ErrorTienda(formatear(metodo, monto, motivo)), monto_(monto) {}
    double monto() const noexcept { return monto_; }
};

class ErrorRecursoNoEncontrado : public ErrorTienda {
public:
    ErrorRecursoNoEncontrado(const std::string& tipo, const std::string& id)
        : ErrorTienda(tipo + " id=" + id + " no encontrado") {}
};
