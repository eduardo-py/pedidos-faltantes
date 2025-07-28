import sqlite3

DB = "mi_base.db"

def conectar():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = conectar()
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS estados (
        id_estados INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    );
    CREATE TABLE IF NOT EXISTS proveedores (
        id_proveedores INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    );
    CREATE TABLE IF NOT EXISTS pedidos_clientes (
        id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        detalle TEXT NOT NULL,
        numero_cliente TEXT,
        nombre_cliente TEXT,
        id_estado INTEGER,
        fecha TEXT,
        hora TEXT,
        FOREIGN KEY (id_estado) REFERENCES estados(id_estados)
    );
    CREATE TABLE IF NOT EXISTS faltantes_stock (
        id_faltante INTEGER PRIMARY KEY AUTOINCREMENT,
        detalle TEXT NOT NULL,
        proveedor_id INTEGER,
        id_estado INTEGER,
        FOREIGN KEY (proveedor_id) REFERENCES proveedores(id_proveedores),
        FOREIGN KEY (id_estado) REFERENCES estados(id_estados)
    );
    """)
    conn.commit()
    conn.close()
