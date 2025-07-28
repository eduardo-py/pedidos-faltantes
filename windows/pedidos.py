
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from windows.pedido_form import PedidoForm
import db

class PedidosWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #ff4839;")
        self.setWindowTitle("Pedidos de Clientes")
        self.resize(1000, 450)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        btn_layout = QHBoxLayout()
        self.btn_nuevo = QPushButton("Nuevo Pedido")
        self.btn_editar = QPushButton("Editar Seleccionado")
        self.btn_eliminar = QPushButton("Eliminar Seleccionado")

        self.btn_nuevo.clicked.connect(self.abrir_formulario_nuevo)
        self.btn_editar.clicked.connect(self.editar_pedido)
        self.btn_eliminar.clicked.connect(self.eliminar_pedido)

        btn_layout.addWidget(self.btn_nuevo)
        btn_layout.addWidget(self.btn_editar)
        btn_layout.addWidget(self.btn_eliminar)

        self.layout.addLayout(btn_layout)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels(["ID", "Detalle", "Cliente", "Teléfono", "Estado", "Fecha", "Hora"])
        self.layout.addWidget(self.tabla)

        self.cargar_pedidos()

    def cargar_pedidos(self):
        self.tabla.setRowCount(0)
        conn = db.conectar()
        query = """
            SELECT p.id_pedido, p.detalle, p.nombre_cliente, p.numero_cliente, e.nombre AS estado, p.fecha, p.hora
            FROM pedidos_clientes p
            LEFT JOIN estados e ON p.id_estado = e.id_estados
            ORDER BY p.fecha DESC, p.hora DESC
        """
        pedidos = conn.execute(query).fetchall()
        conn.close()

        self.tabla.setRowCount(len(pedidos))
        for row_idx, pedido in enumerate(pedidos):
            self.tabla.setItem(row_idx, 0, QTableWidgetItem(str(pedido["id_pedido"])))
            self.tabla.setItem(row_idx, 1, QTableWidgetItem(pedido["detalle"]))
            self.tabla.setItem(row_idx, 2, QTableWidgetItem(pedido["nombre_cliente"]))
            self.tabla.setItem(row_idx, 3, QTableWidgetItem(pedido["numero_cliente"]))
            self.tabla.setItem(row_idx, 4, QTableWidgetItem(pedido["estado"] or ""))
            self.tabla.setItem(row_idx, 5, QTableWidgetItem(pedido["fecha"]))
            self.tabla.setItem(row_idx, 6, QTableWidgetItem(pedido["hora"]))

        self.tabla.resizeColumnsToContents()

    def abrir_formulario_nuevo(self):
        self.formulario = PedidoForm()
        self.formulario.show()
        self.formulario.closed.connect(self.cargar_pedidos)

    def editar_pedido(self):
        fila = self.tabla.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Atención", "Seleccione un pedido para editar.")
            return
        id_pedido = int(self.tabla.item(fila, 0).text())
        self.formulario = PedidoForm(id_pedido=id_pedido)
        self.formulario.show()
        self.formulario.closed.connect(self.cargar_pedidos)

    def eliminar_pedido(self):
        fila = self.tabla.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Atención", "Seleccione un pedido para eliminar.")
            return
        id_pedido = int(self.tabla.item(fila, 0).text())
        confirmar = QMessageBox.question(self, "Eliminar", "¿Estás seguro de eliminar este pedido?",
                                         QMessageBox.Yes | QMessageBox.No)
        if confirmar == QMessageBox.Yes:
            conn = db.conectar()
            conn.execute("DELETE FROM pedidos_clientes WHERE id_pedido = ?", (id_pedido,))
            conn.commit()
            conn.close()
            self.cargar_pedidos()
