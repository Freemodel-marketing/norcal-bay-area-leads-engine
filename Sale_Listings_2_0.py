import requests
import time
import os
from supabase import create_client, Client
from utils import *

# 1. Configuración de Supabase (Usa variables de entorno para seguridad)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
RENTCAST_API_KEY = os.environ.get("RENTCAST_API_KEY")

# ESTA LÍNEA ES PARA DIAGNÓSTICO
if SUPABASE_KEY:
    print(f"✅ La llave fue recibida y es {SUPABASE_KEY} caracteres.")
else:
    print("❌ La llave llegó VACÍA desde GitHub.")

# ... resto del código ...

# Validación simple para asegurarnos de que las llaves existen
"""if not all([SUPABASE_URL, SUPABASE_KEY, RENTCAST_API_KEY]):
    raise ValueError("❌ Faltan llaves de API en las variables de entorno.")


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuración de búsqueda
cities = ["San%20Mateo"]
status = "Active"
daysOld = "30:90" # Days on market
offset = 0

def process_listings():
    for city in cities:
        url = (
            f"https://api.rentcast.io/v1/listings/sale?city={city}&state=CA"
            f"&propertyType=Single%20Family|Condo|Townhouse|Multi-Family"
            f"&status={status}&daysOld={daysOld}&limit=500&offset={offset}"
            f"&includeTotalCount=true"
        )
        
        headers = {
            "accept": "application/json",
            "X-Api-Key": RENTCAST_API_KEY
        }

        print(f"📡 Consultando RentCast para {city}...")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            total_in_db = response.headers.get('X-Total-Count', 'N/A')
            
            print(f"📊 Registros recibidos: {len(data)}")
            print(f"📊 Total disponible en RentCast (X-Total-Count): {total_in_db}")

            # --- LLAMADA A FUNCIÓN SEGREGADA (JSON LOCAL) ---
            # Puedes comentar esta línea cuando ya no necesites el archivo local
            # save_local_backups(data, status, city)

            # Limpiar y aplanar los datos para Supabase
            clean_data = map_data_for_supabase(data)

            # --- IMPORTACIÓN A SUPABASE ---
            if clean_data:
                print(f"🚀 Subiendo datos de {city} a Supabase...")
                # Usamos upsert para actualizar si el registro ya existe por ID
                try:
                    # Ajustamos los datos para que coincidan con tus columnas de Supabase
                    # Nota: Asegúrate que los nombres de campos en Supabase coincidan con el JSON
                    supabase.table("leads_ventas").upsert(clean_data).execute()
                    print(f"✅ ¡Datos sincronizados con éxito en la nube!")
                except Exception as e:
                    print(f"❌ Error al subir a Supabase: {e}")
        else:
            print(f"❌ Error API: {response.status_code} - {response.text}") 

        time.sleep(5) """

if __name__ == "__main__":
    pass
    #process_listings()
