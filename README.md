# TIPE-Modele-du-tas-de-sable-abelien
TIPE sur le modèle du tas de sable abélien

Configuration minimale Python 3.6 avec numba. 
Liste des codes:
- La classe SandAutomate permet de manipuler des tas de sable sur des grilles rectangulaires 2D n x m
- clasify_all: Permet de générer toutes les configurations stables jusqu'à 3x3 et de tester pour chacune si elle est récurrente
- stats_from_markov: Permet de simuler le processus markovien et de récupérer des données issues de ce processus: la configuration avec le moins de grains de sable (poids min), le nombre d'apparition de chaque poids de configuration.
- exploit_from_markov: Permet de visualiser et d'exploiter les données générées avec le processus markovien par le code stats_from_markov
- general: Différentes fonctions permettant de manipuler des tas de sable sous forme de tableau numpy se voulant plus efficace que la classe SandAutomate en utilisant notamment la compilation avec numba
- SandPile: Classe pour manipuler toutes les formes de tas de sable définies par la matrice laplacienne. Cependant, c'est la classe de Sagemath que j'ai utilisée pour émettre des conjectures.
- simule_triangle: Permet de simuler l'éboulement d'un tas de sable sur un pavage triangulaire
- svg_render: Permet de créer une image au format svg représentant une grille triangulaire
