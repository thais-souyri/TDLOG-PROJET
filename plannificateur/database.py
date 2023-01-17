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
    firm_name = CharField()

    class Meta:
        database = db


class Post(Model):
    name = CharField(unique=True)
    time = FloatField()
    index = IntegerField()
    firm_name = CharField

    class Meta:
        database = db


class Skill(Model):
    operator = ForeignKeyField(Person, backref='persons')
    post = ForeignKeyField(Post, backref='posts')
    firm_name = CharField()

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
db.create_tables([Person, Post, Skill, Activity])


def create_table_post(path, firm_name):
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Post.create(name=row['name'], time=row['time'], index=row['index'], firm_name=firm_name)
    return()


def create_table_person(path, firm_name):
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Person.create(ident=row['ident'], name=row['name'], availability=True, nb_hour_week=0, nb_hour_day=0, firm_name=firm_name)
    return()


def create_table_activity(path, firm_name):
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Activity.create(ident=row['ident'], name=row['name'], availability=True, nb_hour_week=0, nb_hour_day=0, firm_name=firm_name)
    return()


def create_table_skill(path, firm_name):
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            posts = row["post"].split(" ")
            for post in posts:
                Skill.create(operator=row['operator'], post=post, firm_name=firm_name)
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

