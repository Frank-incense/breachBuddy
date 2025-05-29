from sqlalchemy import (create_engine, Table, ForeignKey, select, Column, Integer, String, DateTime, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from pawned import checkPassword

engine = create_engine('sqlite:///pawned.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):

    all = {}

    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    username = Column(String(), nullable=False)
    createdAt = Column(DateTime(), server_default=func.now())

    emails = relationship("EmailCheck", backref=backref("user"))
    passwords = relationship("PasswordCheck", backref=backref("user"))
    
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, name):
        if isinstance(name, str) and 0 < len(name) < 15:
            user = session.query(type(self)).filter_by(username=self.name)
            user.username = name
            self._username = name
            session.commit()
            
        else:
            return "Error: name not string"
        

    def __repr__(self):
        return f"<User: {self.id}, username: {self.username}>"
    
    @classmethod
    def create_user(cls, name):
        user = cls(username=name)
        session.add(user)
        session.commit()

        cls.all[user.id] = user
    
    @classmethod
    def find_by_id(cls, id):
        user = session.query(cls).filter_by(id=int(id))
        return user
    
    @classmethod
    def find_by_name(cls, name):
        user = session.query(cls).filter_by(username=name)
        return user
    
    @classmethod
    def get_all(cls):
        users = session.query(User).fetchall()
        return [user for user in users] if users else None
    
    @classmethod
    def most_password_counts():
        statement = select(User.username).select_
    
    def get_password_checks(self):
        statement = select(type(self).username, PasswordCheck.hash, 
            PasswordCheck.checkedAt, PasswordCheck.hash_count).select_from(User).join(
                PasswordCheck, PasswordCheck.user_id == User.id
            )
        rows = session.execute(statement)
        return [row for row in rows] if rows else None
    
    def password_check(self):
        checkPassword(self.id)


class PasswordCheck(Base):
    __tablename__ = "password_checks"
    id = Column(Integer(), primary_key=True)
    hash = Column(String(), nullable=False)
    checkedAt = Column(DateTime(), server_default=func.now())
    hash_count = Column(Integer(), nullable=False)

    user_id = Column(Integer(), ForeignKey('users.id'))



mail_breachs = Table(
    'mail_breachs',
    Base.metadata,
    Column('mail_id', ForeignKey("email_checks.id"), primary_key=True),
    Column('breach_id', ForeignKey("breachs.id"), primary_key=True),
    extend_existing=True,
)

# For further improvements of the app To check email breachs
class EmailCheck(Base):
    __tablename__ = "email_checks"
    id = Column(Integer(), primary_key=True)
    email_checked = Column(String(), nullable=False)
    date_checked = Column(DateTime(), server_default=func.now())
    no_of_breaches = Column(Integer(), nullable=False)

    user_id = Column(Integer(), ForeignKey('users.id'))
    breaches = relationship("Breach", secondary=mail_breachs, back_populates="breachs")

class Breach(Base):
    __tablename__ = "breachs"
    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    domain = Column(String(), nullable=False)
    breachDate = Column(String(), nullable=False)
    exposedData = Column(String(), nullable=False)

    emailChecks = relationship("EmailCheck", secondary=mail_breachs, back_populates="email_checks") 