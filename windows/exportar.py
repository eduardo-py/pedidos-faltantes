
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QListWidget, QListWidgetItem, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
import sqlite3
import pandas as pd

class ExportarWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #ff4839;")
        self.setWindowTitle("Exportar Registros a Excel")
        self.resize(400, 300)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.combo_tabla = QComboBox()
        self.combo_tabla.addItems(["Pedidos", "Faltantes"])
        self.layout.addWidget(QLabel("¿Qué desea exportar?"))
        self.layout.addWidget(self.combo_tabla)

        self.layout.addWidget(QLabel("Filtrar por estado (seleccione uno o varios):"))
        self.lista_estados = QListWidget()
        self.lista_estados.setSelectionMode(QListWidget.MultiSelection)
        self.layout.addWidget(self.lista_estados)

        self.btn_exportar = QPushButton("Exportar a Excel")
        self.layout.addWidget(self.btn_exportar)

        self.btn_exportar.clicked.connect(self.exportar_excel)
        self.combo_tabla.currentIndexChanged.connect(self.cargar_estados)
        self.cargar_estados()

    def cargar_estados(self):
        self.lista_estados.clear()
        conn = sqlite3.connect("mi_base.db")
        estados = conn.execute("SELECT id_estados, nombre FROM estados ORDER BY nombre").fetchall()
        conn.close()
        for e in estados:
            item = QListWidgetItem(e[1])
            item.setData(Qt.UserRole, e[0])
            self.lista_estados.addItem(item)

    def exportar_excel(self):
        tipo = self.combo_tabla.currentText()
        estados_seleccionados = [
            item.data(Qt.UserRole)
            for item in self.lista_estados.selectedItems()
        ]

        conn = sqlite3.connect("mi_base.db")

        if tipo == "Pedidos":
            query = """
                SELECT p.detalle, p.nombre_cliente, p.numero_cliente, e.nombre AS estado, p.fecha, p.hora
                FROM pedidos_clientes p
                LEFT JOIN estados e ON p.id_estado = e.id_estados
            """
            if estados_seleccionados:
                placeholders = ",".join("?" for _ in estados_seleccionados)
                query += f" WHERE p.id_estado IN ({placeholders})"
                df = pd.read_sql_query(query, conn, params=estados_seleccionados)
            else:
                df = pd.read_sql_query(query, conn)

        elif tipo == "Faltantes":
            query = """
                SELECT f.detalle, pr.nombre AS proveedor, e.nombre AS estado, f.fecha, f.hora
                FROM faltantes_stock f
                LEFT JOIN proveedores pr ON f.proveedor_id = pr.id_proveedores
                LEFT JOIN estados e ON f.id_estado = e.id_estados
            """
            if estados_seleccionados:
                placeholders = ",".join("?" for _ in estados_seleccionados)
                query += f" WHERE f.id_estado IN ({placeholders})"
                df = pd.read_sql_query(query, conn, params=estados_seleccionados)
            else:
                df = pd.read_sql_query(query, conn)

        conn.close()

        if df.empty:
            QMessageBox.information(self, "Sin datos", "No se encontraron registros con los filtros seleccionados.")
            return

        nombre_archivo, _ = QFileDialog.getSaveFileName(self, "Guardar como", "", "Excel Files (*.xlsx)")
        if nombre_archivo:
            if not nombre_archivo.endswith(".xlsx"):
                nombre_archivo += ".xlsx"
            df.to_excel(nombre_archivo, index=False)
            QMessageBox.information(self, "Éxito", "Archivo exportado correctamente.")
