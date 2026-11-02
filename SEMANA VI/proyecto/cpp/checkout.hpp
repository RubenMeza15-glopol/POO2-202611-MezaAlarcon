// Proyecto Integrador — Tienda en Línea Local — Semana 6: checkout (base de la Semana 5)
#pragma once
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

#include "tienda.hpp"

// ── Interfaces puras ─────────────────────────────────────────────────────
class IMetodoPago {
public:
    virtual ~IMetodoPago() = default;
    virtual bool procesarPago(double monto, const std::string& referencia) = 0;
    virtual bool esDisponible(double monto) const = 0;
    virtual std::string nombre() const = 0;
};

class INotificador {
public:
    virtual ~INotificador() = default;
    virtual bool notificar(const std::string& destinatario, const std::string& mensaje) = 0;
    virtual std::string canal() const = 0;
};

// ── Implementaciones concretas ───────────────────────────────────────────
class PagoTarjeta : public IMetodoPago {
    std::string ultimos_;
    double limite_;

public:
    PagoTarjeta(std::string ultimos, double limite) : ultimos_(std::move(ultimos)), limite_(limite) {}
    std::string nombre() const override { return "Tarjeta ****" + ultimos_; }
    bool esDisponible(double monto) const override { return monto <= limite_; }
    bool procesarPago(double monto, const std::string& referencia) override {
        std::cout << "[TARJETA ****" << ultimos_ << "] Cobro S/ " << std::fixed << std::setprecision(2)
                  << monto << " — ref " << referencia << "\n";
        limite_ -= monto;
        return true;
    }
};

class PagoYape : public IMetodoPago {
    std::string celular_;
    static constexpr double LIMITE_DIARIO = 500.0;

public:
    explicit PagoYape(std::string celular) : celular_(std::move(celular)) {}
    std::string nombre() const override { return "Yape (" + celular_ + ")"; }
    bool esDisponible(double monto) const override { return monto <= LIMITE_DIARIO; }
    bool procesarPago(double monto, const std::string& referencia) override {
        std::cout << "[YAPE " << celular_ << "] Pago S/ " << std::fixed << std::setprecision(2)
                  << monto << " — ref " << referencia << "\n";
        return true;
    }
};

class PagoContraEntrega : public IMetodoPago {
public:
    std::string nombre() const override { return "Contra entrega"; }
    bool esDisponible(double) const override { return true; }
    bool procesarPago(double monto, const std::string& referencia) override {
        std::cout << "[CONTRA ENTREGA] Se cobrará S/ " << std::fixed << std::setprecision(2)
                  << monto << " al entregar — ref " << referencia << "\n";
        return true;
    }
};

class NotificadorEmail : public INotificador {
public:
    std::string canal() const override { return "Email"; }
    bool notificar(const std::string& destinatario, const std::string& mensaje) override {
        std::cout << "[EMAIL → " << destinatario << "]: " << mensaje << "\n";
        return true;
    }
};

class NotificadorWhatsApp : public INotificador {
public:
    std::string canal() const override { return "WhatsApp"; }
    bool notificar(const std::string& destinatario, const std::string& mensaje) override {
        std::cout << "[WHATSAPP → " << destinatario << "]: " << mensaje << "\n";
        return true;
    }
};

// ── Consumidor: recibe sus dependencias por constructor (DI) ─────────────
class ServicioCheckout {
    IMetodoPago* metodoPago_;
    INotificador& notificador_;

public:
    ServicioCheckout(IMetodoPago& metodoPago, INotificador& notificador)
        : metodoPago_(&metodoPago), notificador_(notificador) {}

    void cambiarMetodoPago(IMetodoPago& metodo) { metodoPago_ = &metodo; }

    bool procesar(Pedido& pedido) {
        // PRECONDICIÓN
        if (pedido.cantidadArticulos() == 0) throw ErrorValidacion("pedido", "no tiene productos");
        double monto = pedido.total();
        std::string referencia = "PED-" + std::to_string(pedido.getNumero());
        std::ostringstream msg;
        msg << "Pedido #" << pedido.getNumero();
        if (!metodoPago_->esDisponible(monto)) {
            msg << ": " << metodoPago_->nombre() << " no disponible para S/ " << std::fixed
                << std::setprecision(2) << monto;
            notificador_.notificar(pedido.getCliente().getCorreo(), msg.str());
            throw ErrorPago(metodoPago_->nombre(), monto, "monto excede el límite");
        }
        if (!metodoPago_->procesarPago(monto, referencia))
            throw ErrorPago(metodoPago_->nombre(), monto, "operación rechazada");
        pedido.confirmarPago();
        // POSCONDICIÓN
        assert(pedido.getEstado() == Pedido::Estado::Pagado && "POST: pedido no quedó pagado");
        msg << " pagado con " << metodoPago_->nombre() << ": S/ " << std::fixed
            << std::setprecision(2) << monto;
        notificador_.notificar(pedido.getCliente().getCorreo(), msg.str());
        return true;
    }
};
