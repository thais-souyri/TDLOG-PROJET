import data
import tools
import database
import random as rd

def nb_operators(firm, post):
    persons_available = plannificateur.database.Person.select().where(plannificateur.database.Person.nb_hour_day < 7).where(plannificateur.database.Person.nb_hour_week < 35).where(plannificateur.database.Person.firm_name == firm)
    sum = 0
    for person in persons_available.select().join(plannificateur.database.Skill).where(plannificateur.database.Skill.operator == persons_available).where(plannificateur.database.Skill.post == post).where(plannificateur.database.Skill.firm_name == firm):
        sum +=1
    return rd.randint(0,sum)

def nb_teams_needed(firm, nb_packages, nb_articles_package):
    nb_team = [2 for i in range(0, 6)]
    time_available = sum(nb_team) * 7 * 60 * data.nb_max_team
    if plannificateur.tools.time_needed(firm, nb_packages, nb_articles_package) > 18 * 7 * 60 * data.nb_max_team :
        return "pas de solution"
    else :
        while plannificateur.tools.time_needed(firm, nb_packages, nb_articles_package) > time_available :
            for i in range(0,6):
                nb_team[i] = rd.randint(2,3)
                time_available = sum(nb_team) * 7 * 60 * data.nb_max_team
    return nb_team

def planning(firm, nb_packages, nb_articles_package):
    planning = plannificateur.tools.dict_creation(firm)
    nb_teams = nb_teams_needed(firm, nb_packages, nb_articles_package)
    tot_interim = 0
    if nb_teams == "pas de solution":
        return nb_teams
    for post in plannificateur.database.Post.select().where(database.Post.firm_name == firm):
        time_needed = plannificateur.tools.time_needed_post(firm, nb_packages, nb_articles_package, post.name)
        while time_needed > 0 :
            for j in range(0, 6):
                day = data.week[j]
                team = data.team[rd.randint(0,nb_teams[j]-1)]
                nb = nb_operators(firm, post)
                time_needed -= nb * 7 * 60
                planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] += nb_operators(firm, post)
                if time_needed > 0:
                    day_index = rd.randint(0,5)
                    day = plannificateur.data.week[day_index]
                    team = plannificateur.data.team[rd.randint(0,nb_teams[day_index]-1)]
                    nb_interim = rd.randint(0, (time_needed//(7*60))+1)
                    if nb_interim + planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] < plannificateur.data.nb_max_team:
                        planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] += nb_interim
                        time_needed -= nb_interim*7*60
                        tot_interim += nb_interim
    tot_interim = tot_interim//5 + 1
    nb_person = plannificateur.tools.total_operators(firm, planning)//5 + 1
    return (planning, tot_interim, nb_person)

