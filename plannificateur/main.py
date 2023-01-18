import RO
#import RO2
#import RO4
#import solver
import data
import database
import tools


def main(nb_packages,activity_field):
    if tools.time_needed(nb_packages, activity_field) > 6 * 7 * data.nb_max_team :
        return "La livraison ne peut être effectuée, il y a trop d'articles"

    nb_skill = 0
    for skill in database.Skill.select():
        nb_skill +=1
    if nb_skill < data.max_height_database:
        (planning, nb_interim, nb_person) = planning(nb_packages, activity_field)
    else :
        (planning, nb_interim, nb_person) = RO.planning(nb_packages, activity_field)
        (planning2, nb_interim2, nb_person2) = RO2.planning(nb_packages, activity_field)
        if nb_person2 < nb_person :
            (planning, nb_interim, nb_person) = (planning2, nb_interim2, nb_person2)
        (planning2, nb_interim2, nb_person2) = RO4.planning(nb_packages, activity_field)
        if nb_person2 < nb_person :
            (planning, nb_interim, nb_person) = (planning2, nb_interim2, nb_person2)
    return (planning, nb_interim, nb_person)

