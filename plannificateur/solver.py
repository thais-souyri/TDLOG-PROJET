#Notre idée première etait de réaliser un solveur linéaire pour les petites instances. Le but de ce solveur était de minimiser le nombre d'intérimaires.
#Afin de déterminer ce nombre, nous devions implémenter notre problème linéaire en utilisant le solver CVXPY.
#Nos variables étaient le temps de travail des opérateurs par jour, par équipe et par poste.
#Le temps de travail à effectuer pour expédier tous les colis étant déterminé par nos constantes de notre base de données téléchargées par l'utilisateur, nous pouvions déterminer le temps nécessaire de travail par jour, par équipe et par poste.
#Il fallait ensuite répartir nos opérateurs en CDI en fonction des postes qu'ils pouvaient effectuer et du temps de travail qui leur reste à faire.
#Certaines de nos contraintes étaient donc de vérifier que le temps de travail nécessaire était bien inférieur au temps fourni par les opérateurs en CDI  et les intérimaires, de vérifier que l'opérateur effectuant ce poste appartenait à l'ensemble des opérateurs ayant cette compétence.
#Afin de diminuer le nombre total d'opérateurs et d'intérimaires, notre fonction objectif serait la somme de tous les opérateurs et intérimaires avec un poids plus élevé pour les intérimaires, représentant une pénalité.
#Cependant nous n'avons pas réussi à mettre cela en application, notre solveur ne nous renvoyant pas de résultat.
#Si nous avions réussi, nous aurions pu dans notre fonction main, nous renvoyant le planning final, rajouter une condition permettant de tester la taille de la base de données et d'utiliser ce programme seulement pour les petites instances.