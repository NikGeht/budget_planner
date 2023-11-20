import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

engine = sqlalchemy.create_engine('postgresql://ngeht:pahan244@localhost:5432/budget_planner')

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


def select_all(user_id: int) -> list:
    """Get all notes where owner is user"""
    all_exp: list = session.query(IncExp).filter(user_id == IncExp.owner).all()
    return all_exp


def select_all_from_category(user_id: int, category_name: str) -> list:
    """Get all notes with user-defined category where owner is user"""
    all_exp: list = session.query(IncExp).filter(user_id == IncExp.owner, category_name == IncExp.category_name).all()
    return all_exp


def valid_user(login: str, password: str) -> bool:
    """Check user's conf data on exist in database"""
    try:
        if session.query(User).filter(login == User.login, password == User.password).one():
            return True
        else:
            return False
    except sqlalchemy.exc.NoResultFound as e:
        return False


def create_user(login: str, password: str, email: str) -> None:
    """Creating user in database"""
    new_user = User(login=login, password=password, email=email)
    session.add(new_user)
    print(f"Пользователь успешно добавлен с данными: {new_user.login}, {new_user.password}, {new_user.email}")
    session.commit()


def get_id_user(login: str) -> int:
    """Getter for user's id"""
    user_id = session.query(User.id).filter(login == User.login).one()
    return user_id[0]


def set_password(login: str, password: str) -> None:
    """Update password for users"""
    session.query(User).filter(login == User.login).update({'password': password})
    session.commit()


def create_note(category_name: str, cost: int, owner: int, data=None) -> None:
    """Create new methods with attributes"""
    new_note = IncExp(category_name=category_name, cost=cost, owner=owner)
    session.add(new_note)
    session.commit()


def delete_note(note_id: int) -> None:
    """Delete user note by id"""
    note = session.query(IncExp).filter(note_id == IncExp.id).one()
    session.delete(note)
    session.commit()


def change_note(note_id: int, category_name: str, cost: int, owner: int, data=None) -> None:
    """Change user note with attributes"""
    session.query(IncExp).filter(note_id == IncExp.id).update({"category_name": category_name,
                                                               "cost": cost,
                                                               "owner": owner})
    session.commit()


def get_balance(login: str) -> int:
    """Get user's balance (sum all expense and income)"""
    user_id: int = get_id_user(login)
    all_notes: list = session.query(IncExp).filter(user_id == IncExp.owner).all()
    balance: int = 0
    for note in all_notes:
        balance += note.cost

    return balance
