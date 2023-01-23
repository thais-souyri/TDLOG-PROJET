import plannificateur.data
import plannificateur.database
import plannificateur.tools

def planning(firm, nb_packages, nb_articles_package):
    planning = plannificateur.tools.dict_creation(firm)
    nb_interim = []

    for post in plannificateur.database.Post.select().where(plannificateur.database.Post.firm_name == firm):
        time_needed = plannificateur.tools.time_needed_post(firm, nb_packages, nb_articles_package, post)
        nb_interim_post = 0
        nb_operators_night = 0
        time_operators_post = 0
        persons_available = plannificateur.database.Person.select().where(plannificateur.database.Person.nb_hour_day < 7).where(plannificateur.database.Person.nb_hour_week < 35).where(plannificateur.database.Person.firm_name == firm)
        for person in persons_available:
            persons_available_post = person.select().join(plannificateur.database.Skill).where(plannificateur.database.Skill.operator==person.ident).where(plannificateur.database.Skill.post == post.name).where(plannificateur.database.Skill.firm_name == firm)
            for p in persons_available_post:
                time_operators_post += 35


        if time_needed > time_operators_post :
            time_interim_post = time_needed - time_operators_post
            nb_interim_post = time_interim_post//(7*60) + 1
            nb_interim.append(nb_interim_post)
        else :
            nb_interim.append(0)

        if time_operators_post > 2*6*plannificateur.data.nb_max_team*7*60: # 2 équipes sur 6 jours travaillant 7h par jour
            time_needed_night = time_operators_post - 2*6 * plannificateur.data.nb_max_team * 7*60
            nb_operators_night = time_needed_night//(7*60) + 1
            time_operators_post = 2*6 * plannificateur.data.nb_max_team*7*60

        nb_operators_needed_post = time_operators_post//(7*60) + nb_interim_post + 1

        for j in range(0, 6) :
            day = plannificateur.data.week[j]
            for k in range(0,2):
                team = plannificateur.data.team[k]
                planning["{}".format(day)]["{}".format(team)]["{}".format(post.name)] += nb_operators_needed_post//12
        if nb_operators_needed_post % 12 > 6 :
            for j in range(0, 6):
                day = plannificateur.data.week[j]
                for k in range(0, 2):
                    team = plannificateur.data.team[k]
                    planning["{}".format(day)]["{}".format(team)]["{}".format(post)] += 1
            for j in range(0, int(nb_operators_needed_post % 12 - 6)):
                day = plannificateur.data.week[j]
                for k in range(0, 2):
                    team = plannificateur.data.team[k]
                    planning["{}".format(day)]["{}".format(team)]["{}".format(post)] += 1
        else :
            for j in range(0, int(nb_operators_needed_post % 12)):
                day = plannificateur.data.week[j]
                for k in range(0, 2):
                    team = plannificateur.data.team[k]
                    planning["{}".format(day)]["{}".format(team)]["{}".format(post)] += 1


        for d in range(0, 6):
            day = plannificateur.data.week[d]
            team = plannificateur.data.team[2]
            planning["{}".format(day)]["{}".format(team)]["{}".format(post)] += nb_operators_night // 6

        for j in range(0,int(nb_operators_night%6)):
            day = plannificateur.data.week[j]
            team = plannificateur.data.team[2]
            planning["{}".format(day)]["{}".format(team)]["{}".format(post)] += 1

    sum_interim = sum(nb_interim)//5 + 1
    nb_operators = plannificateur.tools.total_operators(firm, planning)//5 + 1
    return (planning, sum_interim, nb_operators)

