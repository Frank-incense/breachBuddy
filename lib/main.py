from helper import (check_email, check_password, create_user, 
                    see_users, view_report, get_user)
from pyfiglet import Figlet
import click
import getpass
from rich

fig = Figlet(font="slant")
BANNER = fig.renderText("BreachBuddy")

OPTIONS = """
    [1] 🔍 Check Email for Exposure
    [2] 🧪 Check Password for Exposure
    [3] 📚 View Past Breach History
    [4] 🚪 Exit
    """
ADMIN = """
    [1] 🔍 Check Email for Exposure
    [2] 🧪 Check Password for Exposure
    [3] 📚 View Past Breach History
    [4] 👤 Manage Users
    [5] 🚪 Exit
"""

def login():
    user = None
    print(BANNER)
    print("Credential Exposure Checker | v1.0.0")
    print("Check whether your emails and passwords are exposed through leaks.")
    isUser = ("Are you a user [Y/N]: ")
    if isUser.lower() == "n":
        create_user()
    elif isUser.lower() == "y":
        id = getpass.getpass("Kindly input your id and press enter: ")
        name =input("Kindly input your username: ")
        user = get_user(int(id))
        if user:
            print(f"Welcome back: {name}.")
            (user)
        else:
            print(f"User: {name} not found. Input correct details.")
    
    return user


def menu(user):
    data = None
    if user.username == "admin":
        data = ADMIN
    else:
        data = OPTIONS

    print( data )
    choice = input("\nEnter your choice: ").strip()
    return choice



if __name__ == "__main__":
    user = login()
    while True:
        choice = menu(user)
        