import os
import psycopg2
import time

def get_db_connection():
    """Tente de se connecter à la base de données avec des retries."""
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host="postgres",
                database=os.environ.get("POSTGRES_DB", "fastfood_db"),
                user=os.environ.get("POSTGRES_USER", "fastfood_user"),
                password=os.environ.get("POSTGRES_PASSWORD", "fastfood_password")
            )
            print("Connexion à la base de données réussie !")
            return conn
        except psycopg2.OperationalError as e:
            print(f"La base n'est pas encore prête ({e})... On attend 2s.")
            time.sleep(2)
            retries -= 1
    
    raise Exception("Impossible de se connecter à la BDD après plusieurs essais.")

def init_db(conn):
    """Crée les tables nécessaires si elles n'existent pas (Data Modeling)."""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            status VARCHAR(50) NOT NULL,
            total_price FLOAT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS order_items (
            id SERIAL PRIMARY KEY,
            order_id INTEGER REFERENCES orders(id),
            item_name VARCHAR(100) NOT NULL,
            item_price FLOAT NOT NULL,
            quantity INTEGER NOT NULL
        )
        """
    )
    cur = conn.cursor()
    for command in commands:
        cur.execute(command)
    cur.close()
    conn.commit()
    print("Tables 'orders' et 'order_items' créées/vérifiées !")

if __name__ == "__main__":
    conn = get_db_connection()
    init_db(conn)
    conn.close()