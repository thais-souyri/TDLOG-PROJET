import model.data
import model.database
import plannificateur.tools
from peewee import *

def nb_hours(firm): #renvoie le nombre d'heures travaillées par jour et par semaine
    nb_hours_day = []
    nb_hours_week = []
    for person in model.database.Person.select().where(model.database.Person.firm_name == firm) :
        nb_hours_day.append(person.nb_hour_day)
        nb_hours_week.append(person.nb_hour_week)
    return (nb_hours_day, nb_hours_week)

def persons_available(firm): #renvoie les identifiants des personnes pouvant encore travailler
    persons = []
    (nb_hours_day, nb_hours_week) = nb_hours(firm)
    for person in model.database.Person.select().where(model.database.Person.firm_name == firm).order_by(fn.Random()) : #on les trie aléatoirement, car le choix de la personne a une importance
        if nb_hours_day[person.id - 1] < 7 or nb_hours_week[person.id - 1] < 35 :
            persons.append(person.id)
    return persons

def persons_available_post(firm,post): #renvoie les identifiants des personnes pouvant travailler sur ce poste
    persons = persons_available(firm)
    p_a_p = []
    for person in model.database.Person.select().join(model.database.Skill).where(model.database.Skill.operator == model.database.Person.id).where(model.database.Skill.post == post).where(model.database.Skill.firm_name == firm).select().order_by(fn.Random()):
        for i in persons :
            if person.id == i:
                p_a_p.append(i)
    return p_a_p

def planning (firm, nb_packages, nb_articles_package): #renvoie le planning final
    planning = plannificateur.tools.dict_creation(firm) #créé le planning vide
    nb_team = [2 for i in range(0,6)]
    nb_day_more_team = 0
    persons_working = []
    nb_interim_tot = 0
    time_left = 0 #temps restant à travailler
    (nb_hours_day, nb_hours_week) = nb_hours(firm)
    tot_time = 0
    tot_time2 = 0
    tot_time3 = 0

    Post_rd = model.database.Post.select().where(model.database.Post.firm_name == firm).order_by(fn.Random()) #range les postes aléatoirement car l'ordre à son importance

    for post in Post_rd: #remplissage du planning poste par poste
        time_needed = plannificateur.tools.time_needed_post(firm, nb_packages, nb_articles_package, post.name) #temps nécessaire pour expédier tous les colis
        tot_time += time_needed
        time_needed_day_team = [[0,0,0] for i in range (0,6)] #temps nécessaire pour chaque équipe et chaque jour pour un poste


        if time_needed/12 > 7 * 60 * model.data.nb_max_team: #si le temps nécessaire dépasse la capacité max de l'entrepôt, il faut ajouter des équipes de nuit
            nb_day_more_team = 6 - (time_needed//(7*60*model.data.nb_max_team))#nombre d'équipes de nuit en plus nécessaires
            for i in range(0,nb_day_more_team):
                nb_team[i] = 3
        for i in range(0, 6):
            for j in range(0, nb_team[i]):
                time_needed_day_team[i][j] = time_needed / (6 * 2 + nb_day_more_team) #répartition du temps nécessaire par équipe : temps nécessaire divisé par le nombre d'équipe

        for i in range(0,6): #on remplit le planning par jour
            for t in range (0,nb_team[i]): #on remplit le planning par équipe
                tot_time2 += time_needed_day_team[i][t]
                persons = persons_available_post(firm,post) #personnes pouvant effectuer la tâche

                for index in persons:
                    if time_needed_day_team[i][t] > 0 :#si la tâche n'est pas finie

                        if nb_hours_week[index-1] < 35 : #si l'opérateur peut encore travailler cette semaine
                            time_needed_day_team[i][t] -= (7 - nb_hours_day[index - 1]) * 60 #l'opérateur va faire la tâche sur son temps disponible du jour

                            nb_hours_week[index - 1] += 7 - nb_hours_day[index - 1]
                            nb_hours_day[index-1] += 7 - nb_hours_day[index - 1]
                            day = model.data.week[i]
                            team = model.data.team[t]
                            planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] += 1 #on ajoute un opérateur sur le planning

                            if index not in persons_working:  # on l'ajoute à la liste des travailleurs
                                persons_working.append(index)


                if time_needed_day_team[i][t] > 0: # s'il y a besoin d'intérimaires sur la journée pour finir le travail de cette équipe
                    nb_interim = (time_needed_day_team[i][t] // (7 * 60)) + 1 #nombre d'intérimaires nécessaires pour finir le travail
                    tot_time3 += time_needed_day_team[i][t]
                    day = model.data.week[i]
                    team = model.data.team[t]
                    planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] += nb_interim #on ajoute les intérimaires au planning
                    nb_interim_tot += nb_interim #nombre total d'intérimaires

    nb_person_working = len(persons_working) #nombre d'opérateurs sur le site
    nb_interims = nb_interim_tot//5 + 1 #on suppose qu'un intérimaire travaille 5 jours dans la semaine
    nb_person_working += nb_interims

    return (planning, nb_interims, nb_person_working)

