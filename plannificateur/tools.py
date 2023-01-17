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
    time_needed = nb_packages * database.Post.time[activity_field - 1][post.index]
    if post.action_on_article :
        time_needed = time_needed * activity_field.nb_article_package
    return time_needed

def time_needed(nb_packages, activity_field,post):
    sum = 0
    for post in database.Post.select():
        sum += time_needed_post(nb_packages, activity_field,post.name):
    return post.name

def persons_available():
    persons_available = database.Person.select().where(database.Person.nb_hour_day > 0 & database.Person.nb_hour_week > 0)
    return persons_available

def persons_availbale_post(post):
    persons_available = persons_available()
    persons = persons_available.where(database.Skill.operrator == persons_available & database.Skill.post == post)
    return persons

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

def total_operators(planning):
    sum = 0
    for i in range(0,6):
        day = data.week[i]
        for t in range (0,3):
            team = data.team[t]
            for post in database.Post.select() :
                sum+= planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)]
    return sum


