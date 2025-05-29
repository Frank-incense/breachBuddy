from models import PasswordCheck
import requests
from requests.models import HTTPError
import getpass, hashlib

def checkPassword(id):
    password = getpass.getpass("Input a password: ")
    password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest()
    print(password_hash)
    try: 
        pass_res = requests.get(f"https://api.pwnedpasswords.com/range/{password_hash[0:5]}")
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
        
        for hash in pass_matches:
            pre, suf = hash.split(":")
            if password_hash.upper() == password_hash[0:5].upper()+pre:
                print(password_hash, "=", password_hash[0:5]+pre )
                pass_count = int(suf)
                PasswordCheck(
                    user_id= id,
                    hash_count = pass_count,
                    hash_prefix =password_hash[0:5],
                    )

        if pass_count:
            print("Kindly Ensure you change passwords of accounts using this password.")
            print(f"Password has appeared {pass_count:,}in the database")
        else:
            print("Phewks. You're safe for now. Remember to keep good cyber Hygiene and Password keeping practices.")
        