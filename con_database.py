import sqlite3
from sqlite3 import Error
from tkinter import messagebox
import os

camino = os.path.dirname(__file__) 
connection = sqlite3.connect(camino + "/StockDatabase.db")


class Database:
    
    def dml_database(self, query_sql, dados):
        try:
            with connection:
                con = connection.cursor()
                con.execute(query_sql, dados)
        except Error as e:
            messagebox.showerror(f"{e}", message="No fue posible realizar el registro!")
        else:
            messagebox.showinfo("Successfully", message="Registro realizado con exito!")
    
    def dql_database(self, query_sql, column_names=False):
        try:
            with connection:
                con = connection.cursor()
                con.execute(query_sql)
                response = con.fetchall()
                
                if column_names:
                    lista_columns = []
                    for i in set(response):
                        lista_columns.append(i[0])
                    return lista_columns
        
        except Error as e:
            messagebox.showerror(f"{e}", message="No fue posible encontrar el registro!")
        else:
            return response
        
    def dml_delete(self, id_target_delete):
        try:
            with connection:
                con = connection.cursor()
                con.execute(f"DELETE FROM stock WHERE id='{id_target_delete}'")
        except Error as e:
            messagebox.showerror(f"{e}", message="No fue posible realizar el registro!")
        else:
            messagebox.showinfo("Successfully", message="Registro eliminado con exito!")


def create_table():
    table = """
    CREATE TABLE IF NOT EXISTS stock (
        id              INTEGER     PRIMARY KEY AUTOINCREMENT,
        producto         TEXT (30),
        grupo           TEXT (15),
        medida          TEXT,
        lote            TEXT,
        stock         INTEGER     DEFAULT (0),
        valor_stock   REAL        AS (stock * valor_venta),
        stock_mín     INTEGER     DEFAULT (0),
        status          TEXT        AS (CASE WHEN stock < (stock_mín * 50/100) THEN 'CRÍTICO' WHEN stock <= stock_mín THEN 'VACIO' ELSE 'OK' END),
        proveedor      TEXT (20),
        responsable     TEXT (15),
        entradas        INTEGER     DEFAULT (0),
        fecha_entrada    TEXT,
        costo_unitario      REAL        DEFAULT (0),
        costo_total     REAL        AS (entradas * costo_unitario),
        salidas          INTEGER     DEFAULT (0),
        fecha_salida      TEXT,
        valor_venta     REAL        DEFAULT (0),
        facturación     REAL        AS (valor_venta * salidas),
        reponer           INTEGER     AS (CASE WHEN stock <= stock_mín THEN stock_mín - stock + (stock_mín * 100/100) ELSE 0 END),
        costo_reponer     REAL        AS (costo_unitario * reponer),
        barcode         TEXT (20),
        activo           TEXT,
        id_sucursal     INTEGER,
        id_permiso      INTEGER,
        FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal)
    );
    """
    table_sucursales="""
    CREATE TABLE IF NOT EXISTS sucursales (
        id_sucursal INTEGER PRIMARY KEY,
        nombre_sucursal VARCHAR(50) NOT NULL,
        direccion_sucursal VARCHAR(100) NOT NULL,
        telefono_sucursal VARCHAR(20) NOT NULL  
    );
    """

    table_usuarios="""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario VARCHAR(50) NOT NULL,
        user VARCHAR(50) NOT NULL,
        password_usuario VARCHAR(255) NOT NULL,
        nivel_permiso VARCHAR(20) NOT NULL,
        id_sucursal INT NOT NULL,
        FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal)
    );
    """

    try:
        with connection:
            con = connection.cursor()
            con.execute(table)
            con.execute(table_sucursales)
            con.execute(table_usuarios)

            
    except Error as e:
        print(e)

