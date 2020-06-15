# TIPE-Modele-du-tas-de-sable-abelien
TIPE sur le modèle du tas de sable abélien

Pour comprendre mon TIPE il est utile de lire le MCOT puis la deuxième partie du rapport (la première est une reprise du MCOT). Durant mon TIPE j'ai cherché un critère pour déterminer si une configuration est récurrente à partir de son poids. J'ai eu une approche exhaustive sur des petits cas avec clasify_all puis une approche statistique avec random et markov (constitué chacun d'un code pour générer des données et d'un autre pour les exploiter). J'ai également eu une approche théorique sur le cycles, présente dans la suite du rapport. Ce TIPE pourrait se poursuivre par l'étude des conjectures sur la forme des configuration. Par exemple, la présence d'un motif de bande dans les graphes sur une grille triangulaire. Les grilles triangulaires étant absentes littérature actuelle. On trouvera une ébauche de cette réflexion sur les grilles triangulaires à la fin du rapport.


Configuration minimale Python 3.6 avec numba.

Liste des codes:
- La classe SandAutomate permet de manipuler des tas de sable sur des grilles rectangulaires 2D n x m
- SandPile: Classe pour manipuler toutes les formes de tas de sable définies par la matrice laplacienne. Cependant, c'est la classe de Sagemath que j'ai utilisée pour émettre des conjectures.
- general: Différentes fonctions permettant de manipuler des tas de sable sous forme de tableau numpy se voulant plus efficace que la classe SandAutomate en utilisant notamment la compilation avec numba
- gen_all: Permet de générer toutes les configurations stables pour une taille donnée
- clasify_all: Permet de tester toutes les configurations stables jusqu'à 3x3 et de tester pour chacune si elle est récurrente (donne dénombrement_3x3.png)
- stats_from_markov: Permet de simuler le processus markovien et de récupérer des données issues de ce processus: la configuration avec le moins de grains de sable (poids min), le nombre d'apparition de chaque poids de configuration.
- exploit_from_markov: Permet de visualiser et d'exploiter les données générées avec le processus markovien par le code stats_from_markov (donne stats_markov_100_100_10mi.png)
- stats_from_random: Permet de générer aléatoirement des configurations et de récupérer des données issues de ce processus:
la configuration avec le moins de grains de sable (poids min),
le nombre d'apparition de chaque poids de configuration.
- exploit_from_random: Permet de visualiser et d'exploiter les données générées avec le code stats_from_random
- simule_triangle: Permet de simuler l'éboulement d'un tas de sable sur un pavage triangulaire
- svg_render: Permet de créer une image au format svg représentant une grille triangulaire

![](https://raw.githubusercontent.com/TheoRudkiewicz/TIPE-Modele-du-tas-de-sable-abelien/master/Triangle/186x201_e.png)
