
from helper import (check_email, check_password, create_user, render_breachs,
                    see_users, render_dash, get_user, delete_user)
from pyfiglet import Figlet
from rich.console import Console
import getpass

console = Console()

fig = Figlet(font="slant")
BANNER = fig.renderText("BreachBuddy")

OPTIONS = """
    [1] 🔍 Check Email for Exposure
    [2] 🧪 Check Password for Exposure
    [3] 📚 View Past Breach History
    [4] 👤 Manage Account
    [5] 🚪 Exit
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
    isUser = input("Are you a user [Y/N]: ")
    if isUser.lower() == "n":
        user = create_user()
    elif isUser.lower() == "y":

        matched = False
        while not matched:
            id = getpass.getpass("Kindly input your id and press enter: ")
            
            user = get_user(int(id))
            name =input("Kindly input your username: ")
            if not user:
                console.print(f"[red]Error: User id:{id} does not exist")
            elif user.username == name:
                console.print(f"[yellow]Welcome back: {name}.")
                matched = True
                break
            
            else:
                console.print(f"[red]User: {name} not found. Input correct details.")
    
    return user


def menu(user):
    data = None
    if user.username == "admin":
        data = ADMIN
    else:
        data = OPTIONS

    print( data )
    choice = console.input("\n[green]Enter your choice: ").strip()
    return choice

def command_call(choice, user):
    try:
        if choice == "1":
            check_email(user)
        elif choice == "2":
            check_password(user)
        elif choice == "3":
            console.clear()
            render_breachs(user=user)
        elif choice == "4" and user.username == "admin":
            console.clear()
            print("""
            [1] Display users
            [2] Add users
            [3] Delete users
            [4] back
            """)
            choose = console.input("Choose an option: ")
            if choose == '1':
                see_users()
            elif choose == '2':
                create_user()
            elif choose == '3':
                delete_user(user=user)
            else:
                pass

        elif choice == "4":
            console.clear()
            print("""
            [1] Edit User
            [2] Delete user
            [3] Back
            """)
            choose = console.input("Choose an option: ")
            if choose == '1':
                user.update_user()
            elif choose == '2':
                delete_user(user=user)
            else:
                pass
        elif choice == "5":
            console.print(f"Goodbye {user.username} Keep safe.")
            exit()
        else:
            raise ValueError("Kindly input provided input options")
    except ValueError as err:
        console.print(f"[red]Error: {err}")


if __name__ == "__main__":
    user = login()
    

    while True:
        render_dash(user)
        choice = menu(user)
        command_call(choice=choice, user=user)
        console.input("[bold]Press enter to continue.[/bold]")
        