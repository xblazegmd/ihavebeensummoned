import requests

from utils import API, SECRET, HEADERS
from .formatReq import formatUserString
from .security import generateGJP

def logIn(username: str, password: str) -> list[str]:
    """
    "Log in" to the specified GD account. Kinda...
    
    You see, there is an endpoint to log in called `loginGJAccount.php`, but idk if there is any server backend worries or stuff so I'm not using that.
    So instead, I'll check if the user exists, and try and load DM's to verify the password (since that needs a password)

    This code returns an `int` that will return 0 on success, and negative values on fail.
    Here are some of the errors:
    - -1: Unexcpected error
    - -2: User does not exist
    - -3: Failure to verify password (possibly incorrect)
    """

    # STEP 1: Verify if user exists
    # If user exists, get accountID
    usrParams = {
        "secret": SECRET,
        "str": username
    }
    usrResponse = requests.post(API + "getGJUsers20.php", data=usrParams, headers=HEADERS)

    if not (200 <= usrResponse.status_code < 300):
        return ["-1"] # Unexpected error
    
    if usrResponse.text == "-1":
        return ["-2"] # User does not exist
    
    accID = formatUserString(usrResponse.text)["accountID"]

    # STEP 2: Verify password
    passResponse = verifyPassword(password, int(accID))
    if passResponse in ["-1", "-3"]:
        return [passResponse]
    return [passResponse, accID]

def verifyPassword(password: str, accID: int) -> str:
    """
    Verify if the specified password is correct.
    
    For now it's verified by loading the player's DM's
    
    This code returns an `int` that will return 0 on success, and negative values on fail.
    Here are some of the errors:
    - -1: Unexpected error
    - -3: Failure to verify password (possibly incorrect)
    """
    gjp = generateGJP(password)

    params = {
        "accountID": int(accID),
        "gjp2": gjp,
        "secret": SECRET
    }
    response = requests.post(API + "getGJMessages20.php", data=params, headers=HEADERS)

    if not (200 <= response.status_code < 300):
        return "-1" # Unexpected error

    if response.text == "-1":
        return "-3" # Faliure to verify password

    return gjp
