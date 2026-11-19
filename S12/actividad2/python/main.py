
# =====================================================
# SEMANA 12 - ACTIVIDAD 1
# PATRON OBSERVER - PYTHON 3.12
# Sistema de notificaciones de estudiantes.
# =====================================================

# Importa la clase Estudiante.
from estudiante import Estudiante

# Importa los observadores y el repositorio.
from observer import (
    RepositorioObservable,
    LoggerObserver,
    ConsolaObserver
)

# Importa el servicio de estudiantes.
from servicio_estudiante import ServicioEstudiante


# =====================================================
# FUNCION PRINCIPAL
# =====================================================

def main():

    # Muestra el encabezado del programa.
    print("=" * 45)
    print(" SISTEMA OBSERVER - UNAP (PYTHON)")
    print("=" * 45)

    # Crea el repositorio observable.
    repositorio = RepositorioObservable()

    # Crea los dos observadores.
    logger = LoggerObserver()
    consola = ConsolaObserver()

    # Suscribe los observadores al repositorio.
    repositorio.suscribir(logger)
    repositorio.suscribir(consola)

    # Crea el servicio y le entrega el repositorio.
    servicio = ServicioEstudiante(repositorio)

    # Crea el primer estudiante.
    estudiante1 = Estudiante(
        codigo=1001,
        nombre="Ana Quispe",
        ppa=15.5,
        ciclo=3
    )

    # Crea el segundo estudiante.
    estudiante2 = Estudiante(
        codigo=1002,
        nombre="Luis Mamani",
        ppa=16.8,
        ciclo=4
    )

    # Registra al primer estudiante.
    servicio.registrar(estudiante1)

    # Registra al segundo estudiante.
    servicio.registrar(estudiante2)

    # Consulta al estudiante con código 1001.
    servicio.consultar(1001)

    # Muestra el total de estudiantes registrados.
    print(
        "\nTotal de estudiantes registrados:",
        servicio.total_estudiantes()
    )

    # Indica que la prueba terminó.
    print("\nPRUEBA OBSERVER FINALIZADA")


# Ejecuta main cuando se inicia este archivo.
if __name__ == "__main__":
    main()
