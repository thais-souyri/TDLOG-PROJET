import model.data
import model.database
import plannificateur.tools

def planning(firm, nb_packages, nb_articles_package): #renvoie le planning final
    planning = plannificateur.tools.dict_creation(firm) #crée un planning vide
    nb_interim = []
    person_working = [] #répertorier les opérateurs qui vont travailler
    nb_operators = 0
    tot_time = 0

    for post in model.database.Post.select().where(model.database.Post.firm_name == firm): #on remplit le planning en parcourant les postes
        time_needed = plannificateur.tools.time_needed_post(firm, nb_packages, nb_articles_package, post) #temps nécessaire de travail pour le poste
        tot_time += time_needed
        nb_operators_night = 0 #opérateurs travaillant de nuit (3ème équipe)
        nb_operators_needed_post = time_needed//(35*60) + 1 #nombre d'opérateurs nécessaires sur le poste
        nb_operators += nb_operators_needed_post
        time_operators_post = 0


        persons_available = model.database.Person.select().where(model.database.Person.nb_hour_day < 7).where(model.database.Person.nb_hour_week < 35).where(model.database.Person.firm_name == firm) #personnes pouvant encore travailler dans la semaine
        for person in persons_available:
            persons_available_post = person.select().join(model.database.Skill).where(model.database.Skill.operator==person.id).where(model.database.Skill.post == post.name).where(model.database.Skill.firm_name == firm) #personnes disponibles pouvant effectuer ce poste
            for p in persons_available_post :
                if p.ident not in person_working:
                    time_operators_post += 35*60 #temps de travail des opérateurs disponibles pour le poste
                    person_working.append(p.ident)


        if time_needed > 2*model.data.nb_max_team*35*60: # si le temps nécessaire pour expédier tous les colis est supérieur au temps max de travail dans l'entreprise avec 2 équipes, alors il faut rajouter des équipes de nuit
            time_needed_night = time_needed - 2*model.data.nb_max_team * 35 * 60
            nb_operators_night = time_needed_night//(35*60) + 1 #nombre d'opérateurs nécessaire sur les équipes de nuit

        if time_needed > time_operators_post : #il y a besoin d'intérimaires
            time_interim_post = time_needed - time_operators_post
            nb_interim_post = time_interim_post//(35*60) + 1 #nombre d'intérimaires nécessaire pour accomplir le travail non effectué par les opérateurs en CDI
            nb_interim.append(nb_interim_post)
        else :
            nb_interim.append(0) #si le temps nécessaire pour le poste est inférieur au temps de travail disponible alors il n'y a pas besoin d'intérimaire


        for j in range(0, 6) : #on remplit le planning par jour pour les équipes de jour
            day = model.data.week[j]
            for k in range(0,2):
                team = model.data.team[k]
                planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] += (nb_operators_needed_post-nb_operators_night)//12 #on répartit les opérateurs en équipe de jours sur les 6 équipes de jour

        # on répartit le reste des opérateurs en équipe de jour sur les 6 équipes de jour
        if nb_operators_needed_post % 12 > 6 :
            for j in range(0, 6):
                day = model.data.week[j]
                for k in range(0, 2):
                    team = model.data.team[k]
                    planning["{}".format(day)]["{}".format(team)]["{}".format(post)] += 1
            for j in range(0, int((nb_operators_needed_post % 12) - 6)):
                day = model.data.week[j]
                for k in range(0, 2):
                    team = model.data.team[k]
                    planning["{}".format(day)]["{}".format(team)]["{}".format(post)] += 1
        else :
            for j in range(0, int(nb_operators_needed_post % 12)):
                day = model.data.week[j]
                for k in range(0, 2):
                    team = model.data.team[k]
                    planning["{}".format(day)]["{}".format(team)]["{}".format(post)] += 1


        for d in range(0, 6): #on répartit les opérateurs de nuit
            day = model.data.week[d]
            team = model.data.team[2]
            planning["{}".format(day)]["{}".format(team)]["{}".format(post)] += nb_operators_night // 6

        for j in range(0,int(nb_operators_night%6)):
            day = model.data.week[j]
            team = model.data.team[2]
            planning["{}".format(day)]["{}".format(team)]["{}".format(post)] += 1

    sum_interim = sum(nb_interim)
    return (planning, sum_interim, nb_operators)
