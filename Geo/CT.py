import mysql.connector

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="193.203.166.27",
    user="u387905082_deepiadev",
    password="Tiscaventisca.5",
    database="u387905082_QEP"
)

# Crear cursor
cursor = conexion.cursor()

# Definición de las tablas a crear
tablas = {
    "Data_INEGI": [
        ("id", "INT AUTO_INCREMENT PRIMARY KEY"),
        ("nombre_act", "VARCHAR(255)"),
        ("per_ocu", "VARCHAR(255)"),
        ("entidad", "VARCHAR(255)"),
        ("municipio", "VARCHAR(255)"),
        ("localidad", "VARCHAR(255)"),
        ("latitud", "DOUBLE"),
        ("longitud", "DOUBLE")
    ],
    "puntos_cercanos": [
        ("id", "INT AUTO_INCREMENT PRIMARY KEY"),
        ("id_inventario", "INT"),
        ("tag", "VARCHAR(255)"),
        ("distancia", "INT"),
        ("cantidad", "INT")
    ]
}

# Crear las tablas en la base de datos
for nombre_tabla, columnas_tabla in tablas.items():
    crear_tabla_query = "CREATE TABLE IF NOT EXISTS {} (".format(nombre_tabla)
    for columna, tipo in columnas_tabla:
        crear_tabla_query += "{} {}, ".format(columna, tipo)
    crear_tabla_query = crear_tabla_query[:-2] + ")"
    cursor.execute(crear_tabla_query)
    conexion.commit()

# Cerrar conexión
conexion.close()