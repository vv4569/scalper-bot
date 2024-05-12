from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path
from sqlalchemy import or_, and_
from userindo_generator import random_name_pw


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

#Struture of table.
class User(Base):        
    __tablename__ = 'users'            
    id = Column(Integer, primary_key=True)
    username = Column(String)           
    password = Column(String)

Base.metadata.create_all(bind=engine)

 #Emptying table. For testing purpose. Need to be removed
session.query(User).delete()           

for _ in range(int(input('Generate _ user(s). : '))): 
    result = random_name_pw(username_digits=12, password_digits=12, requirement='both')
    session.add(User(username=result[0], password=result[1]))
    
session.commit()

users = session.query(User).all()
for user in users:
    print(user.id, user.username, user.password)

session.close()
