// Proyecto Integrador — Tienda en Línea Local — Semana 6: repositorios genéricos y colecciones STL
#pragma once
#include <deque>
#include <memory>
#include <optional>
#include <string>
#include <vector>

#include "checkout.hpp"
#include "repositorio.hpp"
#include "result.hpp"

// Cola FIFO con std::deque: push_back/pop_front O(1)
template <typename T>
class ColaAtencion {
    std::deque<T> cola_;

public:
    void encolar(T elemento) { cola_.push_back(std::move(elemento)); }
    std::optional<T> atender() {
        if (cola_.empty()) return std::nullopt;
        T primero = std::move(cola_.front());
        cola_.pop_front();
        return primero;
    }
    std::size_t tamano() const noexcept { return cola_.size(); }
    bool vacia() const noexcept { return cola_.empty(); }
};

using ProductoPtr = std::shared_ptr<Producto>;
using ClientePtr = std::shared_ptr<Cliente>;
using PedidoPtr = std::shared_ptr<Pedido>;

// Única capa de almacenamiento: Repositorio<T, ID> para cada entidad
class TiendaEnLinea {
public:
    Repositorio<ProductoPtr, std::string> productos{[](const ProductoPtr& p) { return p->getCodigo(); }};
    Repositorio<ClientePtr, std::string> clientes{[](const ClientePtr& c) { return c->getDni(); }};
    Repositorio<PedidoPtr, int> pedidos{[](const PedidoPtr& p) { return p->getNumero(); }};
    ColaAtencion<PedidoPtr> colaDespacho;

    // ── Registro ─────────────────────────────────────────────────────────
    void registrarProducto(ProductoPtr p) {
        if (productos.existe(p->getCodigo())) throw ErrorValidacion("código", "ya existe en el catálogo");
        productos.guardar(std::move(p));
    }

    void registrarCliente(ClientePtr c) {
        if (clientes.existe(c->getDni())) throw ErrorValidacion("dni", "cliente ya registrado");
        clientes.guardar(std::move(c));
    }

    // ── Búsquedas (Result para "no encontrado") ──────────────────────────
    Result<ProductoPtr> buscarProducto(const std::string& codigo) const {
        if (auto p = productos.buscar(codigo)) return Result<ProductoPtr>::ok(*p);
        return Result<ProductoPtr>::fallo("Producto " + codigo + " no existe en el catálogo");
    }

    Result<ClientePtr> buscarCliente(const std::string& dni) const {
        if (auto c = clientes.buscar(dni)) return Result<ClientePtr>::ok(*c);
        return Result<ClientePtr>::fallo("Cliente " + dni + " no registrado");
    }

    // ── Flujo de pedidos ─────────────────────────────────────────────────
    PedidoPtr crearPedido(Cliente& cliente) {
        auto pedido = std::make_shared<Pedido>(static_cast<int>(pedidos.tamaño()) + 1, cliente);
        pedidos.guardar(pedido);
        return pedido;
    }

    void pagar(const PedidoPtr& pedido, ServicioCheckout& checkout) {
        checkout.procesar(*pedido);
        colaDespacho.encolar(pedido);   // pagado → espera despacho (FIFO)
    }

    std::optional<PedidoPtr> despachar() { return colaDespacho.atender(); }

    // ── Consultas de dominio ─────────────────────────────────────────────
    std::vector<ProductoPtr> productosStockBajo(int umbral = 5) const {
        return productos.filtrar([umbral](const ProductoPtr& p) { return p->getStock() < umbral; });
    }

    std::vector<ProductoPtr> catalogoPorPrecio() const {
        return productos.ordenar([](const ProductoPtr& a, const ProductoPtr& b) {
            return a->getPrecio() > b->getPrecio();
        });
    }

    double valorInventario() const {
        return productos.acumular(0.0, [](double acc, const ProductoPtr& p) { return acc + p->valorInventario(); });
    }

    std::vector<ClientePtr> clientesFrecuentes(double montoMinimo = 500.0) const {
        auto frecuentes = clientes.filtrar([montoMinimo](const ClientePtr& c) { return c->totalGastado() >= montoMinimo; });
        std::sort(frecuentes.begin(), frecuentes.end(), [](const ClientePtr& a, const ClientePtr& b) {
            return a->totalGastado() > b->totalGastado();
        });
        return frecuentes;
    }

    double ventasTotales() const {
        return pedidos.acumular(0.0, [](double acc, const PedidoPtr& p) {
            return p->getEstado() == Pedido::Estado::Pagado ? acc + p->total() : acc;
        });
    }

    std::size_t cantidadProductosDigitales() const {
        return productos.contar([](const ProductoPtr& p) {
            return dynamic_cast<const ProductoDigital*>(p.get()) != nullptr;
        });
    }

    std::optional<ProductoPtr> primerProductoHasta(double precioMaximo) const {
        return productos.primero([precioMaximo](const ProductoPtr& p) { return p->getPrecio() <= precioMaximo; });
    }
};
