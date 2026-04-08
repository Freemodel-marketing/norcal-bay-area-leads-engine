
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
