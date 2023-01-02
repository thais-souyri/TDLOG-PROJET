from peewee import*
db = SqliteDatabase('people.db')
from datetime import date


class Post(Model):
    name = CharField(unique=True)
    time = FloatField()
    index = IntegerField()

    class Meta:
        database = db


class Person(Model):
    name = CharField(unique=True)
    availability = BooleanField()
    nb_hour_week = IntegerField()   #nombre d'heures déja travaillées dans la semaine
    nb_hour_day = IntegerField()    #nombre d'heures déja travaillées dans le jour
    post = ForeignKeyField(Post, backref='posts')

    class Meta:
        database = db


class Activity(Model):
    name = CharField()
    nb_article_packages = FloatField()
    nb_packages = IntegerField()
    day = DateField()

    class Meta:
        database = db


db.connect()
db.create_tables([Person, Post, Activity])

picking = Post.create(name='picking', time=2, index=1)
emballage = Post.create(name='emballage', time=1, index=2)
palettisation= Post.create(name='palettisation', time=3, index=3)

person1 = Person.create(name='one', post=picking, availability=True, nb_hour_week=0, nb_hour_day=0)
person2 = Person.create(name='two', post=emballage, availability=True, nb_hour_week=0, nb_hour_day=0)
person3 = Person.create(name='three', post=palettisation, availability=True, nb_hour_week=0, nb_hour_day=0)
person4 = Person.create(name='four', post=picking, availability=True, nb_hour_week=0, nb_hour_day=0)
person5 = Person.create(name='five', post=palettisation, availability=True, nb_hour_week=0, nb_hour_day=0)

br = Activity.create(name='br', nb_packages=1, nb_article_packages=2.3,  day=date(2023,  7, 1))
cd = Activity.create(name='cd', nb_packages=8, nb_article_packages=1.24, day=date(2023, 7, 1))

persons = [person1, person2, person3, person4, person5]
nb_person = len(persons)
