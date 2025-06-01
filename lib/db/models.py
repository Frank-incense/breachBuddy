
from sqlalchemy import (create_engine, Table, ForeignKey, select, Column, Integer, String, DateTime, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from .pawned import checkPassword, checkEmail

engine = create_engine('sqlite:///lib/db/pawned.db')
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
    
    # @property
    # def username(self):
    #     return self.username
    
    # @username.setter
    # def username(self, name):
    #     if isinstance(name, str) and 0 < len(name) < 15:
    #         user = session.query(type(self)).filter_by(username=name)
    #         user.update({User.username: name})
    #         session.commit()
            
    #     else:
    #         return "Error: name not string"
        

    def __repr__(self):
        return f"<User: {self.id}, username: {self.username}>"
    
    @classmethod
    def create_user(cls, name):
        user = cls(username=name)
        session.add(user)
        session.commit()

        cls.all[user.id] = user
        return user
    
    @classmethod
    def delete_user(cls, id):
        session.query(cls).filter_by(id=id).delete()
        session.commit()

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
        users = session.query(User)
        return  users if users else None
    
    
    def get_password_checks(self, cls):
        passwords = session.query(cls).filter_by(user_id=self.id).all()
        
        return [row for row in passwords] if passwords else None
    
    def get_email_checks(self, cls):
        emails = session.query(cls).filter_by(user_id=self.id).all()
        
        return [row for row in emails] if emails else None
    
    def password_check(self):
        checkPassword(self)

    def email_check(self):
        checkEmail(self)
    
    def update_user(self):
        name = input("Kindly input a new name: ")
        user = session.query(type(self)).filter_by(id=self.id)
        user.update(
            {
                User.username: name
            }
        )
        session.commit()

class PasswordCheck(Base):

    all = {}

    __tablename__ = "password_checks"
    id = Column(Integer(), primary_key=True)
    hash = Column(String(), nullable=False)
    checkedAt = Column(DateTime(), server_default=func.now())
    hash_count = Column(Integer(), nullable=False)

    user_id = Column(Integer(), ForeignKey('users.id'))

    def __repr__(self):
        return f"<Password: {self.id}, Password: {self.hash[:5]} Occurrances: {self.hash_count}>"

    @classmethod
    def create_password(cls, hash, hashcount, id):
        passCheck = cls(hash = hash, hash_count=hashcount, user_id=id )
        session.add(passCheck)
        session.commit()

        cls.all[passCheck.id] = passCheck
        return passCheck
    
    @classmethod
    def delete_passcheck(cls, id):
        session.query(cls).filter_by(id=id).delete()
        session.commit()



mail_breachs = Table(
    'mail_breachs',
    Base.metadata,
    Column('mail_id', ForeignKey("email_checks.id"), primary_key=True),
    Column('breach_id', ForeignKey("breachs.id"), primary_key=True),
    extend_existing=True,
)

# For further improvements of the app To check email breachs
class EmailCheck(Base):

    all = {}

    __tablename__ = "email_checks"
    id = Column(Integer(), primary_key=True)
    email_checked = Column(String(), nullable=False)
    date_checked = Column(DateTime(), server_default=func.now())
    no_of_breaches = Column(Integer(), nullable=False)

    user_id = Column(Integer(), ForeignKey('users.id'))
    breaches = relationship("Breach", secondary=mail_breachs, back_populates="emailChecks")

    def __repr__(self):
        return f"<Email: {self.id}, email: {self.email_checked} Number of breaches: {self.no_of_breaches}>"

    @classmethod
    def create_email(cls, email, num_of_breaches, id, breach =None):
        mailCheck = cls(email_checked= email, no_of_breaches=num_of_breaches, user_id=id )
        
        if breach:
            mailCheck.breaches.extend(breach)
            
        session.add(mailCheck)
        session.commit()

        cls.all[mailCheck.id] = mailCheck
        return mailCheck
    
    @classmethod
    def clear_table(cls):
        session.query(cls).delete()
        session.commit()
    
    @classmethod
    def delete_email(cls, id):
        session.query(cls).filter_by(id=id).delete()
        session.commit()
    
    @classmethod
    def find_email(cls, em):
        email = session.query(cls).filter_by(email_checked = em)
        return email if email else None
    
class Breach(Base):

    all = {}

    __tablename__ = "breachs"
    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    domain = Column(String(), nullable=False)
    breachDate = Column(String(), nullable=False)
    exposedData = Column(String(), nullable=False)

    emailChecks = relationship("EmailCheck", secondary=mail_breachs, back_populates="breaches") 

    def __repr__(self):
        return f"<Breach: {self.id}, name: {self.name} domain: {self.domain}>"

    @classmethod
    def create_breach(cls, name, domain, breachDate, exposedData):
        breachCheck = cls(name=name, domain=domain, breachDate=breachDate, exposedData=exposedData )
        session.add(breachCheck)
        session.commit()

        cls.all[breachCheck.id] = breachCheck
        return breachCheck
    
    @classmethod
    def clear_table(cls):
        session.query(cls).delete()
        session.commit()