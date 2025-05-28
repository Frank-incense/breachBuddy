from sqlalchemy import (Table, ForeignKey, Column, Integer, String, DateTime, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    username = Column(String(), nullable=False)
    createdAt = Column(DateTime(), server_default=func.now())

    # emails = relationship("EmailCheck", backref=backref("user"))
    passwords = relationship("PasswordCheck", backref=backref("user"))

class PasswordCheck(Base):
    ___tablename__ = "password_checks"
    id = Column(Integer(), primary_key=True)
    hash_prefix = Column(String(), nullable=False)
    checkedAt = Column(DateTime(), server_default=func.now())
    hash_count = Column(Integer(), nullable=False)

    user_id = Column(Integer(), ForeignKey('users.id'))

# mail_breachs = Table(
#     'mail_breachs',
#     Base.metadata,
#     Column('mail_id', ForeignKey("email_checks.id"), primary_key=True),
#     Column('breach_id', ForeignKey("breachs.id"), primary_key=True),
#     extend_existing=True,
# )

# For further improvements of the app To check email breachs
# class EmailCheck(Base):
#     __tablename__ = "email_checks"
#     id = Column(Integer(), primary_key=True)
#     email_checked = Column(String(), nullable=False)
#     date_checked = Column(DateTime(), server_default=func.now())
#     no_of_breaches = Column(Integer(), nullable=False)

#     user_id = Column(Integer(), ForeignKey('users.id'))
#     breaches = relationship("Breach", secondary=mail_breachs, back_populates="breachs")

# class Breach(Base):
#     __tablename__ = "breachs"
#     id = Column(Integer(), primary_key=True)
#     name = Column(String(), nullable=False)
#     domain = Column(String(), nullable=False)
#     breachDate = Column(String(), nullable=False)
#     exposedData = Column(String(), nullable=False)

#     emailChecks = relationship("EmailCheck", secondary=mail_breachs, back_populates="email_checks") 