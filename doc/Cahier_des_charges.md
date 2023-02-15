>**Cahier des charges**
> -


Fonctionnalités de base du projet:

L'objectif du projet est de créer une interface WEB permettant à l'utilisateur de créer un planning hebdomadaire optimisant le nombre d'opérateurs en fonction de la volumétrie de colis à expédier. 
Lors de sa première connexion, chaque utilisateur charge trois fichiers csv. Le premier liste tous les employés de l'entreprise, le second les postes disponibles et les indicateurs de performance associés. Enfin, le dernier fichier permet d'indiquer quels employés sont associés à chaque poste.
Enfin, à chaque connexion, l'utilisateur entre les données suivantes : le nombre de colis à expédier dans la semaine et le nombre moyen d'articles par colis.
En sortie, l'algorithme renvoit un planning hebdomadaire détaillant le nombre de personnes par poste, par demi-journée (matin, après-midi, nuit). 

Le planning sera déterminé via un algorithme, choisi parmi trois autres (la fonction main choisit l'algorithme qui est le plus performant). 

Afin de développer l'interface Web, nous utiliserons la framework Flask. 



