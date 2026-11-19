
# SEMANA 14 - ACTIVIDAD 1
# SISTEMA CRUD DE ESTUDIANTES CON TKINTER Y EXPORTACIÓN A EXCEL

# Importamos Tkinter para crear la interfaz gráfica.
import tkinter as tk

# Importamos ttk y messagebox para los componentes y mensajes.
from tkinter import ttk, messagebox

# Importamos el modelo Estudiante.
from estudiante import Estudiante

# Importamos el servicio que administra los estudiantes.
from servicio import ServicioEstudiante

# Importamos el repositorio que guarda los datos en JSON.
from repositorio_json import RepositorioJSON

# Importamos la estrategia para calcular el promedio.
from estrategias import PromedioSimple

# Importamos las herramientas para crear archivos Excel.
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill


# Creamos la clase principal de la aplicación.
class AppEstudiantes(tk.Tk):

    # Constructor de la ventana.
    def __init__(self):

        # Inicializamos la ventana de Tkinter.
        super().__init__()

        # Configuramos el título.
        self.title("Sistema de Gestión Académica")

        # Configuramos el tamaño de la ventana.
        self.geometry("820x620")

        # Evitamos cambiar el tamaño de la ventana.
        self.resizable(False, False)

        # Creamos el repositorio JSON.
        self.repositorio = RepositorioJSON("datos.json")

        # Creamos el servicio con el repositorio y la estrategia.
        self.servicio = ServicioEstudiante(
            self.repositorio,
            PromedioSimple()
        )

        # Creamos la interfaz gráfica.
        self.crear_interfaz()

        # Mostramos los estudiantes guardados.
        self.actualizar_lista()

    # Construye todos los componentes gráficos.
    def crear_interfaz(self):

        # Título principal.
        titulo = ttk.Label(
            self,
            text="REGISTRO DE ESTUDIANTES",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=15)

        # Marco para los datos del estudiante.
        formulario = ttk.LabelFrame(
            self,
            text="Datos del estudiante",
            padding=15
        )
        formulario.pack(fill="x", padx=20, pady=10)

        # Etiqueta y campo para el código.
        ttk.Label(formulario, text="Código:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.txt_codigo = ttk.Entry(formulario, width=25)
        self.txt_codigo.grid(row=0, column=1, padx=10)

        # Etiqueta y campo para el nombre.
        ttk.Label(formulario, text="Nombre:").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.txt_nombre = ttk.Entry(formulario, width=25)
        self.txt_nombre.grid(row=1, column=1, padx=10)

        # Etiqueta y campo para el PPA.
        ttk.Label(formulario, text="PPA:").grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.txt_ppa = ttk.Entry(formulario, width=25)
        self.txt_ppa.grid(row=2, column=1, padx=10)

        # Etiqueta y campo para las notas.
        ttk.Label(formulario, text="Notas (separadas por comas):").grid(
            row=3, column=0, sticky="w", pady=5
        )
        self.txt_notas = ttk.Entry(formulario, width=25)
        self.txt_notas.grid(row=3, column=1, padx=10)

        # Marco para los botones principales.
        botones = ttk.Frame(self)
        botones.pack(pady=10)

        # Botón para registrar.
        ttk.Button(
            botones,
            text="Registrar",
            command=self.registrar
        ).grid(row=0, column=0, padx=5)

        # Botón para actualizar.
        ttk.Button(
            botones,
            text="Actualizar",
            command=self.actualizar
        ).grid(row=0, column=1, padx=5)

        # Botón para eliminar.
        ttk.Button(
            botones,
            text="Eliminar",
            command=self.eliminar
        ).grid(row=0, column=2, padx=5)

        # Botón para limpiar.
        ttk.Button(
            botones,
            text="Limpiar",
            command=self.limpiar
        ).grid(row=0, column=3, padx=5)

        # Botón para exportar los estudiantes a Excel.
        ttk.Button(
            botones,
            text="Exportar a Excel",
            command=self.exportar_excel
        ).grid(row=0, column=4, padx=5)

        # Marco para buscar estudiantes.
        busqueda = ttk.LabelFrame(
            self,
            text="Buscar estudiante",
            padding=10
        )
        busqueda.pack(fill="x", padx=20, pady=5)

        # Campo para introducir el código de búsqueda.
        ttk.Label(busqueda, text="Código:").grid(
            row=0, column=0, padx=5
        )
        self.txt_buscar = ttk.Entry(busqueda, width=20)
        self.txt_buscar.grid(row=0, column=1, padx=5)

        # Botón para buscar.
        ttk.Button(
            busqueda,
            text="Buscar",
            command=self.buscar
        ).grid(row=0, column=2, padx=5)

        # Botón para mostrar todos.
        ttk.Button(
            busqueda,
            text="Mostrar todos",
            command=self.actualizar_lista
        ).grid(row=0, column=3, padx=5)

        # Marco de la lista de estudiantes.
        marco_lista = ttk.LabelFrame(
            self,
            text="Lista de estudiantes",
            padding=10
        )
        marco_lista.pack(fill="both", expand=True, padx=20, pady=10)

        # Creamos la lista visual.
        self.lista_estudiantes = tk.Listbox(
            marco_lista,
            height=12,
            width=95
        )
        self.lista_estudiantes.pack(
            fill="both",
            expand=True
        )

        # Detectamos cuando se selecciona un estudiante.
        self.lista_estudiantes.bind(
            "<<ListboxSelect>>",
            self.seleccionar_estudiante
        )

    # Obtiene los datos escritos en el formulario.
    def obtener_datos(self):

        # Leemos el código.
        codigo = int(self.txt_codigo.get())

        # Leemos el nombre.
        nombre = self.txt_nombre.get().strip()

        # Leemos las notas separadas por comas.
        notas = [
            float(nota.strip())
            for nota in self.txt_notas.get().split(",")
            if nota.strip()
        ]

        # Validamos que los campos estén completos.
        if not nombre or not notas:
            raise ValueError("Completa el nombre y las notas.")

        # Devolvemos un objeto Estudiante.
        return Estudiante(codigo, nombre, 0.0, notas)

    # Registra un estudiante nuevo.
    def registrar(self):

        try:
            # Obtenemos los datos del formulario.
            estudiante = self.obtener_datos()

            # Comprobamos que el código no exista.
            if self.servicio.buscar(estudiante.codigo) is not None:
                messagebox.showwarning(
                    "Aviso",
                    "Ya existe un estudiante con ese código."
                )
                return

            # Registramos al estudiante.
            self.servicio.registrar(estudiante)

            # Actualizamos la lista.
            self.actualizar_lista()

            # Mostramos confirmación.
            messagebox.showinfo(
                "Éxito",
                "Estudiante registrado correctamente."
            )

            # Limpiamos los campos.
            self.limpiar()

        except ValueError as error:
            messagebox.showerror("Error", str(error))

        except Exception as error:
            messagebox.showerror("Error", str(error))

    # Actualiza los datos de un estudiante.
    def actualizar(self):

        try:
            # Obtenemos los datos del formulario.
            estudiante = self.obtener_datos()

            # Comprobamos que el estudiante exista.
            if self.servicio.buscar(estudiante.codigo) is None:
                messagebox.showwarning(
                    "Aviso",
                    "No existe ese estudiante."
                )
                return

            # Actualizamos los datos.
            self.servicio.actualizar(estudiante)

            # Actualizamos la lista.
            self.actualizar_lista()

            # Mostramos confirmación.
            messagebox.showinfo(
                "Éxito",
                "Estudiante actualizado correctamente."
            )

            # Limpiamos los campos.
            self.limpiar()

        except ValueError as error:
            messagebox.showerror("Error", str(error))

        except Exception as error:
            messagebox.showerror("Error", str(error))

    # Elimina al estudiante indicado por su código.
    def eliminar(self):

        try:
            # Obtenemos el código.
            codigo = int(self.txt_codigo.get())

            # Solicitamos confirmación.
            confirmar = messagebox.askyesno(
                "Confirmar eliminación",
                "¿Deseas eliminar este estudiante?"
            )

            # Si el usuario cancela, no hacemos nada.
            if not confirmar:
                return

            # Eliminamos el estudiante.
            eliminado = self.servicio.eliminar(codigo)

            # Comprobamos si se eliminó.
            if eliminado is False:
                messagebox.showwarning(
                    "Aviso",
                    "No se encontró el estudiante."
                )
                return

            # Actualizamos la lista.
            self.actualizar_lista()

            # Mostramos confirmación.
            messagebox.showinfo(
                "Éxito",
                "Estudiante eliminado correctamente."
            )

            # Limpiamos los campos.
            self.limpiar()

        except ValueError:
            messagebox.showerror(
                "Error",
                "Introduce un código válido."
            )

        except Exception as error:
            messagebox.showerror("Error", str(error))

    # Busca un estudiante por código.
    def buscar(self):

        try:
            # Leemos el código de búsqueda.
            codigo = int(self.txt_buscar.get())

            # Buscamos al estudiante.
            estudiante = self.servicio.buscar(codigo)

            # Si no existe, mostramos un aviso.
            if estudiante is None:
                messagebox.showwarning(
                    "Búsqueda",
                    "Estudiante no encontrado."
                )
                return

            # Limpiamos la lista visual.
            self.lista_estudiantes.delete(0, tk.END)

            # Mostramos el estudiante encontrado.
            self.lista_estudiantes.insert(
                tk.END,
                f"{estudiante.codigo} - {estudiante.nombre} - "
                f"PPA: {estudiante.ppa:.2f} - Notas: {estudiante.notas}"
            )

        except ValueError:
            messagebox.showerror(
                "Error",
                "Introduce un código válido."
            )

    # Muestra todos los estudiantes del repositorio.
    def actualizar_lista(self):

        # Vaciamos la lista visual.
        self.lista_estudiantes.delete(0, tk.END)

        # Recuperamos todos los estudiantes.
        estudiantes = self.servicio.listar()

        # Recorremos los estudiantes.
        for estudiante in estudiantes:

            # Insertamos cada estudiante en la lista.
            self.lista_estudiantes.insert(
                tk.END,
                f"{estudiante.codigo} - {estudiante.nombre} - "
                f"PPA: {estudiante.ppa:.2f} - Notas: {estudiante.notas}"
            )

    # Carga los datos del estudiante seleccionado.
    def seleccionar_estudiante(self, evento):

        # Obtenemos la selección.
        seleccion = self.lista_estudiantes.curselection()

        # Comprobamos que exista una selección.
        if not seleccion:
            return

        # Obtenemos el índice seleccionado.
        indice = seleccion[0]

        # Recuperamos la lista de estudiantes.
        estudiantes = self.servicio.listar()

        # Obtenemos el estudiante seleccionado.
        estudiante = estudiantes[indice]

        # Limpiamos los campos.
        self.limpiar()

        # Colocamos el código.
        self.txt_codigo.insert(0, str(estudiante.codigo))

        # Colocamos el nombre.
        self.txt_nombre.insert(0, estudiante.nombre)

        # Colocamos el PPA.
        self.txt_ppa.insert(0, str(estudiante.ppa))

        # Colocamos las notas separadas por comas.
        self.txt_notas.insert(
            0,
            ",".join(str(nota) for nota in estudiante.notas)
        )

    # Limpia todos los campos del formulario.
    def limpiar(self):

        # Borramos el código.
        self.txt_codigo.delete(0, tk.END)

        # Borramos el nombre.
        self.txt_nombre.delete(0, tk.END)

        # Borramos el PPA.
        self.txt_ppa.delete(0, tk.END)

        # Borramos las notas.
        self.txt_notas.delete(0, tk.END)

        # Borramos el campo de búsqueda.
        self.txt_buscar.delete(0, tk.END)

        # Quitamos la selección de la lista.
        self.lista_estudiantes.selection_clear(0, tk.END)

    # Exporta todos los estudiantes a un archivo Excel.
    def exportar_excel(self):

        try:
            # Creamos un nuevo libro de Excel.
            libro = Workbook()

            # Seleccionamos la hoja activa.
            hoja = libro.active

            # Cambiamos el nombre de la hoja.
            hoja.title = "Estudiantes"

            # Escribimos los encabezados.
            hoja.append(["Código", "Nombre", "PPA", "Notas"])

            # Aplicamos formato a los encabezados.
            for celda in hoja[1]:
                celda.font = Font(bold=True, color="FFFFFF")
                celda.fill = PatternFill(
                    start_color="1F4E78",
                    end_color="1F4E78",
                    fill_type="solid"
                )

            # Recuperamos todos los estudiantes.
            estudiantes = self.servicio.listar()

            # Recorremos la lista de estudiantes.
            for estudiante in estudiantes:

                # Convertimos las notas en texto.
                notas = ", ".join(
                    str(nota) for nota in estudiante.notas
                )

                # Agregamos los datos del estudiante a Excel.
                hoja.append([
                    estudiante.codigo,
                    estudiante.nombre,
                    estudiante.ppa,
                    notas
                ])

            # Ajustamos el ancho de las columnas.
            hoja.column_dimensions["A"].width = 15
            hoja.column_dimensions["B"].width = 25
            hoja.column_dimensions["C"].width = 15
            hoja.column_dimensions["D"].width = 35

            # Guardamos el archivo Excel.
            libro.save("estudiantes.xlsx")

            # Mostramos un mensaje de confirmación.
            messagebox.showinfo(
                "Exportación exitosa",
                "Los estudiantes fueron exportados correctamente "
                "al archivo estudiantes.xlsx"
            )

        except Exception as error:

            # Mostramos cualquier error que ocurra.
            messagebox.showerror(
                "Error al exportar",
                str(error)
            )


# Punto de entrada del programa.
if __name__ == "__main__":

    # Creamos la aplicación.
    app = AppEstudiantes()

    # Iniciamos el ciclo de eventos de Tkinter.
    app.mainloop()
