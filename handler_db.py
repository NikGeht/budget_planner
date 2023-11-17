
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

engine  = sqlalchemy.create_engine('postgresql://ngeht:pahan244@localhost:5432/budget_planner')

Base = declarative_base()

class IncExp(Base):
    __tablename__ = 'inc_exp'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    category_name = sqlalchemy.Column(sqlalchemy.String(length=100))
    data = sqlalchemy.Column(sqlalchemy.Date, nullable=True)
    cost = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), default=func.now())
    owner = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"), nullable=False)

class User(Base):
    __tablename__ = 'user'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.Text)
    money = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    email = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

Base.metadata.create_all(engine)
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

def selectAll():
    all_exp = session.query(IncExp).all()
    print(all_exp)

selectAll()

def createUser(login, password, email):
    new_user = User(login=login, password=password, email=email)
    session.add(new_user)
    session.commit()

def setMoney(money, login):
    session.query(User).filter(User.login == login).update({'money': money})
    session.commit()

def getMoney(login):
    money = session.query(User.money).filter(User.login == login).first()
    return money

def setPassword(login, password):
    session.query(User).filter(User.login == login).update({'password': password})

def createNote(category_name, cost, owner, data=None):
    Note = IncExp(category_name=category_name, cost=cost, owner=owner)
    session.add(Note)
    session.commit()

def deleteNote(id):
    Note = session.query(IncExp).filter(IncExp.id == id).one()
    session.delete(Note)
    session.commit()

def changeNote(id, category_name, cost, owner, data=None):
    session.query(IncExp).filter(IncExp.id == id).update({"category_name": category_name, "cost": cost, "owner": owner})
    session.commit()