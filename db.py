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

#Basic setup
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
failed: int = 0
test_mode: bool = bool(int(input('Test mode (0/1): ')))
phone_no = str(input('Phone number: '))

#Table format
class User(Base):                       
    __tablename__ = 'users'             
    id = Column(Integer, primary_key=True)
    username = Column(String)
    gmail = Column(String)
    password = Column(String)
    pin8 = Column(String)

Base.metadata.create_all(bind=engine)

#Emptying table. For testing purpose. Need to be removed.
session.query(User).delete()            

#Generate users.
num_users: int = 0
while True:
    try:
        num_users = int(input("Generate _ user(s).: "))
        break  
    except ValueError:
        print("Invalid input. Please enter an integer.")

for _ in tqdm(range(num_users)): 
    result: list[str, str, str, str] = random_name_pw(username_digits=12, password_digits=12, phone_no=phone_no)
    if result[1] == '':
        failed += 1
        print(f'Name: {result[0]}, email registration failed.')
        continue
    session.add(User(username=result[0], gmail=result[1], password=result[2], pin8=result[3]))

print(f'Successfully create {num_users-failed} yahoo mail account(s)....({num_users-failed}/{num_users})')
session.commit()

#Show output.
if test_mode:           
    users = session.query(User).all()
    for user in users:
        print(user.id, user.username, user.gmail, user.password, user.pin8)

session.close()
