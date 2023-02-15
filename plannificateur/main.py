import model.data
import model.database
import plannificateur.tools
import plannificateur.RO
import plannificateur.RO2
import plannificateur.RO4
#import plannificateur.solver



def main(firm, nb_packages, nb_articles_package):
    if plannificateur.tools.time_needed(firm, nb_packages, nb_articles_package) > 6 * 7 * 60 * model.data.nb_max_team :
        return "La livraison ne peut être effectuée, il y a trop d'articles"


    nb_skill = 0
    for skill in model.database.Skill.select().where(model.database.Skill.firm_name == firm):
        nb_skill +=1
    if nb_skill < model.data.max_height_database:
        #(planning, nb_interim, nb_person) = plannificateur.solver.planning(firm, nb_packages, nb_articles_package)
        pass
    else :
        (planning, nb_interim, nb_person) = plannificateur.RO.planning(firm, nb_packages, nb_articles_package)
        (planning2, nb_interim2, nb_person2) = plannificateur.RO2.planning(firm, nb_packages, nb_articles_package)
        if nb_person2 < nb_person :
            (planning, nb_interim, nb_person) = (planning2, nb_interim2, nb_person2)
        (planning2, nb_interim2, nb_person2) = plannificateur.RO4.planning(firm, nb_packages, nb_articles_package)
        if nb_person2 < nb_person :
            (planning, nb_interim, nb_person) = (planning2, nb_interim2, nb_person2)
    return (planning, nb_interim, nb_person)

print(main("a",2000,1.8))