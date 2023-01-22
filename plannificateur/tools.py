import data
import database

def dict_creation(firm) :
    planning = {}
    for j in range(0, 6):
        day = plannificateur.data.week[j]
        planning["{}".format(day)] = {}
        for k in range(0, 3):
            team = plannificateur.data.team[k]
            planning["{}".format(day)]["{}".format(team)] = {}
            for post in plannificateur.database.Post.select().where(plannificateur.database.Post.firm_name == firm):
                planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] = 0
    return planning



def time_needed_post(firm, nb_packages, nb_articles_package,post):
    for post in plannificateur.database.Post.select().where(database.Post.name == post).where(plannificateur.database.Post.firm_name == firm):
        t = nb_packages * post.time
        if post.action_on_article :
            time = t * nb_articles_package
        else :
            time = t
    return time

def time_needed(firm, nb_packages, nb_articles_package):
    sum = 0
    for post in plannificateur.database.Post.select().where(plannificateur.database.Post.firm_name == firm):
        sum += time_needed_post(firm,nb_packages, nb_articles_package,post.name)
    return sum

def persons_available(firm):
    persons_available = plannificateur.database.Person.select().where(plannificateur.database.Person.nb_hour_day < 7).where(plannificateur.database.Person.nb_hour_week < 35).where(plannificateur.database.Person.firm_name == firm)
    return persons_available

def persons_available_post(firm, post):
    p_a = persons_available(firm)
    persons = p_a.select().join(plannificateur.database.Skill).where(plannificateur.database.Skill.operator == persons_available).where(plannificateur.database.Skill.post == post).where(plannificateur.database.Skill.firm_name == firm)
    return persons

def need_interim(firm,post):
    persons_available = plannificateur.database.Person.select().where(dplannificateur.atabase.Person.nb_hour_day < 7).where(plannificateur.database.Person.nb_hour_week < 35).where(plannificateur.database.Person.firm_name == firm)
    persons_available_post = persons_available.select().join(plannificateur.database.Skill).where(plannificateur.database.Skill.operator == persons_available).where(plannificateur.database.Skill.post == post).where(plannificateur.database.Skill.firm_name == firm)
    sum = 0
    need = False
    for p in persons_available_post:
        sum +=1
    if sum != 0 :
        need = True
    return need



def nb_person(firm):
    nb_person = 0
    for person in plannificateur.database.Person.select().where(plannificateur.database.Person.firm_name == firm):
        nb_person += 1
    return nb_person

def nb_post(firm):
    nb_post = 0
    for post in plannificateur.database.Post.select().where(plannificateur.database.Post.firm_name == firm):
        nb_post += 1
    return nb_post

def total_operators(firm, planning):
    sum = 0
    for i in range(0,6):
        day = plannificateur.data.week[i]
        for t in range (0,3):
            team = data.team[t]
            for post in plannificateur.database.Post.select().where(plannificateur.database.Post.firm_name == firm) :
                sum += planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)]
    return sum


