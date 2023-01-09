from peewee import*
from datetime import date

db = SqliteDatabase('people.db')


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
    day = DateField()

    class Meta:
        database = db



db.connect()
db.create_tables([Person, Post, Activity])

def create_table():
    picking = Post.create(name='picking', time=2, index=1)
    packaging = Post.create(name='packaging', time=1, index=2)
    palletization = Post.create(name='palletization', time=3, index=3)

    person1 = Person.create(ident=1, name='one', availability=True, nb_hour_week=0, nb_hour_day=0)
    person2 = Person.create(ident=2, name='two', availability=True, nb_hour_week=0, nb_hour_day=0)
    person3 = Person.create(ident=3, name='three', availability=True, nb_hour_week=0, nb_hour_day=0)
    person4 = Person.create(ident=4, name='four', availability=True, nb_hour_week=0, nb_hour_day=0)
    person5 = Person.create(ident=5, name='five', availability=True, nb_hour_week=0, nb_hour_day=0)

    skill1 = Skill(operator=1, post=picking)
    skill2 = Skill(operator=3, post=picking)
    skill3 = Skill(operator=5, post=picking)
    skill4 = Skill(operator=2, post=packaging)
    skill5 = Skill(operator=3, post=packaging)
    skill6 = Skill(operator=4, post=palletization)
    skill7 = Skill(operator=5, post=palletization)
    skill8 = Skill(operator=2, post=palletization)
    skill9 = Skill(operator=1, post=palletization)

    br = Activity.create(name='br', nb_packages=1, nb_article_packages=2.3,  day=date(2023,  7, 1))
    cd = Activity.create(name='cd', nb_packages=8, nb_article_packages=1.24, day=date(2023, 7, 1))

db.close()