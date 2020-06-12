# TIPE-Mod-le-du-tas-de-sable-ab-lien
TIPE sur le modèle du tas de sable abélien


Liste des codes:
- La classe SandAutomate permet de manipuler des tas de sable sur des grilles rectangulaires
- clasify_all: Permet de générer toutes les configurations stables jusqu'à 3x3 et de tester pour chacune si elle est récurrente
- exploit_from_markov: Permet de visualiser et d'exploiter les données généré avec le processus markovien par le code: stats_from_markov
- general: Différentes fonctions permettant de manipuler des tas de sable sous formes de tableau numpy
se voulant plus efficace que la classe en utilisant notamment la compilation avec numba
- stats_from_markov: Permet de simuler le processus markovien et de récupérer des données issues de ce porcessus: la configuration avec le moins de grains de sable (poids min),  le nombre d'apparition de chaque poids de configuration.
