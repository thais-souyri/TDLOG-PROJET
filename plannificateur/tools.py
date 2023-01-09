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
    time_needed = nb_packages * database.Post.timepost_time[activity_field - 1][post.index]
    if post.index < 4:
        time_needed = time_needed * activity_field.nb_article_package
    return time_needed