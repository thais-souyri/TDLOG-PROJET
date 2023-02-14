>**Plannificateur des effectifs dans un entrepôt**

**Principe**:

Le site web, qui comprend un système d'authentification, permet à l'utilisateur d'obtenir un planning indiquant le nombre d'opérateurs nécessaire en renseignant préalablement 
le nombre de colis et le nombre de pièces par colis ainsi que trois fichiers csv caractérisant l'entrepôt (postes, employés, compétences).

**Pour faire fonctionner l'application**:

Il faut run le fichier python "app.py". Le lien obtenu permet d'accéder au site internet.



**Explication des différents dossiers**:

-doc: contient le cahier des charges du projet

-model: contient tous les fichiers relatifs à la création de la base de données. Il y a également trois fichiers csv types pour tester l'application: "person.csv", "post.csv" et "skill.csv"

-plannificateur: contient les fichiers python permettant d'effectuer les calculs 

-static: contient les images et le fichier "main.css" avec l'essentiel du code css utilisé 

-templates: contient les pages html 

-uploads: dossier où seront uploadés les fichiers csv choisis par l'utilisateur 


**Améliorations clés par rapport à la soutenance**:

-L'utilisateur ne doit uploader ses trois fichiers csv que lors de sa première connexion suivant l'inscription. Ensuite, à chaque connexion, il doit simplement renseigner le nombre de colis à traiter et le nombre de pièces par colis 

