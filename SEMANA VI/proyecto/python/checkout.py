# Proyecto Integrador — Tienda en Línea Local — Semana 6: checkout (base de la Semana 5)
from abc import ABC, abstractmethod
from typing import override

from excepciones import ErrorPago, ErrorValidacion
from tienda import Pedido


# ── Interfaces del dominio ───────────────────────────────────────────────
class IMetodoPago(ABC):
    """Contrato: cualquier forma de cobrar un pedido."""

    @abstractmethod
    def procesar_pago(self, monto: float, referencia: str) -> bool: ...

    @abstractmethod
    def es_disponible(self, monto: float) -> bool: ...

    @property
    @abstractmethod
    def nombre(self) -> str: ...


class INotificador(ABC):
    """Contrato: avisar al cliente sobre su pedido."""

    @abstractmethod
    def notificar(self, destinatario: str, mensaje: str) -> bool: ...

    @property
    @abstractmethod
    def canal(self) -> str: ...


# ── Implementaciones concretas (intercambiables) ─────────────────────────
class PagoTarjeta(IMetodoPago):
    def __init__(self, ultimos_digitos: str, limite: float):
        self._ultimos = ultimos_digitos
        self._limite = limite

    @property
    def nombre(self) -> str: return f"Tarjeta ****{self._ultimos}"

    @override
    def es_disponible(self, monto: float) -> bool:
        return monto <= self._limite

    @override
    def procesar_pago(self, monto: float, referencia: str) -> bool:
        print(f"[TARJETA ****{self._ultimos}] Cobro S/ {monto:.2f} — ref {referencia}")
        self._limite -= monto
        return True


class PagoYape(IMetodoPago):
    LIMITE_DIARIO = 500.0

    def __init__(self, celular: str):
        self._celular = celular

    @property
    def nombre(self) -> str: return f"Yape ({self._celular})"

    @override
    def es_disponible(self, monto: float) -> bool:
        return monto <= self.LIMITE_DIARIO

    @override
    def procesar_pago(self, monto: float, referencia: str) -> bool:
        print(f"[YAPE {self._celular}] Pago S/ {monto:.2f} — ref {referencia}")
        return True


class PagoContraEntrega(IMetodoPago):
    @property
    def nombre(self) -> str: return "Contra entrega"

    @override
    def es_disponible(self, monto: float) -> bool:
        return True

    @override
    def procesar_pago(self, monto: float, referencia: str) -> bool:
        print(f"[CONTRA ENTREGA] Se cobrará S/ {monto:.2f} al entregar — ref {referencia}")
        return True


class NotificadorEmail(INotificador):
    @property
    def canal(self) -> str: return "Email"

    @override
    def notificar(self, destinatario: str, mensaje: str) -> bool:
        print(f"[EMAIL → {destinatario}]: {mensaje}")
        return True


class NotificadorWhatsApp(INotificador):
    @property
    def canal(self) -> str: return "WhatsApp"

    @override
    def notificar(self, destinatario: str, mensaje: str) -> bool:
        print(f"[WHATSAPP → {destinatario}]: {mensaje}")
        return True


# ── Consumidor: recibe sus dependencias por constructor (DI) ─────────────
class ServicioCheckout:
    """Coordina el cobro y el aviso de un pedido. No conoce clases concretas."""

    def __init__(self, metodo_pago: IMetodoPago, notificador: INotificador):
        self._metodo_pago = metodo_pago
        self._notificador = notificador

    def cambiar_metodo_pago(self, metodo: IMetodoPago) -> None:
        self._metodo_pago = metodo

    def procesar(self, pedido: Pedido) -> bool:
        # PRECONDICIÓN
        if pedido.cantidad_articulos == 0:
            raise ErrorValidacion("pedido", pedido.numero, "no tiene productos")
        monto = pedido.total
        referencia = f"PED-{pedido.numero}"
        if not self._metodo_pago.es_disponible(monto):
            self._notificador.notificar(
                pedido.cliente.correo,
                f"Pedido #{pedido.numero}: {self._metodo_pago.nombre} no disponible para S/ {monto:.2f}")
            raise ErrorPago(self._metodo_pago.nombre, monto, "monto excede el límite")
        if not self._metodo_pago.procesar_pago(monto, referencia):
            raise ErrorPago(self._metodo_pago.nombre, monto, "operación rechazada")
        pedido.confirmar_pago()
        # POSCONDICIÓN
        assert pedido.estado == "PAGADO", "POST: pedido no quedó pagado"
        self._notificador.notificar(
            pedido.cliente.correo,
            f"Pedido #{pedido.numero} pagado con {self._metodo_pago.nombre}: S/ {monto:.2f}")
        return True
