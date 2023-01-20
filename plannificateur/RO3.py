
import data
import database
import tools
from peewee import *



def planning (firm, nb_packages, nb_articles_package):
    planning = tools.dict_creation(firm)
    nb_person_working = 0
    nb_interim = 0
    nb_team = [2 for i in range(0,6)]
    nb_day_more_team = 0
    persons_working = []
    nb_interim_tot = 0
    for post in database.Post.select().where(database.Post.firm_name == firm).order_by(fn.Random()):
        time_needed = tools.time_needed_post(firm, nb_packages, nb_articles_package, post.name)
        time_needed_day_team = [[0,0,0] for i in range (0,6)]
        if time_needed//12 > 7 * data.nb_max_team:
            nb_day_more_team = (time_needed% 7 * data.nb_max_team)//6 + 1
            for i in range(0,nb_day_more_team):
                nb_team[i] = 3
        for i in range(0, 6):
            for j in range(0, nb_team[i]):
                time_needed_day_team[i][j] = time_needed // 6 * 2 + nb_day_more_team
        if nb_day_more_team != 0 :
            time_needed_day_team[nb_day_more_team - 1][2] = time_needed % 6 * 2 + nb_day_more_team

        for i in range(0,6):
            for t in range (0,nb_team[i]):
                while time_needed_day_team[i][t] > 0 :
                    persons_available = database.Person.select().where(database.Person.nb_hour_day < 7).where(database.Person.nb_hour_week < 35).where(database.Person.firm_name == firm)
                    persons = persons_available.join(database.Skill).where(database.Skill.operator == persons_available).where(database.Skill.post == post).where(database.Skill.firm_name == firm).select().order_by(fn.Random())
                    nb_persons = 0
                    for person in persons :
                        nb_persons += 1
                        if person.nb_hour_day < time_needed_day_team[i][t] :
                            value_day = person.nb_hour_day + 7
                            value_week = person.nb_hour_week + person.nb_hour_day
                            time_needed_day_team[i][t] -= person.nb_hour_day
                            print(time_needed_day_team[i][t])
                            query = database.Person.update(nb_hour_day=value_day).where(
                                database.Person.ident == person.ident)
                            query.execute()
                            query = database.Person.update(nb_hour_day=value_week).where(
                                database.Person.ident == person.ident)
                            query.execute()
                            day = data.week[i]
                            team = data.team[t]
                            planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] += 1

                        else :
                            value_day = person.nb_hour_day + time_needed_day_team[i][t]
                            value_week = person.nb_hour_week + time_needed_day_team[i][t]
                            query = database.Person.update(nb_hour_day = value_day).where(database.Person.ident == person.ident)
                            query.execute()
                            query = database.Person.update(nb_hour_day = value_week).where(database.Person.ident == person.ident)
                            query.execute()
                            time_needed_day_team[i][t] = 0
                            day = data.week[i]
                            team = data.team[t]
                            planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] += 1

                    if time_needed_day_team[i][t] > nb_persons * 7:
                        nb_interim = ((time_needed_day_team[i][t] - nb_persons * 7)//7) +1
                        time_needed_day_team[i][t] -= 7 * nb_interim
                        day = data.week[i]
                        team = data.team[t]
                        planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] += nb_interim
                        nb_interim_tot += nb_interim

        for person in database.Person.select().where(database.Person.firm_name == firm):
            print(person.nb_hour_day)
            if (person.nb_hour_week > 0) and (person.name not in persons_working):
                nb_person_working += 1
                persons_working.append(person.name)


        #nb_person_working += nb_interim_tot
    query = database.Person.update(nb_hour_day=0)
    query.execute()
    query = database.Person.update(nb_hour_day=0)
    query.execute()
    return (planning, nb_interim_tot, nb_person_working)

print(planning('a',500,1.8))