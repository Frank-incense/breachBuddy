from db.models import User 
from tabulate import tabulate
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align

def create_user():
    click.echo("You are adding a new user to the the database")
    username = input("Input your user name: ")
    user = User.create_user( username )
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

def check_password(user):
    print("Checking your password")
    user.password_check()

def check_email(user):
    print("Checking email")
    user.email_check()

def render_dash(user):
    print("Printing report")
    email = user.get_email_checks()
    password = user.get_password_checks()
    # breach = email.breaches
    
    console = Console()
    console.clear()

    title = Align.center("[bold magenta] BreachBuddy - Credential Exposure Checker[/bold magenta]", vertical="top")
    console.print(title)

    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_row("👤 [bold]User[/bold]", f"[cyan]{user.username}[/cyan]")
    table.add_row("📅 [bold]Last Check[/bold]", f"[yellow] {email[0].date_checked if email else 0} [/yellow]")
    table.add_row("📧 [bold]Emails Scanned[/bold]", str(len(email)))
    table.add_row("🔑 [bold]Passwords Scanned[/bold]", str(len(password)))
    table.add_row("🧨 [bold]Breaches Detected[/bold]", f"[red]{0}[/red]")

    panel = Panel(table, title="[green]User Summary", expand=False)
    console.print(panel)

