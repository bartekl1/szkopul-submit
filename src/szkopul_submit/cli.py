from getpass import getpass
from  typing import Any
import requests
import argparse
import pathlib
import json
import time
import sys
import re
import os

def get_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Token {api_key}",
    }

def get_config() -> dict[str, Any]:
    if not os.path.isfile("szkopul.config.json"):
        print("Error: can't find config file.")
        sys.exit(1)
    with open("szkopul.config.json", encoding="UTF-8") as file:
        config = json.load(file)
    return config

def init_config() -> None:
    api_key = getpass("API key (won't be echoed): ")
    contest = input("Contest name or URL: ")

    if contest.startswith("http://") or contest.startswith("https://"):
        regex_value = re.findall(r"^https?:\/\/szkopul\.edu\.pl\/c\/([a-zA-Z-_]+)(?:\/.*)?$", contest)
        if len(regex_value) == 0:
            print("Error: Can't extract contest name from URL.")
            sys.exit(1)
        contest = regex_value[0]

    auth_ping = requests.get("https://szkopul.edu.pl/api/auth_ping", headers=get_headers(api_key))
    if not auth_ping.ok:
        print("Error: Can't authenticate with provided API key.")
        sys.exit(1)
    username = re.findall(r"^pong (.*)$", auth_ping.json())[0]
    print(f"Logged in as {username}")
    
    problems_list = requests.get(f"https://szkopul.edu.pl/api/c/{contest}/problem_list/", headers=get_headers(api_key))
    if not problems_list.ok:
        print(f"Error: Can't find contest {contest}")
        sys.exit(1)

    config = {
        "api_key": api_key,
        "contest": contest,
    }

    with open("szkopul.config.json", "w", encoding="UTF-8") as file:
        json.dump(config, file)
    
    print("Configuration saved to szkopul.config.json")

def submit(args: argparse.Namespace) -> None:
    filepath = args.path
    if not os.path.isfile(filepath):
        print(f"Error: file {filepath} do not exist.")
        sys.exit(1)
    
    problem = args.problem
    if problem is None:
        filename = os.path.split(filepath)[1]
        problem_name = re.findall(r"^([a-z]{3})[0-9]*\.(?:cpp|c|py)$", filename)
        if len(problem_name) == 0:
            print("Error: Can't extract problem name from filename. Use --problem <problem_name>.")
            sys.exit(1)
        problem = problem_name[0]

    config = get_config()
    api_key = config["api_key"]
    contest = config["contest"]

    submission = requests.post(f"https://szkopul.edu.pl/api/c/{contest}/submit/{problem}", headers=get_headers(api_key), files={"file": open(filepath, "rb")})
    if not submission.ok:
        print("Error: Can't submit solution.")
        sys.exit(1)
    submission_id = str(submission.json())
    
    if not args.skip_score:
        print("Waiting for score...")
        score = None
        while score is None:
            time.sleep(2)
            submissions = requests.get(f"https://szkopul.edu.pl/api/c/{contest}/problem_submission_list/{problem}/", headers=get_headers(api_key))
            for sub in submissions.json()["submissions"]:
                if str(sub["id"]) == submission_id:
                    score = sub["score"]
                    break
        print(f"Score: {score}")

def main() -> None:
    parser = argparse.ArgumentParser()

    if "--init" not in sys.argv and "-i" not in sys.argv:
        parser.add_argument("path", type=pathlib.Path, help="Path to file to upload")
    parser.add_argument("-p", "--problem", type=str, help="Name of the problem to submit solution for")
    parser.add_argument("-i", "--init", action="store_true", help="Initialize contest configuration in current directory. Ignores other arguments.")
    parser.add_argument("-s", "--skip-score", action="store_true", help="Skip waiting for score, only submit.")

    args = parser.parse_args()

    if args.init:
        init_config()
    else:
        submit(args)

if __name__ == "__main__":
    main()
