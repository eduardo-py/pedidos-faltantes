
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #ff4839;")
        self.setWindowTitle("Sistema de Gestión")
        self.setGeometry(100, 100, 300, 400)

        layout = QVBoxLayout()

        btn_pedidos = QPushButton("Pedidos")
        btn_pedidos.clicked.connect(self.abrir_pedidos)
        layout.addWidget(btn_pedidos)

        btn_faltantes = QPushButton("Faltantes")
        btn_faltantes.clicked.connect(self.abrir_faltantes)
        layout.addWidget(btn_faltantes)

        btn_estados = QPushButton("Estados")
        btn_estados.clicked.connect(self.abrir_estados)
        layout.addWidget(btn_estados)

        btn_proveedores = QPushButton("Proveedores")
        btn_proveedores.clicked.connect(self.abrir_proveedores)
        layout.addWidget(btn_proveedores)

        btn_exportar = QPushButton("Exportar")
        btn_exportar.clicked.connect(self.abrir_exportar)
        layout.addWidget(btn_exportar)

        self.setLayout(layout)

    def abrir_pedidos(self):
        from windows.pedidos import PedidosWindow
        self.pedidos_window = PedidosWindow()
        self.pedidos_window.show()

    def abrir_faltantes(self):
        from windows.faltantes import FaltantesWindow
        self.faltantes_window = FaltantesWindow()
        self.faltantes_window.show()

    def abrir_estados(self):
        from windows.estados import EstadosWindow
        self.estados_window = EstadosWindow()
        self.estados_window.show()

    def abrir_proveedores(self):
        from windows.proveedores import ProveedoresWindow
        self.proveedores_window = ProveedoresWindow()
        self.proveedores_window.show()

    def abrir_exportar(self):
        from windows.exportar import ExportarWindow
        self.exportar_window = ExportarWindow()
        self.exportar_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
