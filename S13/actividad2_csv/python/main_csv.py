
# SEMANA 13 - ACTIVIDAD 2
# PROGRAMA PRINCIPAL CSV.

# Importa el modelo Estudiante.
from estudiante import Estudiante

# Importa el repositorio CSV.
from repositorio_csv import RepositorioCSV


# Define el nombre del archivo CSV.
RUTA = "estudiantes.csv"


# Función principal.
def main():

    # Muestra el encabezado.
    print("====================================")
    print(" SISTEMA DE ESTUDIANTES - CSV")
    print("====================================")

    # Crea el repositorio.
    repositorio = RepositorioCSV(RUTA)

    # Registra al primer estudiante.
    repositorio.guardar(
        Estudiante(
            1001,
            "Ana Quispe",
            15.5,
            [14.0, 18.0, 14.5]
        )
    )

    # Registra al segundo estudiante.
    repositorio.guardar(
        Estudiante(
            1002,
            "Juan Mamani",
            16.0,
            [15.0, 17.0, 16.0]
        )
    )

    # Registra al tercer estudiante.
    repositorio.guardar(
        Estudiante(
            1003,
            "Rosa Flores",
            17.0,
            [16.0, 18.0, 17.0]
        )
    )
    repositorio.guardar(
            Estudiante(
                1004,
                "Ruben Meza",
                14.5,
                [13.0, 15.0, 15.5]
            )
        )

    # Muestra todos los estudiantes registrados.
    print("\nESTUDIANTES REGISTRADOS:")

    for estudiante in repositorio.listar():
        print(
            f"{estudiante.codigo} - "
            f"{estudiante.nombre} - "
            f"PPA: {estudiante.ppa}"
        )

    # Crea una segunda instancia del repositorio.
    # Esta instancia debe cargar los datos del CSV.
    repositorio2 = RepositorioCSV(RUTA)

    # Muestra los datos recuperados.
    print("\nDATOS RECUPERADOS DEL CSV:")

    for estudiante in repositorio2.listar():
        print(estudiante)

    # Muestra la cantidad recuperada.
    print(
        "\nTotal recuperado:",
        len(repositorio2.listar())
    )

    print("\nPRUEBA CSV FINALIZADA")


# Ejecuta la función principal.
if __name__ == "__main__":
    main()
