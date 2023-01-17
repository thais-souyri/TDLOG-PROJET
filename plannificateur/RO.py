import data
import tools
import database
import random as rd

def nb_operators(nb_pakages, activity_field,post):
    persons_available = tools.persons_available()
    sum = 0
    for person in persons_available.select():
        sum +=1
    return rd.randint(0,sum)

def nb_teams_needed(nb_pakages, activity_field):
    nb_team = [2 for i in range(0, 6)]
    time_available = sum(nb_team) * 7 * data.nb_max_team
    while tools.time_needed() < time_available :
        for i in range(0,6):
            nb_team[i] = rd.randint(2,3)
    return nb_team

def planning(nb_pakages, activity_field):
    planning = tools.dict_creation()
    nb_teams = nb_teams_needed(nb_pakages, activity_field)
    for post in database.Post.select()
        time_needed = tools.time_needed_post()
        while time_needed > 0 :
            for j in range(0, 6):
                day = data.week[j]
                    team = rd.randint(nb_teams[i])
                    nb_operators = nb_operators(nb_pakages, activity_field, post.name)
                    planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] = nb_operators_needed(nb_pakages, activity_field,post)

    nb_interim = total_operators(nb_pakages, activity_field) - nb_operators_available(nb_pakages, activity_field)
    return (planning,nb_interim,nb_person)





