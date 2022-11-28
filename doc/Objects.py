class Posts:
    def __init__(self, list_posts, time_posts,activityfield):
        self.noms = list_posts
        self.temps = time_posts[activityfield.indice]

class Post :
    def __init__(self,Posts,indice)
        self.nom = Posts.noms[indice]
        self.temps = Posts.temps_postes[indice]
        self.indice = indice
        if indice > : 2
            self.previous_task = posts[indice-1]
        else :
            self.previous_task = "task 1"

class ActivityField :
    def __init__(self,nb_article_colis,indice,name):
        self.name = name
        self.nb_art = nb_article_colis
        self.indice = indice

class WorkOrg :
    def __init__(self,period_week, period_month, period_year):
        self.day = period_week
        self.week = period_month
        self.month = period_year

class Operator :
    def __init__(self,break_time, nb_break, work_time,team):
        self.work = work_time
        self.break_ = break_time / nb_break
        self.team = team

class cle_repartition:
    def __init__(self,jour,orga_travail):
        self.periode = orga_travail
        self.jour = jour

semaine = ["lundi", "mardi", "mercredi", "jeudi", "vendredi","samedi", "dimanche"]

nb_articles_colis = [1.24,2.3]
temps_travail = 7*60*60
temps_pause = 30*60
indice_domaine_activité = [1,2]
poste = ["pickeur rack", "pickeur etagere", "operateur skypod", "agent logistique ventilation", "agent logistique conduceteur de ligne emballage", "agent logistique palettisation"]
equipe = [matin, apres_midi, soir]
temps_poste_d2 = [25.7,48,10.3,18,16,10.6]
temps_poste_d1 = [46.8,72,14.4,26.7,37.9,22.5]
temps_poste = [temps_potse_d1,temps_poste_d2]
