from db.models import User 
from tabulate import tabulate
import click
# create a user
# see users
# check password
# check email
# view report 
def create_user():
    click.echo("You are adding a new user to the the database")
    username = input("Input your user name: ")
    user = User.create_user(username = username)
    return f"Success: {user.username} has been created." if user else "Error creating user."

def see_users():
    print("Printing all system users.")
    users = User.get_all()
    print("Generating users table")
    if users:
        table = tabulate(users, headers=users.keys())
        print(table)
    else:
        print("Error: No users in the database")

def get_user(id):
    return User.find_by_id(id)

def check_password():
    print("Checking your password")

def check_email():
    print("Checking email")

def render_dash(user):
    print("Printing report")
    email = user.get_email_check()
    password = user.get_password_check()




