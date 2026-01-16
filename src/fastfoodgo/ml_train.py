import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from fastfoodgo.database import get_db_connection

def train_model():
    print("Démarrage de l'entraînement du modèle de recommandation...")
    conn = get_db_connection()
    
    # 1. Charger les données : On veut grouper les items par commande
    # Ex: Commande 1 -> "Burger Frites Soda"
    query = """
        SELECT order_id, STRING_AGG(item_name, ' ') as items
        FROM order_items
        GROUP BY order_id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    
    if len(df) < 5:
        print("Pas assez de données pour entraîner un modèle fiable. Générez plus de commandes avec seed.py !")
        return

    print(f"Entraînement sur {len(df)} commandes historiques.")

    # 2. Créer la matrice de co-occurrence
    # On regarde quels items apparaissent souvent ensemble
    vectorizer = CountVectorizer(token_pattern=r"(?u)\b\w+\b|\b\w+\s\w+\b") # Gère les noms composés
    X = vectorizer.fit_transform(df['items'])
    
    # Calcul de la matrice de co-occurrence (X transoposé * X)
    cooc_matrix = (X.T * X) 
    cooc_matrix.setdiag(0) # On ne recommande pas un item s'il est déjà là (Burger -> Burger)
    
    # 3. Sauvegarder le modèle (Artifact)
    # En MLOps, on versionne le modèle comme du code
    model_artifact = {
        "vectorizer": vectorizer,
        "cooc_matrix": cooc_matrix,
        "feature_names": vectorizer.get_feature_names_out()
    }
    
    with open("recommender_model.pkl", "wb") as f:
        pickle.dump(model_artifact, f)
        
    print("Modèle entraîné et sauvegardé dans 'recommender_model.pkl'")

if __name__ == "__main__":
    train_model()