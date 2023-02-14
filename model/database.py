from peewee import*
from datetime import date
import csv

db = SqliteDatabase('firm.db')


class Person(Model):
    ident = IntegerField(unique=True, primary_key=True)
    name = CharField(unique=True)
    availability = BooleanField()
    nb_hour_week = IntegerField()
    nb_hour_day = IntegerField()
    firm_name = CharField()

    class Meta:
        database = db

    def not_available (self):
        bool = False
        if Person.nb_hour_week >= 35 or Person.nb_hour_day >= 7:
            bool = True
        return bool

class Post(Model):
    name = CharField(unique=True, primary_key=True)
    time = FloatField()
    index = IntegerField()
    action_on_article = IntegerField()
    firm_name = CharField()

    class Meta:
        database = db




class Skill(Model):
    operator = ForeignKeyField(Person, backref='persons')
    post = ForeignKeyField(Post, backref='posts')
    firm_name = CharField()

    class Meta:
        database = db


class User(Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id





db.create_tables([Person, Post, Skill,User])


def create_table_post(path, firm_name):
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Post.create(name=row['name'], time=row['time'], action_on_article=row['action_on_article'], index=row['index'], firm_name=firm_name)
    return()


def create_table_person(path, firm_name):
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Person.create(ident=row['ident'], name=row['name'], availability=True, nb_hour_week=0, nb_hour_day=0, firm_name=firm_name)
    return()


def create_table_skill(path, firm_name):
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            posts = row["post"].split(" ")
            for post in posts:
                Skill.create(operator=row['operator'], post=post, firm_name=firm_name)
    return()





