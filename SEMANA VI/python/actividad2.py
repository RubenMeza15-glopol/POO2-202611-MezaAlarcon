# ── Actividad 2: Repositorio Python + consultas de dominio + estadísticas ──
from dataclasses import dataclass

from repositorio import Repositorio


@dataclass
class Estudiante:
    codigo: int
    nombre: str
    ppa: float
    escuela: str


@dataclass
class Producto:
    codigo: str
    nombre: str
    precio: float
    stock: int
    categoria: str


# ── Uso con datos del dominio académico ──────────────────────────────────
repo: Repositorio[Estudiante, int] = Repositorio(lambda e: e.codigo)
for e in [
    Estudiante(1001, "Juan Carlos Mamani", 15.2, "Ing. Sistemas"),
    Estudiante(1002, "María Elena Quispe", 18.5, "Ing. Sistemas"),
    Estudiante(1003, "Pedro Flores", 9.8, "Ciencias Comp."),
    Estudiante(1004, "Ana Torres", 13.0, "Ing. Sistemas"),
    Estudiante(1005, "Luis Condori", 16.4, "Ciencias Comp."),
]:
    repo.guardar(e)

print(f"contar(PPA < 10.5): {repo.contar(lambda e: e.ppa < 10.5)}")
print(f"existe(1003): {repo.existe(1003)}  existe(2000): {repo.existe(2000)}")
desaprobado = repo.primero(lambda e: e.ppa < 10.5)
print(f"primero(PPA < 10.5): {desaprobado.nombre if desaprobado else None}")

# Consulta 1: estudiantes con PPA >= 14 en Ing. Sistemas
destacados_sis = repo.filtrar(lambda e: e.ppa >= 14.0 and e.escuela == "Ing. Sistemas")
print(f"\nDestacados Ing. Sistemas: {len(destacados_sis)}")

# Consulta 2: ranking completo por PPA
ranking = repo.ordenar(key=lambda e: e.ppa, reverse=True)
print("\nRanking completo:")
for i, e in enumerate(ranking, 1):
    print(f"  {i}. [{e.codigo}] {e.nombre} — {e.ppa:.2f}")

# Consulta 3: estadísticas por escuela
print("\nEstadísticas por escuela:")
escuelas = {e.escuela for e in repo}  # set de escuelas únicas
for esc in sorted(escuelas):
    alumnos = repo.filtrar(lambda e: e.escuela == esc)
    prom = sum(a.ppa for a in alumnos) / len(alumnos)
    print(f"  {esc}: {len(alumnos)} est., PPA prom={prom:.2f}")

stats = repo.estadisticas("ppa")
print(f"\nPPA: promedio={stats["promedio"]:.2f}, max={stats["max"]:.2f}, min={stats["min"]:.2f}")

# ── 3 consultas adaptadas al Proyecto Integrador (Tienda en Línea Local) ──
productos: Repositorio[Producto, str] = Repositorio(lambda p: p.codigo)
for p in [
    Producto("PRD-0001", "Teclado mecánico", 150.0, 10, "Periféricos"),
    Producto("PRD-0002", "Mouse inalámbrico", 45.5, 3, "Periféricos"),
    Producto("PRD-0003", "Licencia antivirus 1 año", 89.9, 50, "Software"),
    Producto("PRD-0004", "Monitor 24 pulgadas", 620.0, 2, "Pantallas"),
    Producto("PRD-0005", "Curso en línea de Python", 120.0, 100, "Software"),
]:
    productos.guardar(p)

# Consulta 1: productos con stock bajo (< 5 unidades) para reponer
bajo_stock = productos.filtrar(lambda p: p.stock < 5)
print(f"\nStock bajo: {[p.nombre for p in bajo_stock]}")

# Consulta 2: catálogo ordenado por precio (mayor a menor)
print("Catálogo por precio:")
for p in productos.ordenar(key=lambda p: p.precio, reverse=True):
    print(f"  {p.codigo} {p.nombre:<26} S/ {p.precio:8.2f}")

# Consulta 3: valor de inventario por categoría
print("Valor de inventario por categoría:")
for cat in sorted({p.categoria for p in productos}):
    valor = productos.acumular(0.0, lambda acc, p: acc + p.precio * p.stock if p.categoria == cat else acc)
    print(f"  {cat}: S/ {valor:.2f}")
