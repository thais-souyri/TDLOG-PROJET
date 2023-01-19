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



def time_needed_post(firm, nb_packages, nb_articles_package,post):
    time_needed = nb_packages * database.Post.time.where(database.Person.firm_name == firm)
    if post.action_on_article :
        time_needed = time_needed * nb_articles_packages
    return time_needed

def time_needed(firm, nb_packages, nb_articles_package, post):
    sum = 0
    for post in database.Post.select().where(database.Person.firm_name == firm):
        sum += time_needed_post(firm,nb_packages, nb_articles_package,post.name)
    return post.name

def persons_available(firm):
    persons_available = database.Person.select().where(database.Person.nb_hour_day > 0 & database.Person.nb_hour_week > 0 & database.Person.firm_name == firm)
    return persons_available

def persons_available_post(firm, post):
    p_a = persons_available()
    persons = p_a.where(database.Skill.operrator == persons_available & database.Skill.post == post).where(database.Skill.firm_name == firm)
    return persons

def need_interim(firm):
    persons = persons_available(firm)
    need = False
    if len(persons) == 0 :
        need = True
    return need

def nb_person(firm):
    nb_person = 0
    for person in database.Person.select().where(database.Person.firm_name == firm):
        nb_person += 1
    return nb_person

def nb_post(firm):
    nb_post = 0
    for post in database.Post.select().where(database.Person.firm_name == firm):
        nb_post += 1
    return nb_post

def total_operators(firm, planning):
    sum = 0
    for i in range(0,6):
        day = data.week[i]
        for t in range (0,3):
            team = data.team[t]
            for post in database.Post.select().where(database.Person.firm_name == firm) :
                sum+= planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)]
    return sum


