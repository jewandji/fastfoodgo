import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import pickle
from fastfoodgo.database import get_db_connection

def train_model():
    print("Démarrage de l'entraînement IA...")
    conn = get_db_connection()
    
    # 1. Récupérer les données
    query = """
        SELECT order_id, item_name 
        FROM order_items 
    """
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        print("Pas assez de données pour entraîner l'IA.")
        return None

    # 2. Préparer le format "Panier" (One-Hot Encoding)
    basket = (df.groupby(['order_id', 'item_name'])['item_name']
              .count().unstack().reset_index().fillna(0)
              .set_index('order_id'))
    
    # Convertir en 0 ou 1
    def encode_units(x):
        return 1 if x >= 1 else 0
    basket_sets = basket.applymap(encode_units)

    # 3. Algorithme Apriori (Trouver les produits fréquents)
    # support=0.1 signifie qu'on garde les combos présents dans 10% des commandes
    frequent_itemsets = apriori(basket_sets, min_support=0.01, use_colnames=True)
    
    if frequent_itemsets.empty:
        print("Aucune tendance trouvée.")
        return None

    # 4. Générer les règles
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    
    # 5. Sauvegarder le cerveau
    with open("model_rules.pkl", "wb") as f:
        pickle.dump(rules, f)
    
    print("Modèle entraîné et sauvegardé (model_rules.pkl) !")
    return rules

if __name__ == "__main__":
    train_model()