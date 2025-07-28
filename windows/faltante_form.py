
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit,
    QComboBox, QMessageBox, QDateEdit, QTimeEdit
)
from PyQt5.QtCore import pyqtSignal, QDate, QTime
import db

class FaltanteForm(QWidget):
    closed = pyqtSignal()

    def __init__(self, id_faltante=None):
        super().__init__()
        self.setStyleSheet("background-color: #ff4839;")
        self.id_faltante = id_faltante
        self.setWindowTitle("Editar Faltante" if id_faltante else "Nuevo Faltante de Stock")
        self.layout = QVBoxLayout()

        self.detalle = QTextEdit()
        self.proveedor = QComboBox()
        self.estado = QComboBox()
        self.fecha = QDateEdit(calendarPopup=True)
        self.hora = QTimeEdit()

        self.fecha.setDate(QDate.currentDate())
        self.hora.setTime(QTime.currentTime())

        self.layout.addWidget(QLabel("Detalle del Faltante:"))
        self.layout.addWidget(self.detalle)
        self.layout.addWidget(QLabel("Proveedor:"))
        self.layout.addWidget(self.proveedor)
        self.layout.addWidget(QLabel("Estado:"))
        self.layout.addWidget(self.estado)
        self.layout.addWidget(QLabel("Fecha:"))
        self.layout.addWidget(self.fecha)
        self.layout.addWidget(QLabel("Hora:"))
        self.layout.addWidget(self.hora)

        self.btn_guardar = QPushButton("Guardar")
        self.layout.addWidget(self.btn_guardar)
        self.setLayout(self.layout)

        self.btn_guardar.clicked.connect(self.guardar_faltante)
        self.cargar_proveedores()
        self.cargar_estados()

        if self.id_faltante:
            self.cargar_datos()

    def cargar_proveedores(self):
        self.proveedor.clear()
        conn = db.conectar()
        proveedores = conn.execute("SELECT id_proveedores, nombre FROM proveedores ORDER BY nombre").fetchall()
        self.proveedor.addItem("Seleccionar...", -1)
        for p in proveedores:
            self.proveedor.addItem(p["nombre"], p["id_proveedores"])
        conn.close()

    def cargar_estados(self):
        self.estado.clear()
        conn = db.conectar()
        estados = conn.execute("SELECT id_estados, nombre FROM estados ORDER BY nombre").fetchall()
        self.estado.addItem("Seleccionar...", -1)
        for est in estados:
            self.estado.addItem(est["nombre"], est["id_estados"])
        conn.close()

    def cargar_datos(self):
        conn = db.conectar()
        query = "SELECT * FROM faltantes_stock WHERE id_faltante = ?"
        faltante = conn.execute(query, (self.id_faltante,)).fetchone()
        conn.close()

        self.detalle.setPlainText(faltante["detalle"])
        self.fecha.setDate(QDate.fromString(faltante["fecha"], "yyyy-MM-dd"))
        self.hora.setTime(QTime.fromString(faltante["hora"], "HH:mm:ss"))

        index_estado = self.estado.findData(faltante["id_estado"])
        index_prov = self.proveedor.findData(faltante["proveedor_id"])
        self.estado.setCurrentIndex(index_estado if index_estado != -1 else 0)
        self.proveedor.setCurrentIndex(index_prov if index_prov != -1 else 0)

    def guardar_faltante(self):
        detalle = self.detalle.toPlainText().strip()
        proveedor_id = self.proveedor.currentData()
        estado_id = self.estado.currentData()
        fecha = self.fecha.date().toString("yyyy-MM-dd")
        hora = self.hora.time().toString("HH:mm:ss")

        if not detalle or proveedor_id == -1 or estado_id == -1:
            QMessageBox.warning(self, "Error", "Debe completar todos los campos.")
            return

        conn = db.conectar()
        if self.id_faltante:
            conn.execute("""
                UPDATE faltantes_stock
                SET detalle = ?, proveedor_id = ?, id_estado = ?, fecha = ?, hora = ?
                WHERE id_faltante = ?
            """, (detalle, proveedor_id, estado_id, fecha, hora, self.id_faltante))
        else:
            conn.execute("""
                INSERT INTO faltantes_stock (detalle, proveedor_id, id_estado, fecha, hora)
                VALUES (?, ?, ?, ?, ?)
            """, (detalle, proveedor_id, estado_id, fecha, hora))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Éxito", "Guardado correctamente.")
        self.closed.emit()
        self.close()
