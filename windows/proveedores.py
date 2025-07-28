
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox
import sqlite3

class ProveedoresWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Gestión de Proveedores")
		self.setGeometry(100, 100, 400, 300)
		self.setup_ui()
		self.cargar_proveedores()

	def setup_ui(self):
		layout = QVBoxLayout()

		self.input_nombre = QLineEdit()
		layout.addWidget(QLabel("Nombre del proveedor:"))
		layout.addWidget(self.input_nombre)

		btn_layout = QHBoxLayout()
		self.btn_agregar = QPushButton("Agregar")
		self.btn_agregar.clicked.connect(self.agregar_proveedor)
		btn_layout.addWidget(self.btn_agregar)

		self.btn_modificar = QPushButton("Modificar")
		self.btn_modificar.clicked.connect(self.modificar_proveedor)
		btn_layout.addWidget(self.btn_modificar)

		layout.addLayout(btn_layout)

		self.lista = QListWidget()
		self.lista.itemClicked.connect(self.cargar_datos_proveedor)
		layout.addWidget(self.lista)

		self.setLayout(layout)

	def cargar_proveedores(self):
		self.lista.clear()
		conn = sqlite3.connect("mi_base.db")
		cursor = conn.cursor()
		cursor.execute("SELECT id_proveedores, nombre FROM proveedores")
		for row in cursor.fetchall():
			self.lista.addItem(f"{row[0]} - {row[1]}")
		conn.close()

	def agregar_proveedor(self):
		nombre = self.input_nombre.text().strip()
		if nombre:
			conn = sqlite3.connect("mi_base.db")
			cursor = conn.cursor()
			cursor.execute("INSERT INTO proveedores (nombre) VALUES (?)", (nombre,))
			conn.commit()
			conn.close()
			self.input_nombre.clear()
			self.cargar_proveedores()
		else:
			QMessageBox.warning(self, "Advertencia", "El nombre no puede estar vacío.")

	def cargar_datos_proveedor(self, item):
		id_proveedor, nombre = item.text().split(" - ", 1)
		self.input_nombre.setText(nombre)
		self.proveedor_id_actual = int(id_proveedor)

	def modificar_proveedor(self):
		if hasattr(self, 'proveedor_id_actual'):
			nombre = self.input_nombre.text().strip()
			if nombre:
				conn = sqlite3.connect("mi_base.db")
				cursor = conn.cursor()
				cursor.execute("UPDATE proveedores SET nombre = ? WHERE id_proveedores = ?", (nombre, self.proveedor_id_actual))
				conn.commit()
				conn.close()
				self.input_nombre.clear()
				self.cargar_proveedores()
			else:
				QMessageBox.warning(self, "Advertencia", "El nombre no puede estar vacío.")
		else:
			QMessageBox.warning(self, "Advertencia", "Seleccioná un proveedor para modificar.")
