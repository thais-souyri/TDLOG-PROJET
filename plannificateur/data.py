from peewee import*
db = SqliteDatabase('people.db')
from datetime import date


class Post(Model):
    name = CharField(unique=True)
    time = FloatField()
    index =IntegerField()
    class Meta:
        database = db

class Person(Model):
    name = CharField(unique=True)
    post = ForeignKeyField(Post, backref='posts')
    class Meta:
        database = db

class Activity(Model) :
    name= CharField()
    nb_packages= IntegerField()
    day=DateField()
    class Meta:
        database = db

db.connect()
db.create_tables([Person, Post, Activity])

picking = Post.create(name='picking',time=2,index=1)
emballage = Post.create(name='emballage',time=1, index=2)
palettisation= Post.create(name='palettisation',time=3, index=3)

person1 = Person.create(name= 'one',post=picking)
person2 = Person.create(name='two',post=emballage)
person3 = Person.create(name='three', post= palettisation)
person4 = Person.create(name='four',post=picking)
person5 = Person.create(name='five', post=palettisation)

br = Activity.create(name='br', nb_packages= 1, day=date(2023,7,1))
cd = Activity.create(name='cd', nb_packages= 8, day=date(2023,7,1))
week = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
months = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre",
          "décembre"]

nb_articles_package = [1.24, 2.3]
work_time = 7 * 60 * 60
break_time = 30 * 60
activity_field_indexes = [1, 2]
posts = ["pickeur rack", "pickeur etagere", "operateur skypod", "agent logistique ventilation",
        "agent logistique conduceteur de ligne emballage", "agent logistique palettisation"]
nb_posts = len(posts)
team = ["matin", "après-midi", "nuit"]
post_time_d2 = [25.7, 48, 10.3, 18, 16, 10.6]
post_time_d1 = [46.8, 72, 14.4, 26.7, 37.9, 22.5]
post_time = [post_time_d1, post_time_d2]
