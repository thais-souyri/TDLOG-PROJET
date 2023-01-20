import data
import database
import tools

def planning(firm, nb_packages, nb_articles_package):
    planning = tools.dict_creation(firm)
    nb_post = tools.nb_post(firm)
    nb_interim = []

    for post in database.Post.select().where(database.Post.firm_name == firm):
        time_needed = tools.time_needed_post(firm, nb_packages, nb_articles_package, post)
        nb_operators_needed_post = 0
        while time_needed > 0 :
            time_needed = time_needed - 7
            nb_operators_needed_post += 1

        nb_operators_post = 0
        persons_available = database.Person.select().where(database.Person.nb_hour_day < 7).where(database.Person.nb_hour_week < 35).where(database.Person.firm_name == firm)
        for person in persons_available:
            persons_available_post = person.select().join(database.Skill).where(database.Skill.operator==person.ident).where(database.Skill.post == post.name).where(database.Skill.firm_name == firm)
            for p in persons_available_post:
                nb_operators_post += 1

        if nb_operators_needed_post > nb_operators_post * 5 :
            nb_interim_post = nb_operators_needed_post - nb_operators_post * 5
            nb_interim.append(nb_interim_post)
        else :
            nb_interim.append(0)

        if nb_operators_needed_post > 2*6*data.nb_max_team:
            nb_operators_night = nb_operators_needed_post - 2*6 * data.nb_max_team
            nb_operators_needed = 2*6* data.nb_max_team

        for j in range(0, 6):
            day = data.week[j]
            for k in range(0,2):
                team = data.team[k]
                planning["{}".format(day)]["{}".format(team)]["{}".format(post)] = nb_operators_needed//12
        for j in range(nb_operators_needed%12):
            day = data.week[j]
            for k in range(0, 2):
                team = data.team[k]
                planning["{}".format(day)]["{}".format(team)]["{}".format(post)] += 1

        for j in range(0, 6):
            day = data.week[j]
            team = data.team[2]
            planning["{}".format(day)]["{}".format(team)]["{}".format(post)] = nb_operators_night // 6

        for j in range(nb_operators_night%6):
            day = data.week[j]
            team = data.team[2]
            planning["{}".format(day)]["{}".format(team)]["{}".format(post)] += 1

    nb_operators = tools.total_operators()
    print(planning)
    return (planning, nb_interim, nb_operators)


planning('a',12,1.8)
