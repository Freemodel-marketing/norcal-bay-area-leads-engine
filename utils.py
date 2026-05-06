
def split_agent_name(full_name):
    if not full_name:
        return "Unknown", "Unknown"
    
    parts = full_name.split()
    num_parts = len(parts)

    # Caso: Una sola palabra (ej: "Sunnie")
    if num_parts == 1:
        return parts[0], ""
    
    # Caso: 2 palabras (ej: "David Tapper")
    elif num_parts == 2:
        return parts[0], parts[1]
    
    # Caso: 3 o 4 palabras (ej: "Mary J Wong" o "Devi Pua Inia Khanna")
    # Regla: Las dos primeras al First Name, el resto al Last Name
    elif 3 <= num_parts <= 4:
        first_name = " ".join(parts[:2])
        last_name = " ".join(parts[2:])
        return first_name, last_name
    
    # Caso: Más de 4 palabras (ej: "Susan & Sabrina - The Caton Team")
    # Regla: Todo al First Name
    else:
        return full_name, ""

def filter_by_county(raw_data_list, target_county):
    """
    Filtra la lista cruda de la API para mantener solo los que coinciden con el target.
    """
    filtered_leads = []
    # Limpiamos el target: "San%20Mateo" -> "san mateo"
    target_clean = target_county.replace("%20", " ").lower().strip()
    
    for item in raw_data_list:
        # Buscamos el condado dentro del objeto address de la API
        lead_county = item.get('address', {}).get('county', '')
        
        if lead_county:
            # Limpiamos el valor de la API: "San Mateo County" -> "san mateo"
            lead_county_clean = lead_county.lower().replace("county", "").strip()
            
            # Verificamos si hay coincidencia
            if target_clean in lead_county_clean or lead_county_clean in target_clean:
                filtered_leads.append(item)
                
    return filtered_leads

def process_rentcast_results(json_data):
    """
    Procesa el JSON de RentCast y devuelve una lista de diccionarios
    listos para Supabase.
    """
    clean_leads = []
    
    for item in json_data:
        # RentCast agrupa la dirección en un objeto 'address'
        address_obj = item.get('address', {})
        
        # Intentamos obtener el nombre del agente si está disponible
        raw_agent_name = item.get('agentName', '')
        agent_first, agent_last = split_agent_name(raw_agent_name)

        lead = {
            "id": item.get('id'), 
            "address": address_obj.get('formattedAddress'),
            "street": address_obj.get('addressLine1'), # RentCast usa addressLine1 para la calle
            "city": address_obj.get('city'),
            "county": address_obj.get('county'),
            "price": item.get('price'), # En RentCast es 'price', no 'mlsListingPrice'
            "days_on_market": item.get('daysOnMarket'),
            "property_type": item.get('propertyType'),
            "property_use": item.get('propertyUse'), # Aprovechamos que RentCast lo da
            "agent_first_name": agent_first if agent_first != "Not Found" else "PENDING",
            "agent_last_name": agent_last if agent_last != "Not Found" else "PENDING",
            "agent_email": item.get('agentEmail') if item.get('agentEmail') else "PENDING",
            "agent_phone": item.get('agentPhone') if item.get('agentPhone') else "PENDING",
            "agent_office": item.get('listingOffice') if item.get('listingOffice') else "PENDING"
        }
        
        clean_leads.append(lead)
        
    return clean_leads
