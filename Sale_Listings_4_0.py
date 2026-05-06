import requests
import os
import time
from supabase import create_client, Client
from utils import *

# 1. Configuración de Supabase (Usa variables de entorno para seguridad)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
RENTCAST_API_KEY = os.envoron.get("RENTCAST_API_KEY_GILBERTO")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuración de búsqueda
"""cities = ["Oakland", "San%20Francisco", "Berkeley", "San%20Rafael", "San%20Jose", "Alameda",
          "Mill%20Valley", "Richmond", "Sunnyvale", "San%20Mateo", "El%20Cerrito", "Novato",
          "Corte%Madera", "Redwood%20City", "San%20Carlos", "Palo%20Alto", "Piedmont", "San%20Bruno"]
"""

cities = ["Oakland"]

status = "Active"
daysOld = "1:365" # Days on market
offset = 0
price = "50000:5000000"
lotSize = "*:20000"
propertyType = "Single Family|Condo|Townhouse"

def process_listings():
    for city in cities:

        url = f"https://api.rentcast.io/v1/listings/sale?city={city}&state=CA&propertyType={propertyType}&lotSize={lotSize}&status=Active&daysOld={daysOld}&price={price}&limit=500"
        
        headers = {
            "accept": "application/json",
            "X-Api-Key": RENTCAST_API_KEY    # RENTCAST_API_KEY
        }

        print(f"📡 Consultando RentCast para {city}...")
        response = requests.get(url, headers=headers)
        print(f"Numero de resultados encontrados: {len(response.json())}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Leads crudos: {len(data)}")
            # Procesamos
            leads_to_upload = process_rentcast_results(data)
            
            # Subimos a Supabase por lotes
            if leads_to_upload:
                supabase.table("leads_ventas").upsert(leads_to_upload).execute()
                print(f"🚀 {len(leads_to_upload)} leads sincronizados en Supabase.")

        time.sleep(5)

if __name__ == "__main__":
    process_listings()
