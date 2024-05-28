from sqlalchemy import create_engine, Column, String, Integer, Select
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

#Basic setup
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

#Table format
class User(Base):                       
    __tablename__ = 'users'             
    id = Column(Integer, primary_key=True)
    username = Column(String)
    gmail = Column(String)
    password = Column(String)
    pin8 = Column(String)

Base.metadata.create_all(bind=engine)

def initialize_database() -> None:
    """
    Usage:
    -Emptying table. For testing purpose. Need to be removed.
    
    Return:
    -None
    """
    session.query(User).delete()            

def generate_users() -> None: 
    """
    Usage:
    -Generate users and insert to User

    Return:
    -None
    """
    failed: int = 0
    num_users: int = 0
    while True:
        try:
            num_users = int(input("Generate _ user(s).: "))
            break  
        except ValueError:
            print("Invalid input. Please enter an integer.", end='\r')

    for _ in tqdm(range(num_users)): 
        result: list[str, str, str, str] = random_name_pw(username_digits=12, password_digits=12)
        if result[1] == '':
            failed += 1
            continue
        session.add(User(username=result[0], gmail=result[1], password=result[2], pin8=result[3]))

    print(f'Successfully create {num_users-failed} Outlook mail account(s)....({num_users-failed}/{num_users})')
    session.commit()

def show_content() -> list:
    """
    Usage:
    -show content of database, i.e. User
    
    Return:
    -list = content of database. Line by line.
    """
    stmt = Select('*').select_from(User)
    result = session.execute(stmt).fetchall()
    
    return result



if __name__ == '__main__' :
    command: list = [show_content, generate_users, initialize_database]
    index: int = 0
    while True:
        index = int(input("""
Command:
0: Show content
1: Generate users
2: Initialize database
3: exit
input: """))
        if index not in [0, 1, 2]: break
        match index:
            case 0:
                [print(row) for row in command[index]()]
            case 1:
                command[index]()
            case 2:
                #Avoid mistakenly input 2
                if str(input('Delete all user information. (T/F): ')) in 'Tt': command[index]()
                
        print('-'*50)