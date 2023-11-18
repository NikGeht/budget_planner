
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
    email = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

Base.metadata.create_all(engine)
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

def selectAll(id):
    all_exp = session.query(IncExp).filter(IncExp.owner == id).all()
    return all_exp

def selectAllFromCategory(id, category_name):
    all_exp = session.query(IncExp).filter(IncExp.owner == id, IncExp.category_name == category_name).all()
    return all_exp

def validUser(login, password):
    try:
        if session.query(User).filter(User.login == login, User.password == password).one():
            return True
        else:
            return False
    except sqlalchemy.exc.NoResultFound as e:
        return False

def createUser(login, password, email):
    new_user = User(login=login, password=password, email=email)
    session.add(new_user)
    print(f"Пользователь успешно добавлен с данными: {new_user.login}, {new_user.password}, {new_user.email}")
    session.commit()

def getIdUser(login):
    id = session.query(User.id).filter(User.login == login).one()
    return id[0]

def setPassword(login, password):
    session.query(User).filter(User.login == login).update({'password': password})
    session.commit()

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

def getBalance(login):
    id = getIdUser(login)
    res = session.query(IncExp).filter(IncExp.owner == id).all()
    summa = 0
    for i in res:
        summa += i.cost
    
    return summa
