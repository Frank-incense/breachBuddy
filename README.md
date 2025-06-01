# BreachBuddy CLI
## Overview

BreachBuddy is a CLI (Command Line Interface) application developed in Python that helps users check whether their email addresses or passwords have been exposed in public data breaches using the HaveIBeenPwned API. It stores results in a local SQLite database, providing a record of checks conducted and enabling users to review their digital security history.

This tool is intended to promote security awareness and make it easier for individuals to verify the safety of their credentials without needing technical expertise.

## Project Objectives
- Provide a simple command-line utility to check:
    - If an email has appeared in a known data breach

    - If a password has been exposed in a hash dump

- Persist the results to a database for user reference

- Demonstrate how CLI apps can integrate with external APIs and databases

## Achievements

- Built a working CLI interface using Python

- Integrated with the HaveIBeenPwned API for both email and password checks

- Structured a relational database using SQLAlchemy ORM with:

    - Users

    - Email breach records

    - Password hash checks

- reated a many-to-many relationship between email_checks and breaches

- Ensured data persistence and user-based separation of checks

## Challenges

- Mapping API response structures into normalized relational models

- Dealing with edge cases where breached data is inconsistent

- Handling unsupported parameter types during insertions

- Resolving one-to-many and many-to-many relationships via SQLAlchemy

- Managing setup environments and dependency versions across systems

## Database Schema
**Key Tables**

- `users`: Stores user account data.

- `email_checks`: Stores records of email addresses that were checked.

- `password_checks`: Stores results of password hash searches.

- `breachs`: Records of data breach sources.

- `mail_breachs`: Join table for the many-to-many relationship between `email_checks` and breachs.

### Entity-Relationship Overview

```
users
│
├───┬── 1:N ─── email_checks
│   └───┬── M:N ──── breachs (via mail_breachs)
│
└───┬── 1:N ─── password_checks
```

### Project Structure

```
lib/
├── db/
│   ├── __init__.py
│   ├── models.py        # All SQLAlchemy models
│   ├── alembic.ini      # Alembic migration config
|   ├── pawned.py        # API calls 
│   └── migrations/      # Migration versions
├── seed.py              # DB seeding script
├── helper.py            # Utility functions
├── main.py              # Entry point for CLI
├── debug.py             # Debugging and testing functions
```

## Setup Instructions
1. **Clone the repository**
    ```
    git clone https://github.com/Frank-incense/breachBuddy.git
    cd breachBuddy
    ```
2. **Create and activate a virtual environment and install dependencies**
    ```
    pipenv install && pipenv shell
    ```
3. **Set up the database**
    ```
    alembic upgrade head
    ```
4. **Run the CLI app**
    ```
    python lib/main.py
    ```
## Features

- Check if an email has been breached

- Check if a password hash appears in known breaches

- Store and track email/password checks per user

- Database persistence

- CLI search history log (coming soon)

- User registration/authentication via CLI (planned)

## Sample Use Case

1. User enters email to check:

    - API returns associated breach names

    - Results saved to the database

2. User enters password (not stored, only hash used):

    - App checks against breach hashes

    - Displays how many times it appears