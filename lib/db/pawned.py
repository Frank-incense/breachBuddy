import requests
from requests.models import HTTPError
import getpass, hashlib, re

email_api_url = "https://haveibeenpwned.com/api/v3/breachedaccount/"
password_api_url = "https://api.pwnedpasswords.com/range/"
hibp_api_key = "f4cc6062971845c890b231e94481cdd9"

def checkPassword(user):
    password = getpass.getpass("Input a password: ")
    password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest()
    print(password_hash)
   
    try: 
        pass_res = requests.get(f"{password_api_url}{password_hash[0:5]}")
        print("Checking database for hash matches")
        
        if pass_res.status_code != 200:
            raise HTTPError
        
    except HTTPError:
        print("\nError while attempting to connect to...")
        print(f"{pass_res.url}")
        print(f"HTTP Response code: {pass_res.status_code}")
    
    except Exception as e:
        print("Error occurred checking for compromised password...")
        print(f"{e}")
    
    else:
        pass_matches = pass_res.text.splitlines()
        pass_count = 0
        
        from .models import PasswordCheck
        for hash in pass_matches:
            pre, suf = hash.split(":")
            
            if password_hash.upper() == password_hash[0:5].upper()+pre:
                print(password_hash, "=", password_hash[0:5]+pre )
                pass_count = int(suf)
                
                PasswordCheck.create_password(
                    id= user.id,
                    hashcount = pass_count,
                    hash =password_hash,
                    )

        if pass_count:
            print("Kindly Ensure you change passwords of accounts using this password.")
            print(f"Password has appeared {pass_count:,} times in the database")
        
        else:
            print("Phewks. You're safe for now. Remember to keep good cyber Hygiene and Password keeping practices.")

def checkEmail(user):
    email_pattern = r"[a-z][a-z0-9.]+[a-z0-9]+@[a-z.]+.[a-z]+"
    emailcheck = re.compile(email_pattern)
    email = ""
    count = 0
    
    while not emailcheck.match(email):
        email = input("Please input your email address: ")
        
        if not emailcheck.match(email):
            print("Kindly input a correct email format.")
    
    headers = {
        "hibp-api-key": hibp_api_key
    }
    try:
        email_res = requests.get(f"{email_api_url}{email}/?truncateResponse=false", headers=headers)
        
        if email_res.status_code != 200:
            print(email_res.status_code)
            raise HTTPError
            
    except HTTPError as http:
        print(f"HTTP error: {http}")
    
    else:
        emails = email_res.json()
        from .models import EmailCheck, Breach
        breach = []
        
        for em in emails:
            breach.append(Breach.create_breach(name=em['Name'],domain=em['Domain'], breachDate=em['BreachDate'], exposedData=", ".join(em['DataClasses'])))
            count += 1

        found = EmailCheck.find_email(em = email)
        
        if not found:
            EmailCheck.create_email(email=email, num_of_breaches=count, id=user.id, breach=breach)
        else:
            print("Email already in history select option 3 in the menu to view history.")