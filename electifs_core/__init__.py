import sqlalchemy
import sqlalchemy.orm

from .models import *
from .business import *
from .serialization import *
from .exceptions import *

engine = sqlalchemy.create_engine('mysql://root:poney@localhost/electifs?charset=utf8')
Session = sqlalchemy.orm.sessionmaker(bind=engine)
