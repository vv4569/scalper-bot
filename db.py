from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from pathlib import Path
from sqlalchemy import or_, and_
Path("database") \
    .mkdir(exist_ok=True)

# "database/main.db" specifies the database file
# change it if you wish
# turn echo = True to display the sql output
engine = create_engine("sqlite:///database/main.db", echo=False)

# initializes the database
