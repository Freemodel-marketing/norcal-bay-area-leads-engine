
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
