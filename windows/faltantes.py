
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from windows.faltante_form import FaltanteForm
import db

class FaltantesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #ff4839;")
        self.setWindowTitle("Faltantes de Stock")
        self.resize(1000, 450)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        btn_layout = QHBoxLayout()
        self.btn_nuevo = QPushButton("Nuevo Faltante")
        self.btn_editar = QPushButton("Editar Seleccionado")
        self.btn_eliminar = QPushButton("Eliminar Seleccionado")

        self.btn_nuevo.clicked.connect(self.abrir_formulario_nuevo)
        self.btn_editar.clicked.connect(self.editar_faltante)
        self.btn_eliminar.clicked.connect(self.eliminar_faltante)

        btn_layout.addWidget(self.btn_nuevo)
        btn_layout.addWidget(self.btn_editar)
        btn_layout.addWidget(self.btn_eliminar)

        self.layout.addLayout(btn_layout)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["ID", "Detalle", "Proveedor", "Estado", "Fecha", "Hora"])
        self.layout.addWidget(self.tabla)

        self.cargar_faltantes()

    def cargar_faltantes(self):
        self.tabla.setRowCount(0)
        conn = db.conectar()
        query = """
            SELECT f.id_faltante, f.detalle, p.nombre AS proveedor, e.nombre AS estado, f.fecha, f.hora
            FROM faltantes_stock f
            LEFT JOIN proveedores p ON f.proveedor_id = p.id_proveedores
            LEFT JOIN estados e ON f.id_estado = e.id_estados
            ORDER BY f.id_faltante DESC
        """
        faltantes = conn.execute(query).fetchall()
        conn.close()

        self.tabla.setRowCount(len(faltantes))
        for row_idx, faltante in enumerate(faltantes):
            self.tabla.setItem(row_idx, 0, QTableWidgetItem(str(faltante["id_faltante"])))
            self.tabla.setItem(row_idx, 1, QTableWidgetItem(faltante["detalle"]))
            self.tabla.setItem(row_idx, 2, QTableWidgetItem(faltante["proveedor"] or ""))
            self.tabla.setItem(row_idx, 3, QTableWidgetItem(faltante["estado"] or ""))
            self.tabla.setItem(row_idx, 4, QTableWidgetItem(faltante["fecha"] or ""))
            self.tabla.setItem(row_idx, 5, QTableWidgetItem(faltante["hora"] or ""))

        self.tabla.resizeColumnsToContents()

    def abrir_formulario_nuevo(self):
        self.formulario = FaltanteForm()
        self.formulario.show()
        self.formulario.closed.connect(self.cargar_faltantes)

    def editar_faltante(self):
        fila = self.tabla.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Atención", "Seleccione un faltante para editar.")
            return
        id_faltante = int(self.tabla.item(fila, 0).text())
        self.formulario = FaltanteForm(id_faltante=id_faltante)
        self.formulario.show()
        self.formulario.closed.connect(self.cargar_faltantes)

    def eliminar_faltante(self):
        fila = self.tabla.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Atención", "Seleccione un faltante para eliminar.")
            return
        id_faltante = int(self.tabla.item(fila, 0).text())
        confirmar = QMessageBox.question(self, "Eliminar", "¿Estás seguro de eliminar este faltante?",
                                         QMessageBox.Yes | QMessageBox.No)
        if confirmar == QMessageBox.Yes:
            conn = db.conectar()
            conn.execute("DELETE FROM faltantes_stock WHERE id_faltante = ?", (id_faltante,))
            conn.commit()
            conn.close()
            self.cargar_faltantes()
