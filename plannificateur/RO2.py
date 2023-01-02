import data
import database

def time_needed_post(nb_packages, activity_field,post):
    nb_articles = nb_packages * nb_articles_package[activity_field-1]
    time_needed = nb_articles * post_time[activity_field-1][post.index]
    return time_needed


def main(nb_packages, month, activity_field):
    planning = {}
    for j in range(0, 7):
        day = data.week[j]
        planning["{}".format(day)] = {}
        for k in range(0, 3):
            team = data.team[k]
            planning["{}".format(day)]["{}".format(team)] = {}
            for i in range(0, data.nb_posts):
                post = data.posts[i]
                planning["{}".format(day)]["{}".format(team)]["{}".format(post)] = 0

    for post in range (0, data.nb_post):
        time_needed = time_needed_post(nb_packages, activity_field,data.posts[post])
        nb_operators_needed_post = 0
        while time_needed > 0 :
            time_needed = time_needed - data.work_time
            nb_operators_needed_post += 1

        nb_operators_post = 0
        for i in range(0,database.nb_persons):
            if database.persons[i].post == data.posts[post]:
                nb_operators_post += 1

        if nb_operators_needed_post > nb_operators_post :
            nb_interim_post = nb_operators_needed_posts - nb_operators_posts

        if nb_operators_needed_post > 3*6*50:
            return ("Il y a trop d'articles")

        if nb_operators_needed_post > 2*6*50:
            nb_operators_night = nb_operators_needed - 2*6*50
            nb_operators_needed = 2*6*50

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
            team = data.team(2)
            planning["{}".format(day)]["{}".format(team)]["{}".format(post)] = nb_operators_night // 6

        for j in range(nb_operators_night%6):
            day = data.week[j]
            team = data.team[2]
            planning["{}".format(day)]["{}".format(team)]["{}".format(post)] += 1


    print(planning)
    return (planning, nb_interim)


(nb_pakages, month, activity_field) = (0,"janvier",0)

(planning,nb_interim)= main(nb_pakages, month, activity_field)






