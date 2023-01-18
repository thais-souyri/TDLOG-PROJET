import RO3
import data

def planning(nb_packages, activity_field):
    (planning, nb_interim, nb_operator) = RO3.planning(nb_packages, activity_field)
    for i in range(0,data.nb_run_RO):
        (p,i,o) = RO3.planning(nb_packages, activity_field)
        if o < nb_operator :
            (planning, nb_interim, nb_operator) = (p,i,o)
    return (planning, nb_interim, nb_operator)