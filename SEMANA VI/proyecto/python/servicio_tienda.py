# Proyecto Integrador — Tienda en Línea Local — Semana 6: repositorios genéricos y colecciones
from checkout import ServicioCheckout
from cola_atencion import ColaAtencion
from excepciones import ErrorValidacion
from repositorio import Repositorio
from result import Result
from tienda import Cliente, Pedido, Producto, ProductoDigital


class TiendaEnLinea:
    """Única capa de almacenamiento: Repositorio[T, ID] para cada entidad."""

    def __init__(self) -> None:
        self.productos: Repositorio[Producto, str] = Repositorio(lambda p: p.codigo)
        self.clientes: Repositorio[Cliente, str] = Repositorio(lambda c: c.dni)
        self.pedidos: Repositorio[Pedido, int] = Repositorio(lambda p: p.numero)
        self.cola_despacho: ColaAtencion[Pedido] = ColaAtencion()

    # ── Registro ─────────────────────────────────────────────────────────
    def registrar_producto(self, producto: Producto) -> None:
        if self.productos.existe(producto.codigo):
            raise ErrorValidacion("código", producto.codigo, "ya existe en el catálogo")
        self.productos.guardar(producto)

    def registrar_cliente(self, cliente: Cliente) -> None:
        if self.clientes.existe(cliente.dni):
            raise ErrorValidacion("dni", cliente.dni, "cliente ya registrado")
        self.clientes.guardar(cliente)

    # ── Búsquedas (Result para "no encontrado") ──────────────────────────
    def buscar_producto(self, codigo: str) -> Result[Producto]:
        p = self.productos.buscar(codigo)
        return Result.ok(p) if p else Result.fallo(f"Producto {codigo} no existe en el catálogo")

    def buscar_cliente(self, dni: str) -> Result[Cliente]:
        c = self.clientes.buscar(dni)
        return Result.ok(c) if c else Result.fallo(f"Cliente {dni} no registrado")

    # ── Flujo de pedidos ─────────────────────────────────────────────────
    def crear_pedido(self, cliente: Cliente) -> Pedido:
        pedido = Pedido(len(self.pedidos) + 1, cliente)
        self.pedidos.guardar(pedido)
        return pedido

    def pagar(self, pedido: Pedido, checkout: ServicioCheckout) -> None:
        checkout.procesar(pedido)
        self.cola_despacho.encolar(pedido)   # pagado → espera despacho (FIFO)

    def despachar(self) -> Pedido | None:
        return self.cola_despacho.atender()

    # ── Consultas de dominio ─────────────────────────────────────────────
    def productos_stock_bajo(self, umbral: int = 5) -> list[Producto]:
        return self.productos.filtrar(lambda p: p.stock < umbral)

    def catalogo_por_precio(self, descendente: bool = True) -> list[Producto]:
        return self.productos.ordenar(key=lambda p: p.precio, reverse=descendente)

    def valor_inventario(self) -> float:
        return self.productos.acumular(0.0, lambda acc, p: acc + p.valor_inventario)

    def clientes_frecuentes(self, monto_minimo: float = 500.0) -> list[Cliente]:
        frecuentes = self.clientes.filtrar(lambda c: c.total_gastado >= monto_minimo)
        return sorted(frecuentes, key=lambda c: c.total_gastado, reverse=True)

    def ventas_totales(self) -> float:
        return self.pedidos.acumular(
            0.0, lambda acc, p: acc + p.total if p.estado == "PAGADO" else acc)

    def cantidad_productos_digitales(self) -> int:
        return self.productos.contar(lambda p: isinstance(p, ProductoDigital))

    def primer_producto_hasta(self, precio_maximo: float) -> Producto | None:
        return self.productos.primero(lambda p: p.precio <= precio_maximo)
