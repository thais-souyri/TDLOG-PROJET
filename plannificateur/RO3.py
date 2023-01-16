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
    for post in database.Post.select() :
        time_needed = tools.time_needed_post(nb_packages, activity_field, post.name)
        time_needed_day = []
        if time_needed//12 > 7 * data.nb_max_team:
            nb_day_more_team = (time_needed% 6 * data.nb_max_team)//7 + 1
            for i in range(0,nb_day_more_team):
                nb_team[i] = 3
        for i in range(0, 6):
            time_needed_day.append([time_needed // 6 * nb_team[i] for j in range(0,nb_team[i])])
        for time in time_needed_day:
            time_needed -= time
        while time_needed > 0 :
            d = rd.randint(0,5)
            h = rd.randrange(0,time_needed)
            time_needed_day[d] += h
            time_needed -= h

        for i in range(0,6):
            while time_needed_day[i] > 0 :
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
                    time_needed_day[i] -= 7
                day = data.week[i]
                planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] +=1

        for person in data.Person.selct():
            if person.nb_hour_week < 35 :
                nb_person += 1
        nb_person += nb_interim
    return (planning,nb_person,nb_interim)





