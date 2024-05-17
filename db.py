from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path
from sqlalchemy import or_, and_
from userindo_generator import random_name_pw
from tqdm import tqdm


Path("database") \
    .mkdir(exist_ok=True)

# "database/main.db" specifies the database file
# change it if you wish
# turn echo = True to display the sql output
engine = create_engine("sqlite:///database/main.db", echo=False)

# initializes the database

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):                       
    __tablename__ = 'users'             
    id = Column(Integer, primary_key=True)
    username = Column(String)
    gmail = Column(String)
    password = Column(String)
    pin8 = Column(String)

Base.metadata.create_all(bind=engine)
session.query(User).delete()            #Emptying table. For testing purpose. Need to be removed

num_users: int = 0
while True:
    try:
        num_users = int(input("Generate _ user(s).: "))
        break  
    except ValueError:
        print("Invalid input. Please enter an integer.")
for _ in tqdm(range(num_users)): 
    result: list[str, str, str, str] = random_name_pw(username_digits=12, password_digits=12)
    session.add(User(username=result[0], gmail=result[1], password=result[2], pin8=result[3]))
session.commit()

users = session.query(User).all()
for user in users:
    print(user.id, user.username, user.gmail, user.password, user.pin8)

session.close()
