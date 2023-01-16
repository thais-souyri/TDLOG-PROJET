import RO
#import RO2
#import RO4
#import solver
import data
import database


def main(nb_packages,activity_field):
    if len(database.Skill) < data.max_height_database:
        (planning, nb_interim, nb_person) = planning(nb_packages, activity_field)
    else :
        (planning, nb_interim, nb_person) = RO.planning(nb_packages, activity_field)
        #(planning2, nb_interim2, nb_person2) = RO2.planning(nb_packages, activity_field)
        #if nb_person2 < nb_person :
            #(planning, nb_interim, nb_person) = (planning2, nb_interim2, nb_person2)
        #(planning2, nb_interim2, nb_person2) = RO4.planning(nb_packages, activity_field)
        #if nb_person2 < nb_person :
            #(planning, nb_interim, nb_person) = (planning2, nb_interim2, nb_person2)
    return (planning, nb_interim, nb_person)

print(main(100,2))
