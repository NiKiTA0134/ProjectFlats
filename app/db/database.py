from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from flask_login import UserMixin


engine = create_engine("sqlite:///app.db?check_same_thread=False", echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    nickname = Column("nickname", String)
    email = Column("email", String)
    password = Column("password", String)
    message = Column("message", String, nullable=True)
    answer = Column("answer", String, nullable=True)
    currency = Column("currency", String)

    def __init__(self, nickname, email, password, message, answer, currency):
        super().__init__()
        self.nickname = nickname
        self.email = email
        self.password = password
        self.message = message
        self.answer = answer
        self.currency = currency


class Flats(Base):
    __tablename__ = "flats"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(240))
    street = Column("street", String(240))
    floor = Column("floor", Integer)
    room = Column("room", Integer)
    size = Column("size", Integer)
    near = Column("near", String(240), nullable=True)
    price = Column("price", Integer)
    position = Column("position", Integer)
    currency = Column("currency", String)

    def __init__(self, name, street, floor, room, size, near, price, position, currency):
        super().__init__()
        self.name = name
        self.street = street
        self.floor = floor
        self.room = room
        self.size = size
        self.near = near
        self.price = price
        self.position = position
        self.currency = currency


class Hryvnia(Base, UserMixin):
    __tablename__ = "hryvnia"

    id = Column("id", Integer, primary_key=True)
    hryvnia_dollar = Column("hryvnia_dollar", Integer)
    hryvnia_euro = Column("hryvnia_euro", Integer)

    def __init__(self, hryvnia_dollar, hryvnia_euro):
        super().__init__()
        self.hryvnia_dollar = hryvnia_dollar
        self.hryvnia_euro = hryvnia_euro


class Dollar(Base, UserMixin):
    __tablename__ = "dollar"

    id = Column("id", Integer, primary_key=True)
    dollar_hryvnia = Column("hryvnia", Integer)
    dollar_euro = Column("euro", Integer)

    def __init__(self, dollar_hryvnia, dollar_euro):
        super().__init__()
        self.dollar_hryvnia = dollar_hryvnia
        self.dollar_euro = dollar_euro


class Euro(Base, UserMixin):
    __tablename__ = "euro"

    id = Column("id", Integer, primary_key=True)
    euro_dollar = Column("euro_dollar", Integer)
    euro_hryvnia = Column("euro_hryvnia", Integer)

    def __init__(self, euro_dollar, euro_hryvnia):
        super().__init__()
        self.euro_dollar = euro_dollar
        self.euro_hryvnia = euro_hryvnia


Base.metadata.create_all(engine)