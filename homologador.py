from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QRadioButton, QPushButton, QVBoxLayout, QHBoxLayout,
    QTextEdit, QMessageBox, QFrame
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
import sys
import pandas as pd

class HomologadorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Homologador SOAT - CUPS")
        self.setGeometry(100, 100, 950, 600)
        self.setStyleSheet(self.get_stylesheet())
        self.df_principal = self.cargar_excel_principal()
        self.init_ui()

    def get_stylesheet(self):
        return """
            QWidget {
                background-color: #1E1E1E; /* Fondo principal oscuro (VS Code) */
                color: #D4D4D4; /* Color de texto principal (VS Code) */
                font-family: "Segoe UI", sans-serif;
                font-size: 14px;
            }
            QLabel {
                color: #D4D4D4;
            }
            QLineEdit {
                background-color: #252526; /* Fondo de input (VS Code) */
                color: #D4D4D4;
                border: 1px solid #3B3B3B;
                border-radius: 4px;
                padding: 8px;
            }
            QLineEdit::placeholder {
                color: #808080;
            }
            QRadioButton {
                color: #D4D4D4;
            }
            QPushButton {
                background-color: #007ACC; /* Azul de acento (VS Code) */
                color: #FFFFFF;
                border: none;
                border-radius: 4px;
                padding: 10px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0067A6;
            }
            QTextEdit {
                background-color: #252526; /* Fondo de textarea (VS Code) */
                color: #D4D4D4;
                border: 1px solid #3B3B3B;
                border-radius: 4px;
                padding: 10px;
                font-family: "Consolas", monospace;
                font-size: 16px; /* Aumento del tamaño de la fuente */
            }
            QFrame#search_panel, QFrame#results_panel {
                background-color: #1E1E1E; /* Fondo de panel (VS Code) */
                border-radius: 6px;
                padding: 15px;
                margin-bottom: 10px;
                border: 1px solid #3B3B3B; /* Borde sutil para los paneles */
            }
            QLabel#results_label {
                font-weight: bold;
                margin-bottom: 8px;
            }
        """

    def cargar_excel_principal(self):
        try:
            columnas_necesarias = ['CUPS', 'SOAT', 'Denominacion', 'NOMBRE', 'GRUPO QX', 'SERVICIO']
            df = pd.read_excel("HOMOLOGAR.xlsm", sheet_name="homologo soat -iss", usecols=columnas_necesarias)
            df['CUPS'] = df['CUPS'].astype(str).str.strip()
            df['SOAT'] = df['SOAT'].apply(lambda x: str(int(x)) if isinstance(x, float) and not pd.isna(x) else str(x)).astype(str).str.strip()
            df['NOMBRE'] = df['NOMBRE'].astype(str).str.strip()  # Limpiar columna NOMBRE
            return df
        except Exception as e:
            QMessageBox.critical(self, "Error al cargar", f"No se pudo cargar el archivo HOMOLOGAR.xlsm: {e}")
            return pd.DataFrame()

    def init_ui(self):
        font_titulo = QFont("Segoe UI", 28, QFont.Weight.Bold)
        font_subtitulo = QFont("Segoe UI", 18)
        font_label = QFont("Segoe UI", 14)
        font_resultados = QFont("Consolas", 16)  # Nueva fuente para resultados

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        header_layout = QHBoxLayout()
        titulo = QLabel("Homologador")
        titulo.setFont(font_titulo)
        subtitulo = QLabel("SOAT - CUPS")
        subtitulo.setFont(font_subtitulo)
        header_layout.addWidget(titulo)
        header_layout.addWidget(subtitulo)
        header_layout.setAlignment(titulo, Qt.AlignmentFlag.AlignLeft)
        header_layout.setAlignment(subtitulo, Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(header_layout)

        search_panel = QFrame()
        search_panel.setObjectName("search_panel")
        search_input_layout = QVBoxLayout()
        search_label = QLabel("Ingrese CUPS, SOAT o Nombre del Procedimiento:")
        search_label.setFont(font_label)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ej: 12345, ABCDE o Nombre del Procedimiento")
        self.search_input.setFont(font_label)  # Aplicar fuente a la entrada
        radio_layout = QHBoxLayout()
        self.radio_cups = QRadioButton("Buscar por CUPS")
        self.radio_cups.setFont(font_label)
        self.radio_cups.setChecked(True)
        self.radio_soat = QRadioButton("Buscar por SOAT")
        self.radio_soat.setFont(font_label)
        self.radio_nombre = QRadioButton("Buscar por Nombre del Procedimiento")  # Nuevo botón
        self.radio_nombre.setFont(font_label)
        radio_layout.addWidget(self.radio_cups)
        radio_layout.addWidget(self.radio_soat)
        radio_layout.addWidget(self.radio_nombre)
        radio_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        buscar_button = QPushButton("Buscar")
        buscar_button.setFont(font_label)
        buscar_button.clicked.connect(self.buscar)
        search_input_layout.addWidget(search_label)
        search_input_layout.addWidget(self.search_input)
        search_input_layout.addLayout(radio_layout)
        search_input_layout.addWidget(buscar_button)
        search_panel.setLayout(search_input_layout)
        main_layout.addWidget(search_panel)

        results_panel = QFrame()
        results_panel.setObjectName("results_panel")
        results_layout = QVBoxLayout()
        results_label = QLabel("Resultados:")
        results_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        results_label.setObjectName("results_label")
        self.resultados_text = QTextEdit()
        self.resultados_text.setReadOnly(True)
        self.resultados_text.setPlaceholderText("Los resultados de la búsqueda se mostrarán aquí.")
        self.resultados_text.setFont(font_resultados)  # Aplicar fuente más grande a los resultados
        results_layout.addWidget(results_label)
        results_layout.addWidget(self.resultados_text)
        results_panel.setLayout(results_layout)
        main_layout.addWidget(results_panel)

        self.setLayout(main_layout)

    def realizar_busqueda(self, valor, buscar_por):
        try:
            if buscar_por == "CUPS":
                return self.df_principal[self.df_principal['CUPS'].str.strip().str.upper() == valor.upper()]
            elif buscar_por == "SOAT":
                return self.df_principal[self.df_principal['SOAT'].str.strip().str.upper() == valor.upper()]
            elif buscar_por == "NOMBRE":
                return self.df_principal[self.df_principal['NOMBRE'].str.strip().str.upper().str.contains(valor.upper(), na=False)]
        except KeyError as e:
            QMessageBox.critical(self, "Error", f"Columna no encontrada en el archivo: {e}")
            return pd.DataFrame()

    def buscar(self):
        if self.df_principal.empty:
            self.resultados_text.setText("No se cargó el archivo HOMOLOGAR.xlsm.")
            return

        valor = self.search_input.text().strip()
        buscar_por = (
            "CUPS" if self.radio_cups.isChecked() else
            "SOAT" if self.radio_soat.isChecked() else
            "NOMBRE"
        )

        if not valor:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingrese un código o nombre para buscar.")
            return

        resultado = self.realizar_busqueda(valor, buscar_por)

        if resultado.empty:
            self.resultados_text.setText(f"No se encontró ningún registro para {buscar_por}: {valor}.")
        else:
            texto_resultado = "\n".join(
                f"Denominación: {info['Denominacion']}\n"
                f"Nombre: {info['NOMBRE']}\n"
                f"CUPS: {info['CUPS']}\n"
                f"SOAT: {info['SOAT']}\n"
                f"Grupo QX: {info['GRUPO QX']}\n"
                f"Servicio: {info['SERVICIO']}\n"
                f"{'-'*60}"
                for _, info in resultado.iterrows()
            )
            self.resultados_text.setText(texto_resultado)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HomologadorApp()
    window.show()
    sys.exit(app.exec())