class Posts:
    def __init__(self, list_posts, time_posts, activityfield):
        self.name = list_posts
        self.time = time_posts[activityfield.indice]


class Post:
    def __init__(self, Posts, index):
        self.name = Posts.name[index]
        self.time = Posts.time_posts[index]
        self.index = index
        if index > 2:
            self.previous_task = Posts.list_posts[index - 1]
        else:
            self.previous_task = "task 1"


class ActivityField:
    def __init__(self, nb_article_package, index, name):
        self.name = name
        self.nb_art = nb_article_package
        self.index = index


class WorkOrg:
    def __init__(self, period_week, period_month, period_year):
        self.day = period_week
        self.week = period_month
        self.month = period_year


class Operator:
    def __init__(self, break_time, nb_break, work_time, team, Posts):
        self.work = work_time
        self.break_ = break_time / nb_break
        self.team = team


class RepartitionKey:
    def __init__(self, day, WorkOrg):
        self.period = WorkOrg
        self.day = day