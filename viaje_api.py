import openrouteservice
from openrouteservice import convert
import sys

API_KEY = "5b3ce3597851110001cf6248c5f4fd4642744412a24cba3a0db792d3"  # <-- reemplázala con tu clave re

# Diccionario de medios aceptados
medios_transporte = {
    "auto": "driving-car",
    "bicicleta": "cycling-regular",
    "a pie": "foot-walking"
}

# Crear cliente
client = openrouteservice.Client(key=API_KEY)

def geocodificar(ciudad):
    try:
        resultado = client.pelias_search(text=ciudad)
        coords = resultado['features'][0]['geometry']['coordinates']
        return coords
    except:
        print(f"No se pudo encontrar la ciudad: {ciudad}")
        return None

def calcular_ruta(origen, destino, medio):
    coords_origen = geocodificar(origen)
    coords_destino = geocodificar(destino)

    if not coords_origen or not coords_destino:
        return

    if medio not in medios_transporte:
        print("Medio de transporte inválido.")
        return

    profile = medios_transporte[medio]
    try:
        route = client.directions(
            coordinates=[coords_origen, coords_destino],
            profile=profile,
            format='geojson'
        )
        distancia_km = route['features'][0]['properties']['segments'][0]['distance'] / 1000
        duracion_horas = route['features'][0]['properties']['segments'][0]['duration'] / 3600
        distancia_millas = distancia_km * 0.621371

        print("\n--- Resumen del viaje ---")
        print(f"Desde: {origen}")
        print(f"Hasta: {destino}")
        print(f"Medio: {medio}")
        print(f"Distancia: {distancia_km:.2f} km / {distancia_millas:.2f} millas")
        print(f"Duración estimada: {duracion_horas:.2f} horas")
        print(f"Narrativa: Viajando desde {origen} a {destino} en {medio}, recorrerás aproximadamente {distancia_km:.2f} km en unas {duracion_horas:.2f} horas.\n")
    except:
        print("No se pudo calcular la ruta.")

# Bucle principal
while True:
    print("\n--- Calculador de viaje Chile - Argentina ---")
    origen = input("Ingrese la Ciudad de Origen (o 's' para salir): ").strip()
    if origen.lower() == 's':
        print("Saliendo...")
        sys.exit()

    destino = input("Ingrese la Ciudad de Destino (o 's' para salir): ").strip()
    if destino.lower() == 's':
        print("Saliendo...")
        sys.exit()

    print("Elija el medio de transporte (auto, bicicleta, a pie):")
    medio = input("Medio: ").strip().lower()

    calcular_ruta(origen, destino, medio)
