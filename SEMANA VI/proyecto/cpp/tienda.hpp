// Proyecto Integrador — Tienda en Línea Local — Semana 6: entidades (base de la Semana 5) (C++17)
#pragma once
#include <algorithm>
#include <cassert>
#include <iomanip>
#include <iostream>
#include <map>
#include <memory>
#include <numeric>
#include <regex>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

#include "errores_dominio.hpp"

class Producto {
    /*
     * INVARIANTE: codigo_ con formato PRD-0000, !nombre_.empty(), precio_ > 0, stock_ >= 0
     */
    std::string codigo_;
    std::string nombre_;
    double precio_ = 0;
    int stock_ = 0;

protected:
    void verificarInvariante() const {
        assert(std::regex_match(codigo_, std::regex("^PRD-[0-9]{4}$")) && "INV: código");
        assert(!nombre_.empty() && "INV: nombre vacío");
        assert(precio_ > 0 && "INV: precio");
        assert(stock_ >= 0 && "INV: stock negativo");
    }

public:
    Producto(const std::string& codigo, std::string nombre, double precio, int stock) {
        // PRECONDICIONES
        static const std::regex patron("^PRD-[0-9]{4}$");
        if (!std::regex_match(codigo, patron)) throw ErrorValidacion("código", "formato PRD-0000");
        codigo_ = codigo;
        setNombre(std::move(nombre));
        setPrecio(precio);
        setStock(stock);
        verificarInvariante();   // POST-constructor
    }

    virtual ~Producto() = default;

    void setNombre(std::string n) {
        if (n.empty()) throw ErrorValidacion("nombre", "no puede estar vacío");
        nombre_ = std::move(n);
    }
    void setPrecio(double p) {
        if (p <= 0) throw ErrorValidacion("precio", "debe ser mayor que 0");
        precio_ = p;
    }
    void setStock(int s) {
        if (s < 0) throw ErrorValidacion("stock", "no puede ser negativo");
        stock_ = s;
    }

    const std::string& getCodigo() const noexcept { return codigo_; }
    const std::string& getNombre() const noexcept { return nombre_; }
    double getPrecio() const noexcept { return precio_; }
    int getStock() const noexcept { return stock_; }
    double valorInventario() const noexcept { return precio_ * stock_; }

    void reducirStock(int cantidad) {
        // PRECONDICIONES
        if (cantidad <= 0) throw ErrorValidacion("cantidad", "debe ser mayor que 0");
        if (cantidad > stock_) throw ErrorStockInsuficiente(codigo_, stock_, cantidad);
        const int anterior = stock_;
        stock_ -= cantidad;
        // POSCONDICIÓN
        assert(stock_ == anterior - cantidad && "POST: stock mal descontado");
        (void)anterior;
        verificarInvariante();
    }

    virtual double calcularCostoEnvio(int cantidad) const = 0;
    virtual std::string descripcion() const { return nombre_; }

    double costoTotal(int cantidad) const { return precio_ * cantidad + calcularCostoEnvio(cantidad); }

    std::string toString() const {
        std::ostringstream out;
        out << codigo_ << " " << descripcion() << " S/ " << std::fixed << std::setprecision(2)
            << precio_ << " (stock: " << stock_ << ")";
        return out.str();
    }
};

class ProductoFisico : public Producto {
    double pesoKg_;
    static constexpr double TARIFA_POR_KG = 3.0;

    static double validarPeso(double p) {
        if (p <= 0) throw ErrorValidacion("peso_kg", "debe ser mayor que 0");
        return p;
    }

public:
    ProductoFisico(const std::string& codigo, std::string nombre, double precio, int stock, double pesoKg)
        : Producto(codigo, std::move(nombre), precio, stock), pesoKg_(validarPeso(pesoKg)) {}

    double calcularCostoEnvio(int cantidad) const override { return pesoKg_ * cantidad * TARIFA_POR_KG; }
    std::string descripcion() const override {
        std::ostringstream out;
        out << getNombre() << " (" << pesoKg_ << " kg)";
        return out.str();
    }
};

class ProductoDigital : public Producto {
    double tamanoMb_;

    static double validarTamano(double t) {
        if (t <= 0) throw ErrorValidacion("tamano_mb", "debe ser mayor que 0");
        return t;
    }

public:
    ProductoDigital(const std::string& codigo, std::string nombre, double precio, int stock, double tamanoMb)
        : Producto(codigo, std::move(nombre), precio, stock), tamanoMb_(validarTamano(tamanoMb)) {}

    double calcularCostoEnvio(int) const override { return 0.0; }
    std::string descripcion() const override {
        std::ostringstream out;
        out << getNombre() << " (descarga " << tamanoMb_ << " MB)";
        return out.str();
    }
};

