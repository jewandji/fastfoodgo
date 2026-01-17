import pickle
import os
import pandas as pd
from fastfoodgo.ml_train import train_model

MODEL_FILE = "model_rules.pkl"

def load_model():
    """Charge le modèle. S'il n'existe pas, on l'entraîne à la volée."""
    if not os.path.exists(MODEL_FILE):
        print("Modèle introuvable. Lancement de l'auto-entraînement...")
        train_model()
    
    try:
        with open(MODEL_FILE, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

def recommend(current_item):
    rules = load_model()
    
    if rules is None or not isinstance(rules, pd.DataFrame):
        return "Pas assez de données pour une recommandation."

    # On cherche les règles où l'antécédent contient notre produit
    # (En gros : "Si les gens achètent X (current_item), ils prennent quoi ?")
    rec = rules[rules['antecedents'].apply(lambda x: current_item in x)]
    
    if not rec.empty:
        # On prend celui avec la plus forte confiance
        best_match = rec.sort_values('confidence', ascending=False).iloc[0]
        suggested = list(best_match['consequents'])[0]
        return f"Avec {current_item}, les clients adorent : **{suggested}** ! (Confiance : {best_match['confidence']:.0%})"
    else:
        return f"Excellente choix ! Un **Soda** irait bien avec {current_item}."