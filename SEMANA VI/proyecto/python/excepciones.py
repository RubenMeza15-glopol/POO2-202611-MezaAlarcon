# ── excepciones.py — jerarquía de errores de la Tienda en Línea Local ────


class ErrorTienda(Exception):
    """Raíz de todas las excepciones del dominio de la tienda."""

    def __init__(self, mensaje: str, contexto: dict | None = None):
        super().__init__(mensaje)
        self.contexto: dict = contexto or {}

    def __str__(self) -> str:
        base = super().__str__()
        if self.contexto:
            ctx = ", ".join(f"{k}={v!r}" for k, v in self.contexto.items())
            return f"{base}  ← contexto: {{{ctx}}}"
        return base


class ErrorValidacion(ErrorTienda):
    """Dato de entrada que viola una regla del dominio."""

    def __init__(self, campo: str, valor, regla: str):
        super().__init__(f"{campo} inválido: {regla}",
                         contexto={"campo": campo, "valor": valor})
        self.campo = campo
        self.valor = valor


class ErrorStockInsuficiente(ErrorTienda):
    """Se pide más unidades de las disponibles."""

    def __init__(self, codigo: str, disponible: int, solicitado: int):
        super().__init__(f"Stock insuficiente de {codigo}",
                         contexto={"disponible": disponible, "solicitado": solicitado})
        self.codigo = codigo
        self.disponible = disponible
        self.solicitado = solicitado


class ErrorEstadoPedido(ErrorTienda):
    """Operación no permitida en el estado actual del pedido."""

    def __init__(self, numero: int, estado: str, operacion: str):
        super().__init__(f"Pedido #{numero}: no se puede {operacion} en estado {estado}",
                         contexto={"numero": numero, "estado": estado})


class ErrorPago(ErrorTienda):
    """El método de pago rechazó o no pudo procesar el cobro."""

    def __init__(self, metodo: str, monto: float, motivo: str):
        super().__init__(f"Pago rechazado por {metodo}: {motivo}",
                         contexto={"metodo": metodo, "monto": round(monto, 2)})


class ErrorRecursoNoEncontrado(ErrorTienda):
    """Entidad buscada que no existe."""

    def __init__(self, tipo: str, identificador):
        super().__init__(f"{tipo} con id={identificador!r} no encontrado",
                         contexto={"tipo": tipo, "id": identificador})
