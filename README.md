# FastFoodGo - DevOps & Data Project

**FastFoodGo** est une application full-stack simulant la gestion d'un restaurant, de la prise de commande à l'analyse des données, intégrant un pipeline **DevOps complet** et un module d'**Intelligence Artificielle**.

**Démo en ligne :** [https://fastfoodgo-app.onrender.com](https://fastfoodgo-app.onrender.com) *(Si le lien est actif)*

---

## Aperçu

### Dashboard de Pilotage
> *Génération de commandes en temps réel et suivi du Chiffre d'Affaires.*

### Assistant IA (Cross-Selling)
> *Système de recommandation basé sur l'algorithme Apriori (Market Basket Analysis).*


---

## Stack Technique

* **App Web :** Python, Streamlit, Pandas.
* **Base de Données :** PostgreSQL (Hébergé sur Render Cloud).
* **Intelligence Artificielle :** Scikit-learn / Mlxtend (Règles d'association).
* **Conteneurisation :** Docker & Docker Compose.
* **CI/CD :** GitHub Actions (Tests automatisés) -> Déploiement automatique sur Render.

---

## Installation & Démarrage

### Option 1 : Via Docker (Recommandé)
Le projet est entièrement conteneurisé. Pour le lancer localement :

```bash
# 1. Cloner le projet
git clone [https://github.com/jewandji/fastfoodgo.git](https://github.com/jewandji/fastfoodgo.git)
cd fastfoodgo

# 2. Lancer les services (App + Base de données locale)
docker-compose up --build

L'application sera accessible sur : http://localhost:8501


### Option 2 : Installation Manuelle (Python)
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows

# Installer les dépendances
pip install -e ".[dev]"

# Lancer l'application
streamlit run src/fastfoodgo/web.py
```
