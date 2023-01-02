import data
import random as rd

def nb_operators_needed(nb_pakages, month, activity_field,post):
    return rd.randint(0,7)

def total_operators(nb_pakages, month, activity_field):
    sum = 0
    for i in range(0,data.nb_posts):
        sum+= nb_operators_needed(nb_pakages, month, activity_field, data.posts[i])
    return sum

def nb_teams_needed(nb_pakages, month, activity_field):
    return rd.randint(2,3)

def nb_operators_available(nb_pakages, month, activity_field):
    return rd.randint(0,10)

def main(nb_pakages, month, activity_field):
    planning = {}
    for j in range(0, 7):
        day = data.week[j]
        planning["{}".format(day)] = {}
        teams_needed = nb_teams_needed(nb_pakages, month, activity_field)
        for k in range(0, teams_needed):
            team = data.team[k]
            planning["{}".format(day)]["{}".format(team)] = {}
            for i in range(0, data.nb_posts):
                post = data.posts[i]
                planning["{}".format(day)]["{}".format(team)]["{}".format(post)]= nb_operators_needed(nb_pakages, month, activity_field,post)
    nb_interim = total_operators(nb_pakages, month, activity_field) - nb_operators_available(nb_pakages, month, activity_field)
    return (planning,nb_interim)

(nb_pakages, month, activity_field) = (0,"janvier",0)

(planning,nb_interim)= main(nb_pakages, month, activity_field)



