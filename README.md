# FastFoodGo - DevOps & Data Project

**FastFoodGo** est une application full-stack simulant la gestion d'un restaurant, de la prise de commande à l'analyse des données, intégrant un pipeline **DevOps complet** et un module d'**Intelligence Artificielle**.

**Démo en ligne :** [https://fastfoodgo-app.onrender.com](https://fastfoodgo-app.onrender.com) *(Service et base de données suspendu par moment donc le site est mise en arrêt si pour éviter de gaspiller les ressources gratuites de Render)*

---

## Aperçu

### Dashboard de Pilotage
> *Génération de commandes en temps réel et suivi du Chiffre d'Affaires.*
<img width="826" height="409" alt="image" src="https://github.com/user-attachments/assets/d08299e4-c31a-43ed-8c78-57681f570477" />

> <img width="284" height="415" alt="image" src="https://github.com/user-attachments/assets/6fd2d471-173e-4da2-8123-0dcdb888503a" />


### Assistant IA (Cross-Selling)
> *Système de recommandation basé sur l'algorithme Apriori (Market Basket Analysis).*
> <img width="836" height="416" alt="image" src="https://github.com/user-attachments/assets/78620379-152f-4c3e-bbb8-cc1d241d9ae7" />



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
```

L'application sera accessible sur : http://localhost:8501


### Option 2 : Installation Manuelle (Python)

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows

# Installer les dépendances
pip install -e ".[dev]"

# Lancer l'application
streamlit run src/fastfoodgo/web.py
```
