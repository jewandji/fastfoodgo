\# FastFoodGo



Plateforme de commande de repas en ligne (Projet DevOps \& Data).



\## Installation



1\. Cloner le dépôt :

&nbsp;  ```bash

&nbsp;  git clone <URL\_DU\_REPO>

&nbsp;  cd fastfoodgo



2\. Installer les dépendances en mode éditable :

   ```bash

&nbsp;  pip install -e ".\[dev]"



\## Lancer les tests



Pour exécuter la suite de tests unitaires :



   ```bash

   python -m pytest





Intégration Continue (CI)



Ce projet utilise GitHub Actions. À chaque Pull Request, le workflow :



1. Installe l'environnement Python.



2\. Installe les dépendances via pyproject.toml.



3\. Exécute automatiquement les tests pytest.



Si les tests échouent, le merge est bloqué (protection de branche main).











