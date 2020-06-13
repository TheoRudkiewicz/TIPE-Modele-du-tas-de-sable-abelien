# TIPE-Mod-le-du-tas-de-sable-ab-lien
TIPE sur le modèle du tas de sable abélien


Liste des codes:
- La classe SandAutomate permet de manipuler des tas de sable sur des grilles rectangulaires
- clasify_all: Permet de générer toutes les configurations stables jusqu'à 3x3 et de tester pour chacune si elle est récurrente
- exploit_from_markov: Permet de visualiser et d'exploiter les données généré avec le processus markovien par le code: stats_from_markov
- general: Différentes fonctions permettant de manipuler des tas de sable sous formes de tableau numpy
se voulant plus efficace que la classe en utilisant notamment la compilation avec numba
- stats_from_markov: Permet de simuler le processus markovien et de récupérer des données issues de ce porcessus: la configuration avec le moins de grains de sable (poids min),  le nombre d'apparition de chaque poids de configuration.
- SandPile: Classe pour manipuler toutes les formes de tas de sable définit par la matrice laplacienne. Cependant, c'est la classe de Sagemath que j'ai utilisé
- simule_triangle: Permet de simuler l'éboulement d'un tas de sable sur un pavage triangulaire
- svg_render: Permet de créé un svg représenatant une grille triangulaire
