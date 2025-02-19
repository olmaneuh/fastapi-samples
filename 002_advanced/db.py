from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DB_URL = "sqlite:///./todo_app.db"

# create the database engine.
engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})

# create a session factory.
SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# define the base class for ORM models.
Base = declarative_base()
