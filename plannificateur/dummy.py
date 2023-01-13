import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///tutorial.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = User("a","a")
session.add(user)

user = User("b","b")
session.add(user)

user = User("c","c")
session.add(user)

# commit the record the database
session.commit()

session.commit()