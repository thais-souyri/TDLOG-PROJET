import data
import tools
import database
import random as rd

def nb_operators(firm, nb_pakages, nb_article_packages, post):
    persons_available = tools.persons_available()
    sum = 0
    for person in persons_available.select():
        sum +=1
    return rd.randint(0,sum)

def nb_teams_needed(firm, nb_packages, nb_articles_package):
    nb_team = [2 for i in range(0, 6)]
    time_available = sum(nb_team) * 7 * data.nb_max_team
    while tools.time_needed(firm, nb_packages, nb_articles_package) < time_available :
        for i in range(0,6):
            nb_team[i] = rd.randint(2,3)
    return nb_team

def planning(firm, nb_packages, nb_article_packages):
    planning = tools.dict_creation()
    nb_teams = nb_teams_needed(firm, nb_packages, nb_article_packages)
    tot_interim = 0
    for post in database.Post.select().where(database.Post.firm_name == firm):
        time_needed = tools.time_needed_post()
        while time_needed > 0 :
            for j in range(0, 6):
                day = data.week[j]
                team = rd.randint(nb_teams[j])
                nb_operators = nb_operators(nb_packages, activity_field, post.name)
                time_needed -= nb_operators * 7
                planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] = nb_operators_needed(nb_pakages, activity_field,post)
            day = rd.randint(0,6)
            team = rd.randint(nb_teams[day])
            nb_interim = rd.randint((time_needed//7) + 1)
            if nb_interim + planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] < data.nb_max_team:
                planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] += nb_interim
                time_needed -= nb_interim*7
                tot_interim += nb_interim
    nb_person = tools.total_operators(planning)
    return (planning, tot_interim, nb_person)

planning("a",12,1.8)






