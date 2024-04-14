"""
The goal of this algorithm is to parse a log file that contains login attempts
and extract to another file the users who have tried to log in more than 3 times.
"""

import re
from pathlib import Path
from collections import Counter

def load_login_records(file_path):
    file_text = None
    try:
        with open(file_path, "r") as logins:
            file_text = logins.read()
    except FileNotFoundError as e:
        print(f"{type(e)}. Error loading file: {file_path}:\n{e}")
    except Exception as e:
        print(f"{type(e)}. Unexpected error loading file: {file_path}:\n{e}")
    finally:
        return file_text

def count_login_tries(records):
    user_records = re.findall(r"User: (\w+\.\w+)", records)
    return Counter(user_records)

def get_users_to_review(login_tries):
    return dict((user, tries) for user, tries in login_tries.items() if tries >= 3)

def export_users_to_review(users_to_review, file_name):
    items_to_review = "\n".join(f"{key}: {value}" for key, value in users_to_review.items())
    
    try:
        with open(file_name, "w") as file_to_review:
            file_to_review.write(items_to_review)
    except Exception as e:
        print(f"{type(e)}. Error exporting file: {file_name}:\n{e}")

def main():
    file_path = Path(__file__).parent / "Logins.log"
    records = load_login_records(file_path)

    if records:
        login_tries = count_login_tries(records)
        print("login_tries:", login_tries)

        users_to_review = get_users_to_review(login_tries)
        print("users_to_review:", users_to_review)

        export_file_name = Path(__file__).parent / "Logins_to_review.txt"
        print("export_file_name:", export_file_name)
        export_users_to_review(users_to_review, export_file_name)

if __name__ == "__main__":
    main()