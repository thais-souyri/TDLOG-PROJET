import json
from gurobipy import Model, GRB, quicksum
import numpy as np
import tools
import database


#création de classes pour simplifier l'accès aux données


class Parameters:
    def __init__(self, nb_operators_qualified, posts, operators_qualified):
        self.nb_operators_qualified = nb_operators_qualified
        self.posts = posts
        self.operators_qualified = operators_qualified  #liste des opérateurs pouvant réaliser le poste

    def nb_posts(self):
        return len(self.posts)

    def nb_operators_qualified(self):
        return len(self.operators_qualified)

    def reponse(self):
        print('Instance avec {} opérateurs qualifiés'.format(self.nb_operators))

        print("Post:")
        for t in range(self.nb_posts()):
            self.posts[t].show()

        print("Operators qualifiés: \n")
        for i in range(self.nb_operators_qualified()):
            self.operators_qualified[i].show()


#définition des paramètres
def parameter(name):
    m = Model()
    parameters = name["parameters"]
    nb_posts = parameters["size"]["nb_tasks"]
    nb_operators_qualified = parameters["size"]["nb_operators_qualified"]
    nb_interim = parameters["size"]["nb_interim"]
    interim = ["interim"]
    post_name = name["post"]
    posts = [Post(post["post"], post["processing_time"], article["article"],)
             for post in post_name]
    operators = np.empty(nb_posts, dtype=object)
    for posts in post_name:
        i = posts["posts"]
        operators[i] = operator_qualified
    param = Parameters(nb_operators, posts, operators)
    return parameters, nb_posts, nb_operators_qualified, nb_interim, interim, posts,  operators,\
        param


def planning(pb):
    m = Model();
    parameters, nb_posts, nb_operators_qualified, interim, posts, operators, \
        param = parameter(pb)

    #Création des variables; bornes; types)
    c_post = {} #début de prise de poste
    for j in range(1, nb_posts+1):
        name = "c_post" + str(j)
        c_post[j] = m.addVar(vtype=GRB.INTEGER, name=name, lb=0)
    b_post = {} #fin de prise de poste
    for j in range(1, nb_posts + 1):
        name = "b_post" + str(j)
        b_post[j] = m.addVar(vtype=GRB.INTEGER, name=name, lb=0)

    o = {}
    for i in range(1, nb_posts + 1):
        for k in range(1, nb_operators_qualified + 1):
            name = "o" + str(i) + "," + str(k)
            o[i, k] = m.addVar(vtype=GRB.INTEGER, name=name, lb=0, ub=1)


    persons = []
    for i in range(1, nb_posts+1):
        for k in range(1, nb_operators_qualified + 1) :
            persons.append(o[i,k])

    count_persons = []
    for p in persons:
        if p not in count_persons :
            count_persons.append(p)

    nb_person = len(count_persons) + len(interim)

    time_operators = [7 for o in range(nb_operators_qualified)]
    for i in range(1, nb_posts +1):
        for k in range(1,nb_operators_qualified+1):
            if k in o[i,k]:
                time_operators -= b_post[i] - c_post[i]


    time_posts = []
    for i in posts:
        if i.on_article == True :
            time_posts.append(i.process_time * nb_article * nb_packages)
        else:
            time_posts.append(i.process_time)

    #Création de la fonction objectif
    m.setObjective(quicksum(nb_person, GRB.MINIMIZE))

    for i in range(1, nb_posts + 1):
        m.addConstr(2 > quicksum(o[i, l] for l in operators[i - 1]))
        m.addConstr(2 > quicksum(o[i, l] for l in range(1, nb_operators_qualified + 1)))


    for i in range(1, nb_posts + 1):
        for k in range(1, nb_operators_qualified + 1):
            m.addConstr(b_post[i] - c_post[i] >= time_posts[i])
            m.addConstr(time_operators[k] > 0)



    m.optimize()
    m.printAttr('X')


    B = [0 for i in range(0,nb_posts)]
    O = [0 for i in range(0,nb_posts)]

    for t in b_post.values():
        lettre = t.VarName
        B[int(lettre[6:]) - 1] = t.X
    for t in o.values():
        if t.X == 1:
            lettre = t.VarName
            O[int(lettre[1:lettre.find(',')]) - 1] = int(lettre[lettre.find(',') + 1:])

    solution = []

    for i in range(nb_posts):
        post_i = {}
        post_i["post"] = i + 1
        post_i["start"] = int(B[i])
        post_i["operator"] = int(O[i])
        resultats.append(post_i)
    print(solution)


    return (planning, nb_interim, nb_person)

nb_packages = 12
nb_articles_package = 5

pb = (database.Person, database.Person, database.Skill, nb_packages, nb_articles_package)

planning(pb)