from math import radians, sin, cos, sqrt, atan2
import mysql.connector
from tqdm import tqdm

def calcular_distancia(lat1, lon1, lat2, lon2):
    # Radio de la Tierra en kilómetros
    radio_tierra = 6371.0

    # Convertir las latitudes y longitudes a radianes
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Diferencia de latitudes y longitudes
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Aplicar la fórmula del haversine
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    a = min(a, 1)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distancia = radio_tierra * c

    return distancia

conexion = mysql.connector.connect(
    host="193.203.166.27",
    user="u387905082_deepiadev",
    password="Tiscaventisca.5",
    database="u387905082_QEP"
)

cursor = conexion.cursor()

consulta = "SELECT id, latitud, longitud FROM inventarios"
cursor.execute(consulta)
puntos_inventario = cursor.fetchall()

consulta = "SELECT nombre_act, latitud, longitud FROM Data_INEGI"
cursor.execute(consulta)
puntos_interes = cursor.fetchall()

distancias = [100, 200, 300, 1000, 2000, 3000, 5000, 10000, 15000]

resultados = []
id = 1

for punto_inventario in tqdm(puntos_inventario, desc="Procesando puntos de inventario"):
    id_inventario, lat_inventario, lon_inventario = punto_inventario

    for distancia in distancias:
        cantidad = 0

        for punto_interes in puntos_interes:
            nombre_interes, lat_interes, lon_interes = punto_interes

            distancia_calculada = calcular_distancia(lat_inventario, lon_inventario, lat_interes, lon_interes)
            distancia_metros = distancia_calculada * 1000

            if distancia_metros <= distancia:
                cantidad += 1

        resultados.append({
            'id': id,
            'id_inventario': id_inventario,
            'tag': nombre_interes,
            'distancia': distancia,
            'cantidad': cantidad
        })

        id += 1

for resultado in tqdm(resultados, desc="Insertando resultados en la base de datos"):
    consulta = "INSERT INTO puntos_cercanos (id, id_inventario, tag, distancia, cantidad) VALUES (%s, %s, %s, %s, %s)"
    valores = (resultado['id'], resultado['id_inventario'], resultado['tag'], resultado['distancia'], resultado['cantidad'])
    cursor.execute(consulta, valores)

conexion.commit()

cursor.close()
conexion.close()