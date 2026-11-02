# Demostración — Tienda en Línea Local — Semana 6
from checkout import NotificadorEmail, PagoTarjeta, ServicioCheckout
from excepciones import ErrorTienda
from servicio_tienda import TiendaEnLinea
from tienda import Cliente, ProductoDigital, ProductoFisico

tienda = TiendaEnLinea()
for p in (ProductoFisico("PRD-0001", "Teclado mecánico", 150.0, 10, 1.2),
          ProductoFisico("PRD-0002", "Mouse inalámbrico", 45.5, 3, 0.2),
          ProductoDigital("PRD-0003", "Licencia antivirus 1 año", 89.9, 50, 350),
          ProductoFisico("PRD-0004", "Monitor 24 pulgadas", 620.0, 4, 4.5),
          ProductoDigital("PRD-0005", "Curso en línea de Python", 120.0, 100, 2048)):
    tienda.registrar_producto(p)
for c in (Cliente("71234567", "Rosa Condori", "rosa.condori@gmail.com", "Jr. Lima 123, Puno"),
          Cliente("72345678", "Carlos Apaza", "capaza@gmail.com", "Av. El Sol 456, Puno"),
          Cliente("73456789", "Lucía Mamani", "lmamani@gmail.com", "Jr. Arequipa 789, Juliaca")):
    tienda.registrar_cliente(c)

checkout = ServicioCheckout(PagoTarjeta("4321", 5000.0), NotificadorEmail())
compras = [("71234567", [("PRD-0004", 1), ("PRD-0001", 1)]),
           ("72345678", [("PRD-0003", 2)]),
           ("73456789", [("PRD-0002", 2), ("PRD-0009", 1)])]
for dni, items in compras:
    cliente = tienda.buscar_cliente(dni).valor
    pedido = tienda.crear_pedido(cliente)
    for codigo, cantidad in items:
        res = tienda.buscar_producto(codigo)
        if res.es_exito:
            pedido.agregar_producto(res.valor, cantidad)
        else:
            print(f"Se omite: {res.error}")
    try:
        tienda.pagar(pedido, checkout)
    except ErrorTienda as e:
        print(f"Error: {e}")

print("\n── Consultas de dominio ──")
print("1. Stock bajo (< 5):", [f"{p.codigo} ({p.stock})" for p in tienda.productos_stock_bajo()])
print("2. Catálogo por precio:")
for p in tienda.catalogo_por_precio():
    print(f"     {p}")
print(f"3. Valor de inventario: S/ {tienda.valor_inventario():.2f}")
print("4. Clientes frecuentes (≥ S/ 500):", [str(c) for c in tienda.clientes_frecuentes()])
print(f"5. Ventas totales: S/ {tienda.ventas_totales():.2f}")
print(f"6. Productos digitales: {tienda.cantidad_productos_digitales()}")
barato = tienda.primer_producto_hasta(50)
print(f"7. Primer producto hasta S/ 50: {barato.nombre if barato else 'ninguno'}")
print(f"8. Búsqueda inexistente: {tienda.buscar_producto('PRD-9999').error}")

print(f"\n── Despacho FIFO ({len(tienda.cola_despacho)} pedidos) ──")
while tienda.cola_despacho:
    print(f"  → Despachado: {tienda.despachar()}")
