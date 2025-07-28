
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QTextEdit, QComboBox, QMessageBox, QDateEdit, QTimeEdit
)
from PyQt5.QtCore import QDate, QTime, pyqtSignal
import db

class PedidoForm(QWidget):
    closed = pyqtSignal()

    def __init__(self, id_pedido=None):
        super().__init__()
        self.setStyleSheet("background-color: #ff4839;")
        self.id_pedido = id_pedido
        self.setWindowTitle("Editar Pedido" if id_pedido else "Nuevo Pedido de Cliente")
        self.layout = QVBoxLayout()

        self.detalle = QTextEdit()
        self.numero_cliente = QLineEdit()
        self.nombre_cliente = QLineEdit()
        self.estado = QComboBox()
        self.fecha = QDateEdit(calendarPopup=True)
        self.hora = QTimeEdit()

        self.fecha.setDate(QDate.currentDate())
        self.hora.setTime(QTime.currentTime())

        self.layout.addWidget(QLabel("Detalle del Pedido:"))
        self.layout.addWidget(self.detalle)
        self.layout.addWidget(QLabel("Número de Cliente:"))
        self.layout.addWidget(self.numero_cliente)
        self.layout.addWidget(QLabel("Nombre del Cliente:"))
        self.layout.addWidget(self.nombre_cliente)
        self.layout.addWidget(QLabel("Estado del Pedido:"))
        self.layout.addWidget(self.estado)
        self.layout.addWidget(QLabel("Fecha:"))
        self.layout.addWidget(self.fecha)
        self.layout.addWidget(QLabel("Hora:"))
        self.layout.addWidget(self.hora)

        self.btn_guardar = QPushButton("Guardar Pedido")
        self.layout.addWidget(self.btn_guardar)

        self.setLayout(self.layout)
        self.btn_guardar.clicked.connect(self.guardar_pedido)

        self.cargar_estados()
        if self.id_pedido:
            self.cargar_datos()

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
        query = "SELECT * FROM pedidos_clientes WHERE id_pedido = ?"
        pedido = conn.execute(query, (self.id_pedido,)).fetchone()
        conn.close()

        self.detalle.setPlainText(pedido["detalle"])
        self.numero_cliente.setText(pedido["numero_cliente"])
        self.nombre_cliente.setText(pedido["nombre_cliente"])
        self.fecha.setDate(QDate.fromString(pedido["fecha"], "yyyy-MM-dd"))
        self.hora.setTime(QTime.fromString(pedido["hora"], "HH:mm:ss"))

        index_estado = self.estado.findData(pedido["id_estado"])
        self.estado.setCurrentIndex(index_estado if index_estado != -1 else 0)

    def guardar_pedido(self):
        detalle = self.detalle.toPlainText().strip()
        num_cliente = self.numero_cliente.text().strip()
        nombre_cliente = self.nombre_cliente.text().strip()
        estado_id = self.estado.currentData()
        fecha = self.fecha.date().toString("yyyy-MM-dd")
        hora = self.hora.time().toString("HH:mm:ss")

        if not detalle or estado_id == -1:
            QMessageBox.warning(self, "Error", "Debe completar los campos obligatorios.")
            return

        conn = db.conectar()
        if self.id_pedido:
            conn.execute("""
                UPDATE pedidos_clientes
                SET detalle = ?, numero_cliente = ?, nombre_cliente = ?, id_estado = ?, fecha = ?, hora = ?
                WHERE id_pedido = ?
            """, (detalle, num_cliente, nombre_cliente, estado_id, fecha, hora, self.id_pedido))
        else:
            conn.execute("""
                INSERT INTO pedidos_clientes (detalle, numero_cliente, nombre_cliente, id_estado, fecha, hora)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (detalle, num_cliente, nombre_cliente, estado_id, fecha, hora))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Éxito", "Pedido guardado correctamente.")
        self.closed.emit()
        self.close()
