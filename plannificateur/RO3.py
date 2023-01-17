import data
import database
import tools
import random as rd
from peewee import *



def main (activity_field, nb_packages):
    planning = tools.dict_creation()
    nb_person = 0
    nb_interim = 0
    nb_team = [2 for i in range(0,6)]
    nb_day_more_team = 0
    for post in database.Post.select() :
        time_needed = tools.time_needed_post(nb_packages, activity_field, post.name)
        time_needed_day_team = [[0,0,0] for i in range (0,6)]
        if time_needed//12 > 7 * data.nb_max_team:
            nb_day_more_team = (time_needed% 7 * data.nb_max_team)//6 + 1
            for i in range(0,nb_day_more_team):
                nb_team[i] = 3
        for i in range(0, 6):
            for j in range(0, nb_team[i]):
                time_needed_day_team[i][j] = time_needed // 6 * 2 + nb_day_more_team
        if nb_day_more_team != 0 :
            time_needed_day_team[nb_day_more_team - 1 ][2] = time_needed % 6 * 2 + nb_day_more_team


        for i in range(0,6):
            for t in range (0,nb_team[i]):
                while time_needed_day_team[i] > 0 :
                    if not tools.need_interim() :
                        qualified = False
                        while not qualified :
                            persons_available = tools.persons_available().order_by(fn.Random())
                            person = persons_available.get()
                            for skill in database.Skill.select():
                                if skill.operator == person.index and skill.post == post.index :
                                    qualified = True
                        if person.nb_hour_day < time_needed_day[i] :
                            person.nb_hour_day = 0
                            person.nb_hour_week -= person.nb_hour_day
                            time_needed_day[i] -= person.nb_hour_day
                        else :
                            person.nb_hour_day -= time_needed_day[i]
                            person.nb_hour_week -= time_needed_day[i]
                            time_needed_day[i] = 0
                    else :
                        nb_interim += 1
                        time_needed_day_team[i] -= 7
                    day = data.week[i]
                    team = data.team[t]
                    planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] +=1

        for person in data.Person.selct():
            if person.nb_hour_week < 35 :
                nb_person += 1
        nb_person += nb_interim
    print(main(activity_field, nb_packages))
    return (planning,nb_person,nb_interim)

nb_packages = 10
activity_field = 1
(planning,nb_interim)= main(nb_packages, activity_field)