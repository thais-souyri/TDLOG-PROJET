from peewee import*
from datetime import date
import csv

db = SqliteDatabase('firm.db')


class Person(Model):
    ident = IntegerField(unique=True, primary_key=True)
    name = CharField(unique=True)
    availability = BooleanField()
    nb_hour_week = IntegerField()   #nombre d'heures déja travaillées dans la semaine
    nb_hour_day = IntegerField()    #nombre d'heures déja travaillées dans le jour

    class Meta:
        database = db


class Post(Model):
    name = CharField(unique=True)
    time = FloatField()
    index = IntegerField()

    class Meta:
        database = db


class Skill(Model):
    operator = ForeignKeyField(Person, backref='persons')
    post = ForeignKeyField(Post, backref='posts')

    class Meta:
        database = db


class Activity(Model):
    name = CharField()
    nb_article_packages = FloatField()
    nb_packages = IntegerField()
    week_number = IntegerField()

    class Meta:
        database = db


db.connect()
db.create_tables([Person, Post, Activity])


# Import des données depuis le fichier CSV
path = "chemin/vers/fichier.csv"


def create_table_post(path):
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)
            #Post.create(name=row['name'], time=row['time'], index=row['index'])
    return()


create_table_post('posts.csv')


def create_table_person(path):
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            Person.create(ident=row['ident'], name=row['name'], availability=True, nb_hour_week=0, nb_hour_day=0)
    return()


def create_table_activity(path):
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            Activity.create(ident=row['ident'], name=row['name'], availability=True, nb_hour_week=0, nb_hour_day=0)
    return()


def create_table_skill(path):
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            Skill.create(operator=row['operator'], post=row['post'])
    return()



def create_table1():
    picking = Post.create(name='picking', time=2, index=1)
    packaging = Post.create(name='packaging', time=1, index=2)
    palletization = Post.create(name='palletization', time=3, index=3)

    Person.create(ident=1, name='one', availability=True, nb_hour_week=0, nb_hour_day=0)
    Person.create(ident=2, name='two', availability=True, nb_hour_week=0, nb_hour_day=0)
    Person.create(ident=3, name='three', availability=True, nb_hour_week=0, nb_hour_day=0)
    Person.create(ident=4, name='four', availability=True, nb_hour_week=0, nb_hour_day=0)
    Person.create(ident=5, name='five', availability=True, nb_hour_week=0, nb_hour_day=0)

    Skill(operator=1, post=picking)
    Skill(operator=3, post=picking)
    Skill(operator=5, post=picking)
    Skill(operator=2, post=packaging)
    Skill(operator=3, post=packaging)
    Skill(operator=4, post=palletization)
    Skill(operator=5, post=palletization)
    Skill(operator=2, post=palletization)
    Skill(operator=1, post=palletization)

    Activity.create(name='br', nb_packages=1, nb_article_packages=2.3,  day=date(2023,  7, 1))
    Activity.create(name='cd', nb_packages=8, nb_article_packages=1.24, day=date(2023, 7, 1))

db.close()