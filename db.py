from sqlalchemy import create_engine, Column, String, Integer, select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path
from userinfo_generator import random_name_pw
from tqdm import tqdm

Path("database").mkdir(exist_ok=True)

# "database/main.db" specifies the database file
# change it if you wish
# turn echo = True to display the sql output
engine = create_engine("sqlite:///database/main.db", echo=False)

# Basic setup
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Table format
class User(Base):                       
    __tablename__ = 'users'             
    id = Column(Integer, primary_key=True)
    username = Column(String)
    gmail = Column(String)
    password = Column(String)
    pin8 = Column(String)

Base.metadata.create_all(bind=engine)

def get_gmail():
    with SessionLocal() as session:
        users = session.query(User).all()
        return users

def initialize_database() -> None:
    with SessionLocal() as session:
        session.query(User).delete()
        session.commit()

def generate_users() -> None: 
    failed: int = 0
    num_users: int = 0
    while True:
        try:
            num_users = int(input("Generate _ user(s).: "))
            break  
        except ValueError:
            print("Invalid input. Please enter an integer.", end='\r')

    with SessionLocal() as session:
        for _ in tqdm(range(num_users)): 
            result: list[str, str, str, str] = random_name_pw(username_digits=12, password_digits=12)
            if result[1] == '':
                failed += 1
                continue
            session.add(User(username=result[0], gmail=result[1], password=result[2], pin8=result[3]))

        print(f'Successfully created {num_users-failed} Outlook mail account(s)....({num_users-failed}/{num_users})')
        session.commit()

def show_content() -> list:
    with SessionLocal() as session:
        stmt = select(User)
        result = session.execute(stmt).fetchall()
        return result

if __name__ == '__main__':
    command: list = [show_content, generate_users, initialize_database]
    index: int = 0
    while True:
        index = input("""
Command:
0: Show content
1: Generate users
2: Initialize database
3: exit
input: """)
        try:
            index = int(index)
        except:
            index = -1
        match index:
            case 0:
                [print(row) for row in command[index]()]
            case 1:
                command[index]()
            case 2:
                if str(input('Delete all user information. (T/F): ')) in 'Tt': command[index]()
            case 3:
                print('QUIT.')
                break
            case _:
                print('Invalid input.')
                
        print('-'*50)
