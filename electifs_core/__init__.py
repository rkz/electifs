import sqlalchemy
import sqlalchemy.orm

from .models import *
from .business import *
from .serialization import *
from .exceptions import *

engine = None
Session = None

def connect (connection_string):
    global engine, Session
    engine = sqlalchemy.create_engine(connection_string)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)