from db.models import User, EmailCheck, PasswordCheck
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align

def create_user():
    click.echo("You are adding a new user to the the database")
    username = input("Input a user name: ")
    user = User.create_user( username )
    return f"Success: {user.username} has been created." if user else "Error creating user."

def delete_user(user):
    print("Your are deleting a user from the database.")
    console = Console()
    id = console.input("[red]Input user id to be deleted: ")
    User.delete_user(id=int(id))
    print(f"User {user.username} has been deleted from the database.")

def see_users():
    print("Printing all system users.")
    users = User.get_all()
    console = Console()
    print("Generating users table")

    if users:
        table = Table(show_header=True, box=None, padding=(0, 1))

        for user in users:
            table.add_row(f"👤 [bold]User: {user.id}[/bold]", f"[cyan]{user.username}[/cyan]")
        
        panel = Panel(table, title="[green]System Users.", expand=False)
        console.print(panel)

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
    email = user.get_email_checks(EmailCheck)
    password = user.get_password_checks(PasswordCheck)
    breaches = sum([e.no_of_breaches for e in email]) if email else 0

    console = Console()
    console.clear()

    title = Align.center("[bold magenta] BreachBuddy - Credential Exposure Checker[/bold magenta]", vertical="top")
    console.print(title)

    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_row("👤 [bold]User[/bold]", f"[cyan]{user.username}[/cyan]")
    table.add_row("📅 [bold]Last Check[/bold]", f"[yellow] {email[0].date_checked if email else 0} [/yellow]")
    table.add_row("📧 [bold]Emails Scanned[/bold]", f"{str(len(email))if email else 0}")
    table.add_row("🔑 [bold]Passwords Scanned[/bold]", f"{str(len(password))if password else 0}")
    table.add_row("🧨 [bold]Breaches Detected[/bold]", f"[red]{breaches}[/red]")

    panel = Panel(table, title="[green]User Summary", expand=False)
    console.print(panel)

def render_breachs(user):
    email = user.get_email_checks(EmailCheck)
    
    console = Console()
    console.clear()

    title = Align.center("[bold magenta] BreachBuddy - Credential Exposure Checker[/bold magenta]", vertical="top")
    console.print(title)
    
    table = Table(show_header=False, box=None, padding=(0, 1))
    if email: 
        for e in email:
            print(e)
            breaches = e.breaches
            for breach in breaches:
                table.add_row(f"[bold]{breach.name}[/bold]", f"[cyan]{breach.domain}[/cyan]")
        
    panel = Panel(table, title="[green]Breach History", expand=False)
    console.print(panel)

