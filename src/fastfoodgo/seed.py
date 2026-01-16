import time
import random
from fastfoodgo.database import get_db_connection

# Notre "Menu" simulé
MENU_ITEMS = [
    ("Burger Classique", 8.50),
    ("Cheese Royal", 9.50),
    ("Frites", 3.50),
    ("Soda", 2.50),
    ("Glace Vanille", 4.00),
    ("Salade César", 7.00)
]

STATUS_CHOICES = ["created", "paid", "preparing", "ready", "delivered"]

def create_random_order(conn):
    cur = conn.cursor()
    
    # 1. On choisit entre 1 et 5 articles au hasard
    items_count = random.randint(1, 5)
    selected_items = random.choices(MENU_ITEMS, k=items_count)
    
    total_price = sum(price for _, price in selected_items)
    status = random.choice(STATUS_CHOICES)
    
    # 2. On insère la commande principale (Order)
    cur.execute(
        "INSERT INTO orders (status, total_price) VALUES (%s, %s) RETURNING id",
        (status, total_price)
    )
    order_id = cur.fetchone()[0]
    
    # 3. On insère les détails (Order Items)
    for name, price in selected_items:
        cur.execute(
            "INSERT INTO order_items (order_id, item_name, item_price, quantity) VALUES (%s, %s, %s, %s)",
            (order_id, name, price, 1)
        )
    
    conn.commit()
    cur.close()
    print(f"Commande #{order_id} générée ({status}) - {total_price}€")

if __name__ == "__main__":
    conn = get_db_connection()
    print("Démarrage du générateur de données...")
    try:
        # On génère 10 commandes avec une petite pause entre chaque
        for _ in range(10):
            create_random_order(conn)
            time.sleep(0.5) 
    except KeyboardInterrupt:
        print("Arrêt.")
    finally:
        conn.close()