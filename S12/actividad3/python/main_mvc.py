
# ACTIVIDAD 3 - MVC COMPLETO CON OBSERVER Y STRATEGY
# Programa principal: conecta todos los componentes.

# Importa el modelo Estudiante.
from estudiante import Estudiante

# Importa el repositorio en memoria.
from repositorio_memoria import RepositorioMemoria

# Importa el repositorio observable y los observadores.
from observer import (
    RepositorioObservable,
    ConsolaObservador,
    LoggerObservador
)

# Importa las dos estrategias de promedio.
from estrategias import PromedioSimple, PromedioModerado

# Importa el controlador.
from servicio_estudiante import ServicioEstudiante


def main():
    # Muestra el encabezado del programa.
    print("======================================")
    print(" SISTEMA MVC - OBSERVER - STRATEGY")
    print("======================================")

    # Crea el repositorio que almacena los estudiantes.
    repositorio_base = RepositorioMemoria()

    # Envuelve el repositorio para agregar notificaciones Observer.
    repositorio = RepositorioObservable(repositorio_base)

    # Crea los dos observadores.
    vista = ConsolaObservador()
    logger = LoggerObservador()

    # Suscribe ambos observadores.
    repositorio.suscribir(vista)
    repositorio.suscribir(logger)

    # Crea el controlador con la estrategia de promedio simple.
    servicio = ServicioEstudiante(
        repositorio,
        PromedioSimple()
    )

    # Crea los tres estudiantes iniciales.
    estudiantes = [
        Estudiante(1001, "Ana Quispe", [15.0, 16.0, 17.0], ciclo=3),
        Estudiante(1002, "Luis Mamani", [14.0, 15.0, 16.0], ciclo=4),
        Estudiante(1003, "Rosa Flores", [18.0, 17.0, 16.0], ciclo=5)
    ]

    # Registra cada estudiante.
    print("\n--- REGISTRO INICIAL ---")
    for estudiante in estudiantes:
        servicio.registrar(estudiante)

    # Muestra el total de estudiantes registrados.
    print("\nTotal registrados:", servicio.total_estudiantes())

    # Agrega un cuarto estudiante con tres notas de 5.0.
    print("\n--- CUARTO ESTUDIANTE ---")
    estudiante4 = Estudiante(
        1004,
        "Pedro Mamani",
        [5.0, 5.0, 5.0],
        ciclo=2
    )
    servicio.registrar(estudiante4)

    # Consulta el PPA del cuarto estudiante.
    encontrado = servicio.consultar(1004)
    print(f"PPA de {encontrado.nombre}: {encontrado.ppa:.1f}")

    # Cambia la estrategia de promedio simple a moderado.
    print("\n--- CAMBIO DE ESTRATEGIA ---")
    servicio.cambiar_estrategia(PromedioModerado())

    # Crea un estudiante de prueba para comparar estrategias.
    prueba = Estudiante(
        1005,
        "Estudiante de Prueba",
        [10.0, 15.0, 20.0],
        ciclo=2
    )

    # Registra usando la estrategia moderada.
    servicio.registrar(prueba)

    # Muestra el resultado del promedio moderado.
    print(f"PPA con PromedioModerado: {prueba.ppa:.1f}")

    # Finaliza la prueba.
    print("\nPRUEBA MVC FINALIZADA")


# Ejecuta main() cuando este archivo se inicia directamente.
if __name__ == "__main__":
    main()
