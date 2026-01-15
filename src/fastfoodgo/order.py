class OrderError(Exception):
    """Erreur personnalisée pour les problèmes de commande."""
    pass

def calculate_order_total(items: list) -> float:
    """
    Calcule le total d'une liste d'articles.
    Chaque article est un dictionnaire {'name': str, 'price': float, 'quantity': int}.
    """
    if not items:
        return 0.0
    
    total = 0.0
    for item in items:
        if item['price'] < 0:
            raise OrderError("Le prix ne peut pas être négatif")
        total += item['price'] * item.get('quantity', 1)
        
    return total

def validate_status_transition(current_status: str, new_status: str) -> bool:
    """
    Valide si le changement de statut est autorisé.
    Cycle de vie : created -> paid -> preparing -> delivered
    """
    valid_transitions = {
        "created": ["paid", "cancelled"],
        "paid": ["preparing", "cancelled"],
        "preparing": ["ready", "cancelled"],
        "ready": ["delivered"],
        "delivered": [],
        "cancelled": []
    }
    
    if current_status not in valid_transitions:
        raise OrderError(f"Statut inconnu: {current_status}")
        
    if new_status in valid_transitions[current_status]:
        return True
        
    return False