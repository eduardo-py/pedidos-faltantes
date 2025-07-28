from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QMessageBox
import db

class EstadosWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #ff4839;")
        self.setWindowTitle("Gestión de Estados")
        self.layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.input = QLineEdit()
        btns = QHBoxLayout()
        self.btn_add = QPushButton("Agregar / Actualizar")
        self.btn_del = QPushButton("Eliminar")
        btns.addWidget(self.btn_add); btns.addWidget(self.btn_del)
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.input)
        self.layout.addLayout(btns)
        self.setLayout(self.layout)

        self.estado_id = None
        self.btn_add.clicked.connect(self.add_update)
        self.btn_del.clicked.connect(self.delete)
        self.list_widget.itemClicked.connect(self.load_item)
        self.load_items()

    def load_items(self):
        self.list_widget.clear()
        conn = db.conectar()
        for r in conn.execute("SELECT id_estados, nombre FROM estados ORDER BY nombre"):
            self.list_widget.addItem(f"{r['id_estados']} - {r['nombre']}")
        conn.close()

    def load_item(self, item):
        id_, nombre = item.text().split(" - ", 1)
        self.estado_id = id_
        self.input.setText(nombre)

    def add_update(self):
        nombre = self.input.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "Nombre es obligatorio.")
            return
        conn = db.conectar()
        cur = conn.cursor()
        if self.estado_id:
            cur.execute("UPDATE estados SET nombre=? WHERE id_estados=?", (nombre, self.estado_id))
        else:
            cur.execute("INSERT INTO estados(nombre) VALUES(?)", (nombre,))
        conn.commit(); conn.close()
        self.estado_id = None; self.input.clear()
        self.load_items()

    def delete(self):
        if not self.estado_id:
            QMessageBox.warning(self, "Error", "Seleccionar un estado.")
            return
        conn = db.conectar()
        conn.execute("DELETE FROM estados WHERE id_estados=?", (self.estado_id,))
        conn.commit(); conn.close()
        self.estado_id = None; self.input.clear()
        self.load_items()
