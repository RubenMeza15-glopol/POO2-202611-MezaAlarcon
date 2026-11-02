# Pruebas del repositorio genérico y de la tienda — ejecutar: pytest -v test_repositorio.py
from dataclasses import dataclass

import pytest

from checkout import IMetodoPago, INotificador, ServicioCheckout
from cola_atencion import ColaAtencion
from excepciones import ErrorValidacion
from repositorio import Repositorio
from servicio_tienda import TiendaEnLinea
from tienda import Cliente, ProductoDigital, ProductoFisico


@dataclass
class Item:
    id: int
    valor: float


@pytest.fixture
def repo():
    r: Repositorio[Item, int] = Repositorio(lambda i: i.id)
    for i, v in enumerate([5.0, 1.0, 3.0], start=1):
        r.guardar(Item(i, v))
    return r


class PagoOk(IMetodoPago):
    @property
    def nombre(self) -> str: return "Ok"
    def es_disponible(self, monto: float) -> bool: return True
    def procesar_pago(self, monto: float, referencia: str) -> bool: return True


class AvisoNulo(INotificador):
    @property
    def canal(self) -> str: return "Nulo"
    def notificar(self, destinatario: str, mensaje: str) -> bool: return True


@pytest.fixture
def tienda():
    t = TiendaEnLinea()
    t.registrar_producto(ProductoFisico("PRD-0001", "Teclado", 150.0, 10, 1.0))
    t.registrar_producto(ProductoFisico("PRD-0002", "Mouse", 45.5, 3, 0.2))
    t.registrar_producto(ProductoDigital("PRD-0003", "Antivirus", 89.9, 50, 350))
    t.registrar_cliente(Cliente("71234567", "Rosa", "rosa@gmail.com", "Puno"))
    return t


# ── Repositorio genérico ─────────────────────────────────────────────────
def test_crud(repo):
    assert len(repo) == 3 and repo.existe(2) and 2 in repo
    assert repo.buscar(9) is None
    assert repo.eliminar(2) and not repo.eliminar(2)
    repo.guardar(Item(1, 9.0))          # sobreescribe
    assert repo.buscar(1).valor == 9.0 and len(repo) == 2


def test_consultas(repo):
    assert [i.id for i in repo.filtrar(lambda i: i.valor > 2)] == [1, 3]
    assert [i.valor for i in repo.ordenar(key=lambda i: i.valor)] == [1.0, 3.0, 5.0]
    assert repo.acumular(0.0, lambda acc, i: acc + i.valor) == 9.0
    assert repo.contar(lambda i: i.valor >= 3) == 2
    assert repo.primero(lambda i: i.valor < 2).id == 2
    assert repo.primero(lambda i: i.valor > 100) is None


def test_estadisticas(repo):
    assert repo.estadisticas("valor") == {"min": 1.0, "max": 5.0, "promedio": 3.0, "n": 3}


def test_cola_fifo():
    cola: ColaAtencion[str] = ColaAtencion()
    for x in "abc":
        cola.encolar(x)
    assert [cola.atender() for _ in range(4)] == ["a", "b", "c", None]


# ── Tienda sobre repositorios ────────────────────────────────────────────
def test_registro_duplicado(tienda):
    with pytest.raises(ErrorValidacion):
        tienda.registrar_producto(ProductoDigital("PRD-0003", "Otro", 1.0, 1, 1))


def test_consultas_tienda(tienda):
    assert [p.codigo for p in tienda.productos_stock_bajo()] == ["PRD-0002"]
    assert tienda.catalogo_por_precio()[0].codigo == "PRD-0001"
    assert tienda.valor_inventario() == pytest.approx(150 * 10 + 45.5 * 3 + 89.9 * 50)
    assert tienda.cantidad_productos_digitales() == 1
    assert tienda.primer_producto_hasta(50).codigo == "PRD-0002"
    assert not tienda.buscar_producto("PRD-9999").es_exito


def test_pagar_encola_y_despacha(tienda):
    cliente = tienda.buscar_cliente("71234567").valor
    checkout = ServicioCheckout(PagoOk(), AvisoNulo())
    for codigo in ("PRD-0001", "PRD-0003"):
        pedido = tienda.crear_pedido(cliente)
        pedido.agregar_producto(tienda.buscar_producto(codigo).valor, 1)
        tienda.pagar(pedido, checkout)
    assert tienda.ventas_totales() == pytest.approx(150 + 3.0 + 89.9)
    assert [tienda.despachar().numero, tienda.despachar().numero] == [1, 2]
    assert tienda.despachar() is None
