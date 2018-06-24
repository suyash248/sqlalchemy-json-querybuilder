__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()
con_url = 'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'.format(
    username='root', password='', host='localhost', port=3306, database='test'
)
engine = create_engine(con_url, pool_recycle=3600)

# Set up the session
session_maker = sessionmaker(bind=engine, autoflush=True, autocommit=False, expire_on_commit=True)
session = scoped_session(session_maker)

