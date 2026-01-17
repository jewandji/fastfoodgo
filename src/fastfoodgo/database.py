import os
import psycopg2
import time

def get_db_connection():
    """Tente de se connecter à la base de données."""
    
    # 1. PRIORITÉ CLOUD : Si on a une URL complète (donnée par Render ou toi)
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        try:
            conn = psycopg2.connect(db_url)
            print("Connexion CLOUD réussie via DATABASE_URL !")
            return conn
        except Exception as e:
            print(f"Erreur de connexion Cloud : {e}")

    # 2. SINON LOCAL (DOCKER) : On utilise la méthode classique
    print("Tentative de connexion locale (Docker)...")
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host="postgres",
                database=os.environ.get("POSTGRES_DB", "fastfood_db"),
                user=os.environ.get("POSTGRES_USER", "fastfood_user"),
                password=os.environ.get("POSTGRES_PASSWORD", "fastfood_password")
            )
            print("Connexion DOCKER réussie !")
            return conn
        except psycopg2.OperationalError as e:
            print(f"La base n'est pas encore prête... On attend 2s.")
            time.sleep(2)
            retries -= 1
    
    raise Exception("Impossible de se connecter à la BDD après plusieurs essais.")

def init_db(conn):
    # ... (Le reste de ton code init_db ne change pas, tu peux le garder tel quel)
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
    print("Tables créées/vérifiées !")

if __name__ == "__main__":
    conn = get_db_connection()
    init_db(conn)
    conn.close()