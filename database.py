from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('mysql+pymysql://b64e82961b3ee9:1122290a'
                       '@us-cdbr-iron-east-02.cleardb.net/heroku_1c9ac2620cf55df')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Venue(Base):
    __tablename__ = 'venues'

    id = Column(INTEGER(11), primary_key=True)
    venue = Column(String(255), nullable=False)
    capacity = Column(String(255), nullable=False, server_default=text("'0'"))
    location = Column(String(255))
    state = Column(String(15))
    add_method = Column(String(50))