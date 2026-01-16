import pickle
import numpy as np
import sys
import os

MODEL_PATH = "recommender_model.pkl"

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Le modèle n'existe pas. Lancez d'abord ml_train.py !")
    
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

def recommend(item_name):
    artifact = load_model()
    vectorizer = artifact["vectorizer"]
    cooc_matrix = artifact["cooc_matrix"]
    feature_names = artifact["feature_names"]
    
    # 1. Trouver l'index du produit demandé
    # Le vectorizer met tout en minuscule, on s'adapte
    clean_name = item_name.lower()
    
    try:
        # On cherche le mot clé dans le vocabulaire (ex: "burger" dans "burger classique")
        # Simplification : on prend le premier token qui matche
        token_index = -1
        for word in clean_name.split():
            if word in vectorizer.vocabulary_:
                token_index = vectorizer.vocabulary_[word]
                break
        
        if token_index == -1:
            return "Aucune recommandation (Produit inconnu)"

        # 2. Regarder dans la matrice ce qui est le plus proche
        # On prend la ligne correspondante dans la matrice de co-occurrence
        row = cooc_matrix.getrow(token_index).toarray()[0]
        
        # On trouve l'index de la valeur maximale (le produit le plus souvent associé)
        best_match_index = row.argmax()
        
        # Si le score est 0, pas d'association forte
        if row[best_match_index] == 0:
             return "Pas assez de données pour recommander."

        recommended_word = feature_names[best_match_index]
        
        # On essaie de retrouver un nom "joli" correspondant au token (approximation simple)
        return f"Avec '{item_name}', les clients achètent souvent : {recommended_word.upper()}"

    except Exception as e:
        return f"Erreur lors de la recommandation : {e}"

if __name__ == "__main__":
    # Test interactif
    print("--- AGENT IA FASTFOODGO ---")
    
    # Exemples de tests
    test_items = ["Burger Classique", "Salade César", "Frites"]
    
    for item in test_items:
        print(f"Client achète : {item}")
        print(recommend(item))
        print("-" * 20)