# Proyecto Integrador — Tienda en Línea Local — Semana 6: entidades (base de la Semana 5)
import re
from abc import ABC, abstractmethod
from typing import override

from excepciones import ErrorEstadoPedido, ErrorStockInsuficiente, ErrorValidacion


class Producto(ABC):
    """
    INVARIANTE:
        código con formato PRD-0000
        nombre no vacío
        precio > 0
        stock >= 0
    """
    _PATRON_CODIGO = re.compile(r"^PRD-\d{4}$")

    def __init__(self, codigo: str, nombre: str, precio: float, stock: int):
        # ── PRECONDICIONES ───────────────────────────────────────────────
        if not self._PATRON_CODIGO.match(codigo):
            raise ErrorValidacion("código", codigo, "formato PRD-0000")
        self.__codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self._verificar_invariante()  # POST-constructor

    @property
    def codigo(self) -> str:
        return self.__codigo

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor.strip():
            raise ErrorValidacion("nombre", valor, "no puede estar vacío")
        self.__nombre = valor.strip()

    @property
    def precio(self) -> float:
        return self.__precio

    @precio.setter
    def precio(self, valor: float) -> None:
        if valor <= 0:
            raise ErrorValidacion("precio", valor, "debe ser mayor que 0")
        self.__precio = float(valor)

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if valor < 0:
            raise ErrorValidacion("stock", valor, "no puede ser negativo")
        self.__stock = valor

    @property
    def valor_inventario(self) -> float:
        return self.__precio * self.__stock

    def reducir_stock(self, cantidad: int) -> None:
        # PRECONDICIÓN
        if cantidad <= 0:
            raise ErrorValidacion("cantidad", cantidad, "debe ser mayor que 0")
        if cantidad > self.__stock:
            raise ErrorStockInsuficiente(self.__codigo, self.__stock, cantidad)
        stock_anterior = self.__stock
        self.__stock -= cantidad
        # POSCONDICIÓN
        assert self.__stock == stock_anterior - cantidad, "POST: stock mal descontado"
        self._verificar_invariante()

    def reponer_stock(self, cantidad: int) -> None:
        if cantidad <= 0:
            raise ErrorValidacion("cantidad", cantidad, "debe ser mayor que 0")
        self.__stock += cantidad
        self._verificar_invariante()

    @abstractmethod
    def calcular_costo_envio(self, cantidad: int) -> float: ...

    def descripcion(self) -> str:
        return self.__nombre

    def costo_total(self, cantidad: int) -> float:
        return self.__precio * cantidad + self.calcular_costo_envio(cantidad)

    def _verificar_invariante(self) -> None:
        assert self._PATRON_CODIGO.match(self.__codigo), "INV: código"
        assert len(self.__nombre) > 0, "INV: nombre vacío"
        assert self.__precio > 0, "INV: precio"
        assert self.__stock >= 0, "INV: stock negativo"

    def diagnostico(self) -> str:
        try:
            self._verificar_invariante()
            return f"{self.__codigo}: OK — stock {self.__stock}"
        except AssertionError as e:
            return f"{self.__codigo}: INVÁLIDO — {e}"

    def __str__(self) -> str:
        return f"{self.__codigo} {self.descripcion()} S/ {self.__precio:.2f} (stock: {self.__stock})"


class ProductoFisico(Producto):
    TARIFA_POR_KG = 3.0

    def __init__(self, codigo: str, nombre: str, precio: float, stock: int, peso_kg: float):
        if peso_kg <= 0:
            raise ErrorValidacion("peso_kg", peso_kg, "debe ser mayor que 0")
        self.__peso_kg = peso_kg
        super().__init__(codigo, nombre, precio, stock)

    @override
    def calcular_costo_envio(self, cantidad: int) -> float:
        return self.__peso_kg * cantidad * self.TARIFA_POR_KG

    @override
    def descripcion(self) -> str:
        return f"{self.nombre} ({self.__peso_kg} kg)"


class ProductoDigital(Producto):
    def __init__(self, codigo: str, nombre: str, precio: float, stock: int, tamano_mb: float):
        if tamano_mb <= 0:
            raise ErrorValidacion("tamano_mb", tamano_mb, "debe ser mayor que 0")
        self.__tamano_mb = tamano_mb
        super().__init__(codigo, nombre, precio, stock)

    @override
    def calcular_costo_envio(self, cantidad: int) -> float:
        return 0.0

    @override
    def descripcion(self) -> str:
        return f"{self.nombre} (descarga {self.__tamano_mb} MB)"


