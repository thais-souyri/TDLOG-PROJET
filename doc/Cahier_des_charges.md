Fonctionnalités de base du projet:

L'objectif du projet est de créer une interface WEB permettant à l'utilisateur de créer un planning hebdomadaire optimisant le nombre d'opérateurs en fonction de la volumétrie de colis à expédier. 
Lors de sa première connexion, chaque utilisateur télécharge trois fichiers csv. Le premier liste tous les employés de l'entreprise, le second les postes disponibles et les indicateurs de performance associés. Enfin, le dernier fichier permet d'indiquer quels employés sont associés à chaque poste.
Enfin, à chaque connexion, l'utilisateur entre les données suivantes : le nombre de colis à expédier dans la semaine et le nombre moyen d'articles par colis.
En sortie, l'algorithme renvoit un planning hebdomadaire détaillant le nombre de personnes par poste, par demi-journée. 

Afin de réaliser ceci, nous avons créé une base de données composée de plusieurs tables: 
- une class tâche comprenant comme attributs le temps d'exécution par article pour cette tâche; les taches précédentes nécessaires pour effectuer cette tâche. 
- une class poste comprenant comme attribut les tâches réalisables par ce poste 
- une class domaine d'activité comprenant comme attributs le nombre d'article moyen par colis 
- une class organisation du travail comprenant comme attribut la période de l'année (nous permettant d'avoir le nombre d'heure disponible dans la semaine)
- une class opérateur comprenant comme attributs le temps de pause nécessaire après un certain nombre d'heures de travail successives (si le temps nous le permet)
- une class clé de répartition comprenant comme attributs le domaine d'activité et la préiode de l'année

Le planning optimal sera déterminé dans l'idéal grâce au résultat d'un problème d'optimisation linéaire. 
La fonction objectif sera donc la somme du nombre d'opérateurs par poste. Avec comme contraintes le nombre de colis expédiés à atteindre à la fin de la semaine, l'ordre des tâches. (d'autres contraintes seront certainement à rajouter). Pour cela, nous utiliserons la bibliothèque Pulp. 

Afin de développer l'interface Web, nous utiliserons la framework Flask. 



