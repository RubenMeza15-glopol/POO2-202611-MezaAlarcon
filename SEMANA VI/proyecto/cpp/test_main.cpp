// test_main.cpp — g++ -std=c++17 -Wall -Wextra -o test_main test_main.cpp && ./test_main
#include <cassert>
#include <cmath>
#include <iostream>

#include "servicio_tienda.hpp"

struct Item {
    int id;
    double valor;
};

class PagoOk : public IMetodoPago {
public:
    std::string nombre() const override { return "Ok"; }
    bool esDisponible(double) const override { return true; }
    bool procesarPago(double, const std::string&) override { return true; }
};

class AvisoNulo : public INotificador {
public:
    std::string canal() const override { return "Nulo"; }
    bool notificar(const std::string&, const std::string&) override { return true; }
};

bool cerca(double a, double b) { return std::fabs(a - b) < 1e-9; }

Repositorio<Item, int> crearRepo() {
    Repositorio<Item, int> r([](const Item& i) { return i.id; });
    r.guardar({1, 5.0});
    r.guardar({2, 1.0});
    r.guardar({3, 3.0});
    return r;
}

void test_crud() {
    auto r = crearRepo();
    assert(r.tamaño() == 3 && r.existe(2) && !r.buscar(9));
    assert(r.eliminar(2) && !r.eliminar(2));
    r.guardar({1, 9.0});   // sobreescribe
    assert(r.buscar(1)->valor == 9.0 && r.tamaño() == 2);
    std::cout << "[PASS] CRUD del repositorio\n";
}

void test_consultas_genericas() {
    auto r = crearRepo();
    assert(r.filtrar([](const Item& i) { return i.valor > 2; }).size() == 2);
    auto orden = r.ordenar([](const Item& a, const Item& b) { return a.valor < b.valor; });
    assert(orden[0].id == 2 && orden[2].id == 1);
    assert(cerca(r.acumular(0.0, [](double acc, const Item& i) { return acc + i.valor; }), 9.0));
    assert(r.contar([](const Item& i) { return i.valor >= 3; }) == 2);
    assert(r.primero([](const Item& i) { return i.valor < 2; })->id == 2);
    assert(!r.primero([](const Item& i) { return i.valor > 100; }));
    std::cout << "[PASS] filtrar/ordenar/acumular/contar/primero\n";
}

void test_cola_fifo() {
    ColaAtencion<int> cola;
    for (int x : {1, 2, 3}) cola.encolar(x);
    assert(*cola.atender() == 1 && *cola.atender() == 2 && *cola.atender() == 3 && !cola.atender());
    std::cout << "[PASS] cola FIFO\n";
}

TiendaEnLinea crearTienda() {
    TiendaEnLinea t;
    t.registrarProducto(std::make_shared<ProductoFisico>("PRD-0001", "Teclado", 150.0, 10, 1.0));
    t.registrarProducto(std::make_shared<ProductoFisico>("PRD-0002", "Mouse", 45.5, 3, 0.2));
    t.registrarProducto(std::make_shared<ProductoDigital>("PRD-0003", "Antivirus", 89.9, 50, 350));
    t.registrarCliente(std::make_shared<Cliente>("71234567", "Rosa", "rosa@gmail.com", "Puno"));
    return t;
}

void test_registro_duplicado() {
    auto t = crearTienda();
    bool lanzo = false;
    try { t.registrarProducto(std::make_shared<ProductoDigital>("PRD-0003", "Otro", 1.0, 1, 1)); }
    catch (const ErrorValidacion&) { lanzo = true; }
    assert(lanzo);
    std::cout << "[PASS] registro duplicado rechazado\n";
}

void test_consultas_tienda() {
    auto t = crearTienda();
    auto bajo = t.productosStockBajo();
    assert(bajo.size() == 1 && bajo[0]->getCodigo() == "PRD-0002");
    assert(t.catalogoPorPrecio()[0]->getCodigo() == "PRD-0001");
    assert(cerca(t.valorInventario(), 150 * 10 + 45.5 * 3 + 89.9 * 50));
    assert(t.cantidadProductosDigitales() == 1);
    assert((*t.primerProductoHasta(50))->getCodigo() == "PRD-0002");
    assert(!t.buscarProducto("PRD-9999").esExito());
    std::cout << "[PASS] consultas de dominio\n";
}

void test_pagar_y_despachar() {
    auto t = crearTienda();
    auto cliente = t.buscarCliente("71234567").valor();
    PagoOk pago;
    AvisoNulo aviso;
    ServicioCheckout checkout(pago, aviso);
    for (const std::string codigo : {"PRD-0001", "PRD-0003"}) {
        auto pedido = t.crearPedido(*cliente);
        pedido->agregarProducto(*t.buscarProducto(codigo).valor(), 1);
        t.pagar(pedido, checkout);
    }
    assert(cerca(t.ventasTotales(), 150 + 3.0 + 89.9));
    assert((*t.despachar())->getNumero() == 1 && (*t.despachar())->getNumero() == 2 && !t.despachar());
    std::cout << "[PASS] pago, ventas y despacho FIFO\n";
}

int main() {
    test_crud();
    test_consultas_genericas();
    test_cola_fifo();
    test_registro_duplicado();
    test_consultas_tienda();
    test_pagar_y_despachar();
    std::cout << "\nTodas las pruebas pasaron (6/6).\n";
    return 0;
}
