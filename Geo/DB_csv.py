import os
import pandas as pd
import mysql.connector
from tqdm import tqdm

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="193.203.166.27",
    user="u387905082_deepiadev",
    password="Tiscaventisca.5",
    database="u387905082_QEP"
)

# Nombre de la tabla en la base de datos
nombre_tabla = "Data_INEGI"

# Definir las columnas de la tabla
columnas_tabla = [
    ("id", "INT AUTO_INCREMENT PRIMARY KEY"),
    ("nombre_act", "VARCHAR(255)"),
    ("per_ocu", "VARCHAR(255)"),
    ("entidad", "VARCHAR(255)"),
    ("municipio", "VARCHAR(255)"),
    ("localidad", "VARCHAR(255)"),
    ("latitud", "DOUBLE"),
    ("longitud", "DOUBLE")
]

# Crear cursor
cursor = conexion.cursor()

# Crear la tabla en la base de datos si no existe
def crear_tabla():
    crear_tabla_query = "CREATE TABLE IF NOT EXISTS {} (".format(nombre_tabla)
    for columna, tipo in columnas_tabla:
        crear_tabla_query += "{} {}, ".format(columna, tipo)
    crear_tabla_query = crear_tabla_query[:-2] + ")"
    cursor.execute(crear_tabla_query)
    conexion.commit()

# Insertar los datos del DataFrame en la tabla
def insertar_datos(df):
    for _, fila in tqdm(df.iterrows(), total=len(df), desc="Insertando datos"):
        valores = [fila[columna] for columna, _ in columnas_tabla[1:]]  # Excluir la primera columna (ID)
        insert_query = "INSERT INTO {} ({}) VALUES ({})".format(nombre_tabla, ", ".join([col[0] for col in columnas_tabla[1:]]), ", ".join(["%s" for _ in range(len(columnas_tabla) - 1)]))
        cursor.execute(insert_query, tuple(valores))
    conexion.commit()

# Especificar el archivo CSV a leer
archivo_csv = "Oficinas_Limpia.csv"  # Reemplaza con el nombre de tu archivo

# Leer el archivo CSV y agregarlo a la tabla
ruta_csv = os.path.join("C:/Users/HP/Desktop/Data_Limpia", archivo_csv)  # Reemplaza con la ruta de tu directorio
df = pd.read_csv(ruta_csv, encoding='latin1')

# Eliminar filas con valores NaN del DataFrame
df.dropna(inplace=True)

# Llamamos a la función para insertar los datos
insertar_datos(df)

# Llamamos a la función para crear la tabla (si es necesario)
crear_tabla()

# Cerrar conexión
conexion.close()