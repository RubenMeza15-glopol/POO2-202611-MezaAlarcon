
# SEMANA 14 - ACTIVIDAD 1
# SISTEMA CRUD DE ESTUDIANTES CON PYQT5
# EXPORTACION E IMPORTACION DE EXCEL

import sys

# Componentes graficos de PyQt5.
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGroupBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QFileDialog
)

# Modelo, servicio, repositorio y estrategia.
from estudiante import Estudiante
from servicio import ServicioEstudiante
from repositorio_json import RepositorioJSON
from estrategias import PromedioSimple

# Herramientas para trabajar con Excel.
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill


class AppEstudiantes(QMainWindow):

    def __init__(self):
        super().__init__()

        # Configuracion de la ventana.
        self.setWindowTitle("Sistema de Gestion Academica - PyQt5")
        self.setGeometry(100, 100, 900, 650)

        # Creamos el repositorio y el servicio.
        self.repositorio = RepositorioJSON("datos.json")
        self.servicio = ServicioEstudiante(
            self.repositorio,
            PromedioSimple()
        )

        # Construimos la interfaz.
        self.crear_interfaz()

        # Cargamos los estudiantes guardados.
        self.actualizar_lista()

    # Construye la interfaz grafica.
    def crear_interfaz(self):

        central = QWidget()
        self.setCentralWidget(central)

        principal = QVBoxLayout(central)

        # Titulo principal.
        titulo = QLabel("REGISTRO DE ESTUDIANTES")
        titulo.setStyleSheet(
            "font-size: 22px; font-weight: bold; padding: 12px;"
        )
        principal.addWidget(titulo)

        # Formulario de estudiantes.
        grupo = QGroupBox("Datos del estudiante")
        formulario = QFormLayout()

        self.txt_codigo = QLineEdit()
        formulario.addRow("Codigo:", self.txt_codigo)

        self.txt_nombre = QLineEdit()
        formulario.addRow("Nombre:", self.txt_nombre)

        self.txt_ppa = QLineEdit()
        self.txt_ppa.setReadOnly(True)
        formulario.addRow("PPA calculado:", self.txt_ppa)

        self.txt_notas = QLineEdit()
        self.txt_notas.setPlaceholderText("Ejemplo: 15, 18, 14")
        formulario.addRow("Notas:", self.txt_notas)

        grupo.setLayout(formulario)
        principal.addWidget(grupo)

        # Botones principales.
        botones = QHBoxLayout()

        btn_registrar = QPushButton("Registrar")
        btn_registrar.clicked.connect(self.registrar)
        botones.addWidget(btn_registrar)

        btn_actualizar = QPushButton("Actualizar")
        btn_actualizar.clicked.connect(self.actualizar)
        botones.addWidget(btn_actualizar)

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self.eliminar)
        botones.addWidget(btn_eliminar)

        btn_limpiar = QPushButton("Limpiar")
        btn_limpiar.clicked.connect(self.limpiar)
        botones.addWidget(btn_limpiar)

        btn_excel = QPushButton("Exportar a Excel")
        btn_excel.clicked.connect(self.exportar_excel)
        botones.addWidget(btn_excel)

        btn_importar = QPushButton("Importar desde Excel")
        btn_importar.clicked.connect(self.importar_excel)
        botones.addWidget(btn_importar)

        principal.addLayout(botones)

        # Seccion de busqueda.
        grupo_busqueda = QGroupBox("Buscar estudiante")
        busqueda = QHBoxLayout()

        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText("Codigo del estudiante")
        busqueda.addWidget(self.txt_buscar)

        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar)
        busqueda.addWidget(btn_buscar)

        btn_mostrar = QPushButton("Mostrar todos")
        btn_mostrar.clicked.connect(self.actualizar_lista)
        busqueda.addWidget(btn_mostrar)

        grupo_busqueda.setLayout(busqueda)
        principal.addWidget(grupo_busqueda)

        # Tabla de estudiantes.
        grupo_lista = QGroupBox("Lista de estudiantes")
        lista = QVBoxLayout()

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(
            ["Codigo", "Nombre", "PPA", "Notas"]
        )

        self.tabla.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.tabla.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.tabla.itemSelectionChanged.connect(
            self.seleccionar_estudiante
        )

        lista.addWidget(self.tabla)
        grupo_lista.setLayout(lista)
        principal.addWidget(grupo_lista)

    # Obtiene los datos escritos en el formulario.
    def obtener_datos(self):

        codigo = int(self.txt_codigo.text())
        nombre = self.txt_nombre.text().strip()

        notas = [
            float(nota.strip())
            for nota in self.txt_notas.text().split(",")
            if nota.strip()
        ]

        if not nombre or not notas:
            raise ValueError("Completa el nombre y las notas.")

        # Comprueba que las notas sean validas.
        if any(nota < 0 or nota > 20 for nota in notas):
            raise ValueError("Las notas deben estar entre 0 y 20.")

        return Estudiante(codigo, nombre, 0.0, notas)

    # Registra un estudiante.
    def registrar(self):

        try:
            estudiante = self.obtener_datos()

            if self.servicio.buscar(estudiante.codigo) is not None:
                QMessageBox.warning(
                    self, "Aviso",
                    "Ya existe un estudiante con ese codigo."
                )
                return

            self.servicio.registrar(estudiante)
            self.actualizar_lista()

            QMessageBox.information(
                self, "Exito",
                "Estudiante registrado correctamente."
            )

            self.limpiar()

        except ValueError as error:
            QMessageBox.warning(self, "Error", str(error))

        except Exception as error:
            QMessageBox.critical(self, "Error", str(error))

    # Actualiza un estudiante.
    def actualizar(self):

        try:
            estudiante = self.obtener_datos()

            if self.servicio.buscar(estudiante.codigo) is None:
                QMessageBox.warning(
                    self, "Aviso",
                    "No existe ese estudiante."
                )
                return

            self.servicio.actualizar(estudiante)
            self.actualizar_lista()

            QMessageBox.information(
                self, "Exito",
                "Estudiante actualizado correctamente."
            )

            self.limpiar()

        except ValueError as error:
            QMessageBox.warning(self, "Error", str(error))

        except Exception as error:
            QMessageBox.critical(self, "Error", str(error))

    # Elimina un estudiante.
    def eliminar(self):

        try:
            codigo = int(self.txt_codigo.text())

            respuesta = QMessageBox.question(
                self,
                "Confirmar",
                "Deseas eliminar este estudiante?",
                QMessageBox.Yes | QMessageBox.No
            )

            if respuesta != QMessageBox.Yes:
                return

            eliminado = self.servicio.eliminar(codigo)

            if eliminado is False:
                QMessageBox.warning(
                    self, "Aviso",
                    "No se encontro el estudiante."
                )
                return

            self.actualizar_lista()

            QMessageBox.information(
                self, "Exito",
                "Estudiante eliminado correctamente."
            )

            self.limpiar()

        except ValueError:
            QMessageBox.warning(
                self, "Error",
                "Introduce un codigo valido."
            )

        except Exception as error:
            QMessageBox.critical(self, "Error", str(error))

    # Busca un estudiante por codigo.
    def buscar(self):

        try:
            codigo = int(self.txt_buscar.text())
            estudiante = self.servicio.buscar(codigo)

            if estudiante is None:
                QMessageBox.information(
                    self, "Busqueda",
                    "Estudiante no encontrado."
                )
                return

            self.mostrar_estudiantes([estudiante])

        except ValueError:
            QMessageBox.warning(
                self, "Error",
                "Introduce un codigo valido."
            )

    # Recupera todos los estudiantes.
    def actualizar_lista(self):

        estudiantes = self.servicio.listar()
        self.mostrar_estudiantes(estudiantes)

    # Muestra los estudiantes en la tabla.
    def mostrar_estudiantes(self, estudiantes):

        self.tabla.setRowCount(0)

        for estudiante in estudiantes:

            fila = self.tabla.rowCount()
            self.tabla.insertRow(fila)

            self.tabla.setItem(
                fila, 0,
                QTableWidgetItem(str(estudiante.codigo))
            )

            self.tabla.setItem(
                fila, 1,
                QTableWidgetItem(estudiante.nombre)
            )

            self.tabla.setItem(
                fila, 2,
                QTableWidgetItem(f"{estudiante.ppa:.2f}")
            )

            self.tabla.setItem(
                fila, 3,
                QTableWidgetItem(str(estudiante.notas))
            )

        self.tabla.resizeColumnsToContents()

    # Carga los datos del estudiante seleccionado.
    def seleccionar_estudiante(self):

        fila = self.tabla.currentRow()

        if fila < 0:
            return

        codigo = int(self.tabla.item(fila, 0).text())
        estudiante = self.servicio.buscar(codigo)

        if estudiante is None:
            return

        self.txt_codigo.setText(str(estudiante.codigo))
        self.txt_nombre.setText(estudiante.nombre)
        self.txt_ppa.setText(str(estudiante.ppa))

        self.txt_notas.setText(
            ",".join(str(nota) for nota in estudiante.notas)
        )

    # Limpia el formulario.
    def limpiar(self):

        self.txt_codigo.clear()
        self.txt_nombre.clear()
        self.txt_ppa.clear()
        self.txt_notas.clear()
        self.txt_buscar.clear()
        self.tabla.clearSelection()

    # Exporta los estudiantes a Excel.
    def exportar_excel(self):

        try:
            libro = Workbook()
            hoja = libro.active
            hoja.title = "Estudiantes"

            # Encabezados.
            hoja.append(["Codigo", "Nombre", "PPA", "Notas"])

            # Formato de los encabezados.
            for celda in hoja[1]:
                celda.font = Font(bold=True, color="FFFFFF")
                celda.fill = PatternFill(
                    start_color="1F4E78",
                    end_color="1F4E78",
                    fill_type="solid"
                )

            estudiantes = self.servicio.listar()

            for estudiante in estudiantes:

                notas = ", ".join(
                    str(nota) for nota in estudiante.notas
                )

                hoja.append([
                    estudiante.codigo,
                    estudiante.nombre,
                    estudiante.ppa,
                    notas
                ])

            # Ancho de las columnas.
            hoja.column_dimensions["A"].width = 15
            hoja.column_dimensions["B"].width = 25
            hoja.column_dimensions["C"].width = 15
            hoja.column_dimensions["D"].width = 35

            libro.save("estudiantes.xlsx")
            libro.close()

            QMessageBox.information(
                self,
                "Exportacion",
                "Archivo estudiantes.xlsx creado correctamente."
            )

        except PermissionError:
            QMessageBox.warning(
                self,
                "Archivo ocupado",
                "Cierra estudiantes.xlsx en Excel e intenta nuevamente."
            )

        except Exception as error:
            QMessageBox.critical(
                self, "Error al exportar", str(error)
            )

    # Importa estudiantes desde un archivo Excel.
    def importar_excel(self):

        libro = None

        try:
            # Abre el selector de archivos.
            ruta, _ = QFileDialog.getOpenFileName(
                self,
                "Seleccionar archivo Excel",
                "",
                "Archivos Excel (*.xlsx)"
            )

            # Si no selecciona archivo, termina.
            if not ruta:
                return

            # Abre el archivo seleccionado.
            libro = load_workbook(ruta, data_only=True)
            hoja = libro.active

            # Contadores de importacion.
            importados = 0
            omitidos = 0

            # Recorre las filas desde la segunda.
            for numero_fila, fila in enumerate(
                hoja.iter_rows(min_row=2, values_only=True),
                start=2
            ):

                # Ignora filas completamente vacias.
                if not fila or all(valor is None for valor in fila):
                    continue

                # Verifica que existan las cuatro columnas.
                if len(fila) < 4:
                    raise ValueError(
                        f"Faltan columnas en la fila {numero_fila}."
                    )

                codigo, nombre, ppa_excel, notas_excel = fila[:4]

                # Comprueba los datos obligatorios.
                if codigo is None or nombre is None or notas_excel is None:
                    raise ValueError(
                        f"Hay datos incompletos en la fila {numero_fila}."
                    )

                # Convierte las notas en una lista numerica.
                if isinstance(notas_excel, str):
                    notas = [
                        float(n.strip())
                        for n in notas_excel.split(",")
                        if n.strip()
                    ]
                else:
                    notas = [float(notas_excel)]

                if not notas:
                    raise ValueError(
                        f"No hay notas en la fila {numero_fila}."
                    )

                if any(nota < 0 or nota > 20 for nota in notas):
                    raise ValueError(
                        f"Hay una nota fuera del rango 0 a 20 "
                        f"en la fila {numero_fila}."
                    )

                # Comprueba si el codigo ya existe.
                if self.servicio.buscar(int(codigo)) is not None:
                    omitidos += 1
                    continue

                # Crea el objeto estudiante.
                estudiante = Estudiante(
                    int(codigo),
                    str(nombre),
                    0.0,
                    notas
                )

                # Registra mediante el servicio.
                # El servicio calcula nuevamente el PPA.
                self.servicio.registrar(estudiante)

                importados += 1

            # Cerramos el archivo Excel.
            libro.close()
            libro = None

            # Actualizamos la tabla.
            self.actualizar_lista()

            # Mostramos el resultado.
            QMessageBox.information(
                self,
                "Importacion finalizada",
                f"Estudiantes importados: {importados}\n"
                f"Registros omitidos por codigo repetido: {omitidos}"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error de importacion",
                str(error)
            )

        finally:
            if libro is not None:
                libro.close()


# Punto de entrada del programa.
if __name__ == "__main__":

    # Creamos la aplicacion.
    aplicacion = QApplication(sys.argv)

    # Creamos la ventana principal.
    ventana = AppEstudiantes()

    # Mostramos la ventana.
    ventana.show()

    # Iniciamos el ciclo de eventos.
    sys.exit(aplicacion.exec_())
