import json
import csv

def save_local_backups(data, status, city):
    """
    Genera un archivo JSON de respaldo y un archivo CSV procesado
    con la información de agentes y oficinas.
    """
    if not data:
        print(f"⚠️ No hay datos para generar archivos locales en {city}.")
        return

    # --- 1. GENERAR ARCHIVO JSON ---
    json_file = f"{status}_SalesListings_{city}_properties.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"💾 Respaldo JSON guardado: {json_file}")

    # --- 2. GENERAR ARCHIVO CSV ---
    csv_file = f"{status}_Leads_{city}.csv"
    headers = [
        'formattedAddress', 'County', 'propertyType', 'listedDate', 'daysOnMarket', 
        'Agent Name', 'Agent Phone', 'Agent Email', 'Agent Website',
        'Office Name', 'Office Phone', 'Office Email', 'Office Website'
    ]

    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for p in data:
                # Extraemos diccionarios anidados de forma segura
                agent = p.get('listingAgent', {})
                office = p.get('listingOffice', {})

                row = {
                    'formattedAddress': p.get('formattedAddress'),
                    'County': p.get('county'),
                    'propertyType': p.get('propertyType'),
                    'listedDate': p.get('listedDate'),
                    'daysOnMarket': p.get('daysOnMarket'),
                    
                    # Datos del Agente
                    'Agent Name': agent.get('name', 'N/A'),
                    'Agent Phone': agent.get('phone', 'N/A'),
                    'Agent Email': agent.get('email', 'N/A'),
                    'Agent Website': agent.get('website', 'N/A'),
                    
                    # Datos de la Oficina
                    'Office Name': office.get('name', 'N/A'),
                    'Office Phone': office.get('phone', 'N/A'),
                    'Office Email': office.get('email', 'N/A'),
                    'Office Website': office.get('website', 'N/A')
                }
                writer.writerow(row)
        
        print(f"✅ Archivo CSV generado con éxito: {csv_file} ({len(data)} registros)")
    
    except Exception as e:
        print(f"❌ Error al generar el CSV: {e}")

def map_data_for_supabase(raw_data):
    """
    Transforma el JSON anidado de RentCast en un diccionario plano
    para las columnas de Supabase.
    """
    mapped_list = []
    
    for p in raw_data:
        agent = p.get('listingAgent', {})
        office = p.get('listingOffice', {})
        
        flat_record = {
            "id": p.get('id'),
            "address": p.get('formattedAddress'),
            "property_type": p.get('propertyType'),
            "price": p.get('price'),
            "county": p.get('county'),
            "listed_date": p.get('listedDate'),
            "days_on_market": p.get('daysOnMarket'),
            
            # Datos del Agente aplanados
            "agent_name": agent.get('name'),
            "agent_phone": agent.get('phone'),
            "agent_email": agent.get('email'),
            "agent_website": agent.get('website'),
            
            # Datos de la Oficina aplanados
            "office_name": office.get('name'),
            "office_phone": office.get('phone'),
            "office_email": office.get('email'),
            "office_website": office.get('website')
        }
        mapped_list.append(flat_record)
        
    return mapped_list