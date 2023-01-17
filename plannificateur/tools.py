import data
import database

def dict_creation() :
    planning = {}
    for j in range(0, 7):
        day = data.week[j]
        planning["{}".format(day)] = {}
        for k in range(0, 3):
            team = data.team[k]
            planning["{}".format(day)]["{}".format(team)] = {}
            for post in database.Post.select():
                planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] = 0
    return planning

def time_needed_post(nb_packages, activity_field,post):
    time_needed = nb_packages * database.Post.timepost_time[activity_field - 1][post.index]
    if post.index < 4:
        time_needed = time_needed * activity_field.nb_article_package
    return time_needed

def persons_available():
    persons_available = database.Person.select().where(database.Person.nb_hour_day > 0 & database.Person.nb_hour_week > 0)
    return persons_available

def need_interim():
    persons = persons_available()
    need = False
    if len(persons) == 0 :
        need = True
    return need

def nb_person():
    nb_person = 0
    for person in database.Person.select():
        nb_person += 1
    return nb_person

def nb_post():
    nb_post = 0
    for post in database.Post.select():
        nb_post += 1
    return nb_post

def time_needed_day(time_needed_day_team) :
    time = 0
    time_needed_day = []
    for i in range (0,6):
        for j in range (0,3):
            time += time_needed_day_team[i][j]
        time_needed_day. append(time)
    return time_needed_day