class Cliente:
    """INVARIANTE: DNI de 8 dígitos, nombre y dirección no vacíos, correo válido."""
    _PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")

    def __init__(self, dni: str, nombre: str, correo: str, direccion: str):
        if not (len(dni) == 8 and dni.isdigit()):
            raise ErrorValidacion("dni", dni, "debe tener 8 dígitos")
        if not nombre.strip():
            raise ErrorValidacion("nombre", nombre, "no puede estar vacío")
        if not self._PATRON_CORREO.match(correo):
            raise ErrorValidacion("correo", correo, "formato usuario@dominio")
        if not direccion.strip():
            raise ErrorValidacion("dirección", direccion, "no puede estar vacía")
        self.__dni = dni
        self.__nombre = nombre.strip()
        self.__correo = correo
        self.__direccion = direccion.strip()
        self.__compras: list[float] = []

    @property
    def dni(self) -> str: return self.__dni

    @property
    def nombre(self) -> str: return self.__nombre

    @property
    def correo(self) -> str: return self.__correo

    @property
    def direccion(self) -> str: return self.__direccion

    @property
    def total_gastado(self) -> float:
        return sum(self.__compras)

    def registrar_compra(self, monto: float) -> None:
        if monto <= 0:
            raise ErrorValidacion("monto", monto, "debe ser mayor que 0")
        self.__compras.append(monto)

    def __str__(self) -> str:
        return f"{self.__nombre} (DNI {self.__dni}) — gastado: S/ {self.total_gastado:.2f}"


class Pedido:
    """
    INVARIANTE:
        número > 0
        estado in ESTADOS
        toda cantidad > 0
        estado PAGADO  =>  al menos una línea
    """
    ESTADOS = ("PENDIENTE", "PAGADO", "CANCELADO")

    def __init__(self, numero: int, cliente: Cliente):
        if numero <= 0:
            raise ErrorValidacion("número de pedido", numero, "debe ser mayor que 0")
        self.__numero = numero
        self.__cliente = cliente
        self.__lineas: list[tuple[Producto, int]] = []
        self.__estado = "PENDIENTE"
        self._verificar_invariante()

    @property
    def numero(self) -> int: return self.__numero

    @property
    def cliente(self) -> Cliente: return self.__cliente

    @property
    def estado(self) -> str: return self.__estado

    @property
    def total(self) -> float:
        return sum(p.costo_total(c) for p, c in self.__lineas)

    @property
    def cantidad_articulos(self) -> int:
        return sum(c for _, c in self.__lineas)

    def agregar_producto(self, producto: Producto, cantidad: int) -> None:
        # PRECONDICIONES
        if self.__estado != "PENDIENTE":
            raise ErrorEstadoPedido(self.__numero, self.__estado, "agregar productos")
        if cantidad <= 0:
            raise ErrorValidacion("cantidad", cantidad, "debe ser mayor que 0")
        reservado = sum(c for p, c in self.__lineas if p is producto)
        if reservado + cantidad > producto.stock:
            raise ErrorStockInsuficiente(producto.codigo, producto.stock - reservado, cantidad)
        articulos_antes = self.cantidad_articulos
        self.__lineas.append((producto, cantidad))
        # POSCONDICIÓN
        assert self.cantidad_articulos == articulos_antes + cantidad, "POST: línea no agregada"
        self._verificar_invariante()

    def confirmar_pago(self) -> None:
        if self.__estado != "PENDIENTE":
            raise ErrorEstadoPedido(self.__numero, self.__estado, "confirmar el pago")
        if not self.__lineas:
            raise ErrorEstadoPedido(self.__numero, "VACÍO", "confirmar el pago")
        for producto, cantidad in self.__lineas:
            producto.reducir_stock(cantidad)
        self.__cliente.registrar_compra(self.total)
        self.__estado = "PAGADO"
        self._verificar_invariante()

    def cancelar(self) -> None:
        if self.__estado != "PENDIENTE":
            raise ErrorEstadoPedido(self.__numero, self.__estado, "cancelar")
        self.__estado = "CANCELADO"
        self._verificar_invariante()

    def _verificar_invariante(self) -> None:
        assert self.__numero > 0, "INV: número"
        assert self.__estado in self.ESTADOS, "INV: estado"
        assert all(c > 0 for _, c in self.__lineas), "INV: cantidad no positiva"
        assert self.__estado != "PAGADO" or self.__lineas, "INV: pedido pagado vacío"

    def diagnostico(self) -> str:
        try:
            self._verificar_invariante()
            return f"Pedido #{self.__numero}: OK — {self.__estado}"
        except AssertionError as e:
            return f"Pedido #{self.__numero}: INVÁLIDO — {e}"

    def __str__(self) -> str:
        return (f"Pedido #{self.__numero} — {self.__cliente.nombre} — "
                f"{self.cantidad_articulos} artículo(s) — S/ {self.total:.2f} [{self.__estado}]")
