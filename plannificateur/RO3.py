import data
import database
import tools
from peewee import *

def nb_hours(firm):
    nb_hours_day = []
    nb_hours_week = []
    for person in plannificateur.database.Person.select().where(plannificateur.database.Person.firm_name == firm) :
        nb_hours_day.append(person.nb_hour_day)
        nb_hours_week.append(person.nb_hour_week)
    return (nb_hours_day, nb_hours_week)

def persons_available(firm):
    persons = []
    (nb_hours_day, nb_hours_week) = nb_hours(firm)
    for person in plannificateur.database.Person.select().where(plannificateur.database.Person.firm_name == firm):
        if nb_hours_day[person.ident - 1] < 7 or nb_hours_week[person.ident - 1] < 35 :
            persons.append(person.ident)
    return persons

def persons_available_post(firm,post):
    persons = persons_available(firm)
    p_a_p = []
    for person in plannificateur.database.Person.select().join(dplannificateur.atabase.Skill).where(plannificateur.database.Skill.operator == plannificateur.database.Person.ident).where(dplannificateur.atabase.Skill.post == post).where(plannificateur.database.Skill.firm_name == firm).select().order_by(fn.Random()):
        for i in persons :
            if person.ident == i:
                p_a_p.append(i)
    return p_a_p

def planning (firm, nb_packages, nb_articles_package):
    planning = plannificateur.tools.dict_creation(firm)
    nb_person_working = 0
    nb_team = [2 for i in range(0,6)]
    nb_day_more_team = 0
    persons_working = []
    nb_interim_tot = 0
    (nb_hours_day, nb_hours_week) = nb_hours(firm)

    Post_rd = database.Post.select().where(plannificateur.database.Post.firm_name == firm).order_by(fn.Random())
    for post in Post_rd:
        time_needed = plannificateur.tools.time_needed_post(firm, nb_packages, nb_articles_package, post.name)
        time_needed_day_team = [[0,0,0] for i in range (0,6)]
        if time_needed//12 > 7 * 60 * plannificateur.data.nb_max_team:
            nb_day_more_team = (time_needed % (7 * 60 * plannificateur.data.nb_max_team))//6 + 1
            for i in range(0,nb_day_more_team):
                nb_team[i] = 3
        for i in range(0, 6):
            for j in range(0, nb_team[i]):
                time_needed_day_team[i][j] = time_needed / (6 * 2 + nb_day_more_team)

        for i in range(0,6):
            for t in range (0,nb_team[i]):
                while time_needed_day_team[i][t] > 0 :
                    persons = persons_available_post(firm,post)


                    for index in persons:
                        if (7 - nb_hours_day[index-1]) * 60 <= time_needed_day_team[i][t] :
                            time_needed_day_team[i][t] -= (7 - nb_hours_day[index - 1]) * 60
                            nb_hours_week[index - 1] += 7 - nb_hours_day[index - 1]
                            nb_hours_day[index-1] = 7
                            day = plannificateur.data.week[i]
                            team = plannificateur.data.team[t]
                            planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] += 1


                        else:
                            nb_hours_day[index-1] += time_needed_day_team[i][t]/60
                            nb_hours_week[index-1] += time_needed_day_team[i][t]/60
                            time_needed_day_team[i][t] = 0
                            day = plannificateur.data.week[i]
                            team = plannificateur.data.team[t]
                            planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] += 1

                    sum_time_left = 0
                    for index in persons:
                        sum_time_left += nb_hours_day[index - 1]

                    if time_needed_day_team[i][t] > sum_time_left:
                        nb_interim = ((time_needed_day_team[i][t] - sum_time_left) // (7 * 60)) + 1
                        time_needed_day_team[i][t] -= 7 * 60 * nb_interim
                        day = plannificateur.data.week[i]
                        team = plannificateur.data.team[t]
                        planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] += nb_interim
                        nb_interim_tot += nb_interim


    for person in database.Person.select().where(database.Person.firm_name == firm):
        if nb_hours_week[person.ident - 1] > 0 and (person.ident not in persons_working):
            nb_person_working += 1
            persons_working.append(person.ident)

    nb_interims = nb_interim_tot//5 + 1
    nb_person_working += nb_interims

    return (planning, nb_interims, nb_person_working)

