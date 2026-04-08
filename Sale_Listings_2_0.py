import os
import requests
import time
from supabase import create_client, Client
from utils import *

# Configuración
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
RE_API_KEY = os.environ.get("RE_API_KEY") 

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

SEARCH_URL = "https://api.realestateapi.com/v2/PropertySearch"
DETAIL_URL = "https://api.realestateapi.com/v2/PropertyDetail"

counties = [
    "San%20Francisco", "San%20Mateo", "Santa%20Clara", "Santa%20Cruz",
    "Monterey", "Alameda", "Contra%20Costa", "Napa", "Sonoma", "Marin"
]

def fetch_and_store_ids():
    
    print("ESTOY VIVO")
    
    headers = {
        "accept": "application/json",
        "x-user-id": "UniqueUserIdentifier",
        "content-type": "application/json",
        "x-api-key": RE_API_KEY
    }

    all_final_leads = [] # Lista maestra para acumular TODO antes de subir

    for county in counties:
        payload = {
            "size": 250,
            "county": county,
            "state": "CA",
            "mls_days_on_market_min": 90,
            "mls_active": True
        }

        print(f"📡 Buscando leads en {county}...")
        response = requests.post(SEARCH_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            raw_data = response.json().get('data', [])
            print(f"Numero de resultados encontrados: {len(response.json())}")
            
            for prop in raw_data:
                # 1. Armamos la info básica de la propiedad
                address_info = prop.get('address', {})
                prop_id = prop.get('id')
                
                lead = {
                    "id": prop_id, # Guardado como número real
                    "address": address_info.get('address'),
                    "street": address_info.get('street'),
                    "city": address_info.get('city'),
                    "county": address_info.get('county'),
                    "price": prop.get('mlsListingPrice'),
                    "days_on_market": prop.get('mlsDaysOnMarket'),
                    "property_type": prop.get('propertyType'),
                    "agent_first_name": "Not Found",
                    "agent_last_name": "Not Found",
                    "agent_email": "Not Found",
                    "agent_phone": "Not Found",
                    "agent_office": "Not Found"
                }

                # 2. Consultamos el DETALLE para obtener al agente inmediatamente
                print(f"🔍 Enriqueciendo propiedad ID: {prop_id}...")
                detail_payload = {"comps": False, "id": prop_id}
                
                try:
                    detail_res = requests.post(DETAIL_URL, json=detail_payload, headers=headers)
                    if detail_res.status_code == 200:
                        detail_data = detail_res.json().get("data", {})
                        mls_history = detail_data.get("mlsHistory", [])
                        
                        if mls_history:
                            latest = mls_history[0] # El registro más reciente

                            raw_agent_name = latest.get("agentName", "")
                            # Aplicamos nuestra lógica de división
                            agent_first, agent_last = split_agent_name(raw_agent_name)
                            
                            lead["agent_first_name"] = agent_first
                            lead["agent_last_name"] = agent_last
                            lead["agent_email"] = latest.get("agentEmail")
                            lead["agent_phone"] = latest.get("agentPhone")
                            lead["agent_office"] = latest.get("agentOffice")
                    
                    # Pausa pequeña para no saturar la API en el bucle interno
                    time.sleep(1) 
                except Exception as e:
                    print(f"⚠️ Error enriqueciendo ID {prop_id}: {e}")

                all_final_leads.append(lead)
            
        else:
            print(f"❌ Error en {county}: {response.status_code}")
        
        time.sleep(10) # Pausa entre condados

    # 3. SUBIDA FINAL A SUPABASE
    if all_final_leads:
        print(f"🚀 Subiendo {len(all_final_leads)} leads COMPLETOS a Supabase...")
        # Upsert por si el script corre dos veces, no duplicar IDs
        supabase.table("leads_ventas").upsert(all_final_leads).execute()
        print("✅ ¡Proceso terminado con éxito!")

if __name__ == "__main__":
    fetch_and_store_ids()
