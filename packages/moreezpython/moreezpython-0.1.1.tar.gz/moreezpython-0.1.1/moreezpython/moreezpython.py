import datetime
import time
import requests
import random as rdm

class color:
    #Color
    GRAY = '\033[38;5;247m'
    WHITE = '\033[97m'
    # Blue
    CYAN = '\033[38;5;45m'
    BLUE = '\033[38;5;32m'
    B_BLUE = '\033[38;5;17m'
    L_BLUE = '\033[96m'
    # Green
    L_GREEN = '\033[38;5;83m'
    GREEN = '\033[38;5;46m'
    B_GREEN = '\033[38;5;28m'
    # Purple
    MAGENTA = '\033[35m'
    PURPLE = '\033[38;5;63m'
    L_PURPLE = '\033[38;5;105m'
    B_PURPLE = '\033[38;5;55m'
    # Red
    L_RED = '\033[38;5;1m'
    RED = '\033[38;5;160m'
    B_RED = '\033[38;5;52m'
    # Yellow
    L_YELLOW = '\033[38;5;222m'
    YELLOW = '\033[38;5;220m'
    B_YELLOW = '\033[38;5;214m'
    GOLD = '\033[38;5;136m'

    #Debug Color
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Function Log
def log(what):
    print(f"{color.L_YELLOW}{what}{color.END}")


# Function nostop
def pause():
    input()

date = datetime.datetime.now()
hours = date.hour
minute = date.minute
second = date.second

def wait(seconds):
    time.sleep(seconds)

# Function stop
def stop():
    exit(f"\n{color.WARNING}Exit by Command{color.END}")

def connect(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as errh:
        return False
    except requests.exceptions.ConnectionError as errc:
        return False
    except requests.exceptions.Timeout as errt:
        return False
    except requests.exceptions.RequestException as err:
        return False

def random(min, max, float):
    if not isinstance(min, int):
        error(f"Error, you need to put one int in args in the function random")
    if not isinstance(max, int):
        error("Error, you need to put one int in args in the function random")
    if not isinstance(float, int):
        error("Error, you need to put one int in args in the function random")

    if (float == 0):
       return rdm.randint(min,max)
    else:
        return round(rdm.uniform(min,max), float)

def error(err):
    raise Exception(err)