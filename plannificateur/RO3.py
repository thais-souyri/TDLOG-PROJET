import data
import database
import tools
import random as rd



def main (activity_field, nb_packages):
    planning = tools.dict_creation()
    for post in database.Post.select() :
        time_needed = tools.time_needed_post(nb_packages, activity_field, post.name)
        while time_needed > 0 :
            person = rd.random(database.Person)
            qualified = false
            for skill in database.Skill.select():
                if skill.operator == person.index and skill.post = post.index :
                    qualified = true
            if qualified and person.index
    return None





