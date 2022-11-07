Fonctionnalités de base du projet:

L'objectif du projet est de créer une interface WEB permettant à l'utilisateur de créer un planning hebdomadaire optimisant le nombre d'opérateurs en fonction de la volumétrie de colis à expédier. 
Les données entrées par l'utilisateur sont : le nombre de colis à expédier, la période de l'année (FFA ou non) et le domaine d'activité (1 ou 2)

Afin de réaliser ceci nous créérons plusieurs class : 
- une class tâche comprenant comme attributs le temps d'exécution par article pour cette tâche; les taches précédentes nécessaires pour effectuer cette tâche. 
- une class poste comprenant comme attribut les tâches réalisables par ce poste 
- une class domaine d'activité comprenant comme attributs le nombre d'article moyen par colis 
- une class organisation du travail comprenant comme attribut la période de l'année (nous permettant d'avoir le nombre d'heure disponible dans la semaine)
- une class opérateur comprenant comme attributs le temps de pause nécessaire après un certain nombre d'heures de travail successives (si le temps nous le permet)
- une class clé de répartition 

Le planning optimal sera déterminé grâce au résultat d'un problème d'optimisation linéaire. 
La fonction objectif sera donc la somme du nombre d'opérateurs par poste. Avec comme contraintes le nombre de colis expédiés à atteindre à la fin de la semaine, l'ordre des tâches. (d'autres contraintes seront certainement à rajouter) 

Afin de développer l'interface Web, nous utiliserons la framework Flask. 


Afin d'améliorer 
