import pandas as pd
from fastfoodgo.database import get_db_connection

def print_kpis():
    conn = get_db_connection()
    
    print("--- RAPPORT KPI FASTFOODGO ---")
    
    # 1. Chiffre d'affaires total
    # On utilise pandas pour lire le SQL directement en DataFrame (très utilisé en Data Science)
    df_orders = pd.read_sql("SELECT * FROM orders", conn)
    
    total_revenue = df_orders['total_price'].sum()
    print(f"Chiffre d'affaires total : {total_revenue} €")
    
    # 2. Répartition par statut
    print("\nCommandes par statut :")
    status_counts = df_orders['status'].value_counts()
    print(status_counts)
    
    # 3. Top des articles vendus (Jointure SQL)
    query_items = """
        SELECT item_name, SUM(quantity) as total_sold
        FROM order_items
        GROUP BY item_name
        ORDER BY total_sold DESC
        LIMIT 3
    """
    df_items = pd.read_sql(query_items, conn)
    
    print("\nTop 3 Articles :")
    print(df_items)
    
    conn.close()

if __name__ == "__main__":
    print_kpis()