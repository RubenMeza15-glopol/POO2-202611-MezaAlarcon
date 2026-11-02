// g++ -std=c++17 -Wall -Wextra -o tienda main_tienda.cpp
#include "servicio_tienda.hpp"

int main() {
    TiendaEnLinea tienda;
    tienda.registrarProducto(std::make_shared<ProductoFisico>("PRD-0001", "Teclado mecánico", 150.0, 10, 1.2));
    tienda.registrarProducto(std::make_shared<ProductoFisico>("PRD-0002", "Mouse inalámbrico", 45.5, 3, 0.2));
    tienda.registrarProducto(std::make_shared<ProductoDigital>("PRD-0003", "Licencia antivirus 1 año", 89.9, 50, 350));
    tienda.registrarProducto(std::make_shared<ProductoFisico>("PRD-0004", "Monitor 24 pulgadas", 620.0, 4, 4.5));
    tienda.registrarProducto(std::make_shared<ProductoDigital>("PRD-0005", "Curso en línea de Python", 120.0, 100, 2048));
    tienda.registrarCliente(std::make_shared<Cliente>("71234567", "Rosa Condori", "rosa.condori@gmail.com", "Jr. Lima 123, Puno"));
    tienda.registrarCliente(std::make_shared<Cliente>("72345678", "Carlos Apaza", "capaza@gmail.com", "Av. El Sol 456, Puno"));
    tienda.registrarCliente(std::make_shared<Cliente>("73456789", "Lucía Mamani", "lmamani@gmail.com", "Jr. Arequipa 789, Juliaca"));

    PagoTarjeta tarjeta("4321", 5000.0);
    NotificadorEmail email;
    ServicioCheckout checkout(tarjeta, email);

    const std::vector<std::pair<std::string, std::vector<std::pair<std::string, int>>>> compras = {
        {"71234567", {{"PRD-0004", 1}, {"PRD-0001", 1}}},
        {"72345678", {{"PRD-0003", 2}}},
        {"73456789", {{"PRD-0002", 2}, {"PRD-0009", 1}}},
    };
    for (const auto& [dni, items] : compras) {
        auto pedido = tienda.crearPedido(*tienda.buscarCliente(dni).valor());
        for (const auto& [codigo, cantidad] : items) {
            auto res = tienda.buscarProducto(codigo);
            if (res.esExito()) pedido->agregarProducto(*res.valor(), cantidad);
            else std::cout << "Se omite: " << res.error() << "\n";
        }
        try {
            tienda.pagar(pedido, checkout);
        } catch (const ErrorTienda& e) {
            std::cout << "Error: " << e.what() << "\n";
        }
    }

    std::cout << std::fixed << std::setprecision(2) << "\n── Consultas de dominio ──\n1. Stock bajo (< 5):";
    for (const auto& p : tienda.productosStockBajo()) std::cout << " " << p->getCodigo() << " (" << p->getStock() << ")";
    std::cout << "\n2. Catálogo por precio:\n";
    for (const auto& p : tienda.catalogoPorPrecio()) std::cout << "     " << p->toString() << "\n";
    std::cout << "3. Valor de inventario: S/ " << tienda.valorInventario() << "\n";
    std::cout << "4. Clientes frecuentes (≥ S/ 500):";
    for (const auto& c : tienda.clientesFrecuentes()) std::cout << " " << c->getNombre() << " (S/ " << c->totalGastado() << ")";
    std::cout << "\n5. Ventas totales: S/ " << tienda.ventasTotales() << "\n";
    std::cout << "6. Productos digitales: " << tienda.cantidadProductosDigitales() << "\n";
    auto barato = tienda.primerProductoHasta(50);
    std::cout << "7. Primer producto hasta S/ 50: " << (barato ? (*barato)->getNombre() : "ninguno") << "\n";
    std::cout << "8. Búsqueda inexistente: " << tienda.buscarProducto("PRD-9999").error() << "\n";

    std::cout << "\n── Despacho FIFO (" << tienda.colaDespacho.tamano() << " pedidos) ──\n";
    while (auto pedido = tienda.despachar()) std::cout << "  → Despachado: " << (*pedido)->toString() << "\n";
    return 0;
}
