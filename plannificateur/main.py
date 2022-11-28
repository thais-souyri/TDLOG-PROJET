import RO
import tabulate
import data

print ('Veuillez entrer le nombre de colis à expédier dans la semaine: ')
nb_package = input()

print ("Veuillez entrer le secteur d'activité: ")
print('1. C-discount')
print('2. BR')
activity_field_index = input()

print ("Veuillez indiquer le mois de l'année:")
month = input()


(planning, nb_interim) = RO.main(nb_package, month, activity_field_index)

print("Le nombre d'intérimaires nécessaire sera de {}".format(nb_interim))

print("Le planning d'organisation de la semaine est le suivant :")

for i in range (0,6):
    print("{}".format(data.week[i]))
    print(tabulate(planning[i], headers=["Team", "Posts"]))


print(tabulate(planning, headers=["Name", "Age", "Percent"]))





