import model.data
import plannificateur.tools
import model.database
import random as rd

def nb_operators(firm, post): # renvoie un enter aléatoire entre 0 et le nombre de personnes disponibles pour ce poste
    persons_available = model.database.Person.select().where(model.database.Person.nb_hour_day < 7).where(model.database.Person.nb_hour_week < 35).where(model.database.Person.firm_name == firm)
    sum = 0
    for person in persons_available.select().join(model.database.Skill).where(model.database.Skill.operator == persons_available).where(model.database.Skill.post == post).where(model.database.Skill.firm_name == firm):
        sum +=1
    return rd.randint(0,sum)

def nb_teams_needed(firm, nb_packages, nb_articles_package): #renvoie le nombre d'équipe nécessaire par jour, la mise en place d'une troisième équipe est aléatoire
    nb_team = [2 for i in range(0, 6)]
    time_available = sum(nb_team) * 7 * 60 * model.data.nb_max_team #le temps disponible correspond au nombre d'équipe multiplié par le nombre maximum dans une équipe multiplié par le temps qu'une personne travaille par jour
    if plannificateur.tools.time_needed(firm, nb_packages, nb_articles_package) > 18 * 7 * 60 * model.data.nb_max_team :
        return "pas de solution" #si le temps nécessaire pour expédié touls les colis est supérieur au temps max de travail que peut fournir l'usine alors il n'y a pas de solution
    else :
        while plannificateur.tools.time_needed(firm, nb_packages, nb_articles_package) > time_available : #tant que le temps nécessaire est inférieur au temps disponible, on ajoute une troisème équipe dans une journée de manière aléatoire
            for i in range(0,6):
                nb_team[i] = rd.randint(2,3)
                time_available = sum(nb_team) * 7 * 60 * model.data.nb_max_team
    return nb_team

def planning(firm, nb_packages, nb_articles_package): #renvoie le planning final
    planning = plannificateur.tools.dict_creation(firm) #crée le planning vide
    nb_teams = nb_teams_needed(firm, nb_packages, nb_articles_package)
    tot_interim = 0
    if nb_teams == "pas de solution":
        return nb_teams
    for post in model.database.Post.select().where(model.database.Post.firm_name == firm): #on parcourt tous les postes, et on s'assure qu'on peut expédier tous les colis
        time_needed = plannificateur.tools.time_needed_post(firm, nb_packages, nb_articles_package, post.name) #temps nécessaire sur le poste pour expédier tous les colis
        for j in range(0, 6): #on parcourt tous les jours de la semaine (l'entreprise ne travail pas le dimanche)
            day = model.data.week[j] #jour de la semaine
            team = model.data.team[rd.randint(0,nb_teams[j]-1)] #on choisit aléatoirement l'équipe du jour
            nb = nb_operators(firm, post) #nombre d'opérateurs qui vont travailer sur ce poste ce jour
            time_needed -= nb * 7 * 60 #on retire au temps nécessaire le temps que vont travailler les opérateurs choisis aléatoirement
            planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] += nb_operators(firm, post) #on ajoute au planning le nombre d'opérateurs choisis
        while time_needed > 0:
            if time_needed > 0: #si le temps travaillé par les opérateurs en CDI n'est pas suffisant, on ajoute au planning des intérimaires
                day_index = rd.randint(0,5) #on choisit un jour au hasard
                day = model.data.week[day_index]
                team = model.data.team[rd.randint(0,nb_teams[day_index]-1)]
                nb_interim = rd.randint(0, (time_needed//(7*60))+1) #on choisit aléatoirement le nombre d'intérim entre 0 et le nombre max d'intérimaire nécessaire pour ce poste
                if nb_interim + planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] < model.data.nb_max_team: #on vérifie que l'ajout des intérimaires à l'équipe ne dépasse pas la capacité max d'une équipe
                    planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] += nb_interim #on ajoute le nombre d'intérimaire à l'équipe
                    time_needed -= nb_interim*7*60
                    tot_interim += nb_interim
    tot_interim = tot_interim//5 + 1 #on suppose qu'un même intérimaire va travailler 5 jours dans la semaine
    nb_person = plannificateur.tools.total_operators(firm, planning)//5 + 1 #on suppose qu'un opérateur va travailler 5 jours dans la semaine
    return (planning, tot_interim, nb_person)