class Cliente {
    std::string dni_, nombre_, correo_, direccion_;
    std::vector<double> compras_;

public:
    Cliente(std::string dni, std::string nombre, std::string correo, std::string direccion) {
        static const std::regex patronDni("^[0-9]{8}$");
        static const std::regex patronCorreo(R"(^[\w.+-]+@[\w-]+(\.[\w-]+)+$)");
        if (!std::regex_match(dni, patronDni)) throw ErrorValidacion("dni", "debe tener 8 dígitos");
        if (nombre.empty()) throw ErrorValidacion("nombre", "no puede estar vacío");
        if (!std::regex_match(correo, patronCorreo)) throw ErrorValidacion("correo", "formato usuario@dominio");
        if (direccion.empty()) throw ErrorValidacion("dirección", "no puede estar vacía");
        dni_ = std::move(dni);
        nombre_ = std::move(nombre);
        correo_ = std::move(correo);
        direccion_ = std::move(direccion);
    }

    const std::string& getDni() const noexcept { return dni_; }
    const std::string& getNombre() const noexcept { return nombre_; }
    const std::string& getCorreo() const noexcept { return correo_; }
    double totalGastado() const { return std::accumulate(compras_.begin(), compras_.end(), 0.0); }

    void registrarCompra(double monto) {
        if (monto <= 0) throw ErrorValidacion("monto", "debe ser mayor que 0");
        compras_.push_back(monto);
    }
};

class Pedido {
public:
    enum class Estado { Pendiente, Pagado, Cancelado };

private:
    /*
     * INVARIANTE: numero_ > 0, toda cantidad > 0, estado Pagado => !lineas_.empty()
     */
    int numero_;
    Cliente& cliente_;
    std::vector<std::pair<Producto*, int>> lineas_;
    Estado estado_ = Estado::Pendiente;

    void verificarInvariante() const {
        assert(numero_ > 0 && "INV: número");
        assert(std::all_of(lineas_.begin(), lineas_.end(),
                           [](const auto& linea) { return linea.second > 0; }) && "INV: cantidad");
        assert((estado_ != Estado::Pagado || !lineas_.empty()) && "INV: pedido pagado vacío");
    }

public:
    Pedido(int numero, Cliente& cliente) : numero_(numero), cliente_(cliente) {
        if (numero <= 0) throw ErrorValidacion("número de pedido", "debe ser mayor que 0");
        verificarInvariante();
    }

    int getNumero() const noexcept { return numero_; }
    const Cliente& getCliente() const noexcept { return cliente_; }
    Estado getEstado() const noexcept { return estado_; }

    double total() const {
        double t = 0.0;
        for (const auto& [p, cant] : lineas_) t += p->costoTotal(cant);
        return t;
    }
    int cantidadArticulos() const {
        int n = 0;
        for (const auto& linea : lineas_) n += linea.second;
        return n;
    }

    std::string estadoTexto() const {
        switch (estado_) {
            case Estado::Pendiente: return "PENDIENTE";
            case Estado::Pagado: return "PAGADO";
            case Estado::Cancelado: return "CANCELADO";
        }
        return "";
    }

    void agregarProducto(Producto& producto, int cantidad) {
        // PRECONDICIONES
        if (estado_ != Estado::Pendiente) throw ErrorEstadoPedido(numero_, estadoTexto(), "agregar productos");
        if (cantidad <= 0) throw ErrorValidacion("cantidad", "debe ser mayor que 0");
        int reservado = 0;
        for (const auto& [p, cant] : lineas_)
            if (p == &producto) reservado += cant;
        if (reservado + cantidad > producto.getStock())
            throw ErrorStockInsuficiente(producto.getCodigo(), producto.getStock() - reservado, cantidad);
        const int antes = cantidadArticulos();
        lineas_.emplace_back(&producto, cantidad);
        // POSCONDICIÓN
        assert(cantidadArticulos() == antes + cantidad && "POST: línea no agregada");
        (void)antes;
        verificarInvariante();
    }

    void confirmarPago() {
        if (estado_ != Estado::Pendiente) throw ErrorEstadoPedido(numero_, estadoTexto(), "confirmar el pago");
        if (lineas_.empty()) throw ErrorEstadoPedido(numero_, "VACÍO", "confirmar el pago");
        for (auto& [p, cant] : lineas_) p->reducirStock(cant);
        cliente_.registrarCompra(total());
        estado_ = Estado::Pagado;
        verificarInvariante();
    }

    void cancelar() {
        if (estado_ != Estado::Pendiente) throw ErrorEstadoPedido(numero_, estadoTexto(), "cancelar");
        estado_ = Estado::Cancelado;
        verificarInvariante();
    }

    std::string toString() const {
        std::ostringstream out;
        out << "Pedido #" << numero_ << " — " << cliente_.getNombre() << " — " << cantidadArticulos()
            << " artículo(s) — S/ " << std::fixed << std::setprecision(2) << total() << " ["
            << estadoTexto() << "]";
        return out.str();
    }
};
