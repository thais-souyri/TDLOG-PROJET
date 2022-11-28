import data
import random as rd

def main(nb_pakages, month, activity_field):
    planning = [[] for i in range (0,6)]
    for j in range(0, 6):
        for i in range (0,data.nb_operators):
            team = rd.randint(0, 3)
            nb_posts = rd.randint(0, 3)
            posts = [rd.randint(0,6) for i in range(0, nb_posts)]
            planning[j].append([team,posts])
    nb_interim = rd.randint(0,12)
    return (planning,nb_interim)

(nb_pakages, month, activity_field) = (0,0,0)

(planning,nb_interim)= main(nb_pakages, month, activity_field)

print(planning)

