import requests

from .errors import *
from utils import API, SECRET, HEADERS, logger
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
        if usrResponse.status_code == 403:
            logger.error(f"Request to {API + 'getGJUsers20.php'} returned a 403 error")
            raise HTTPForbiddenError(f"Request to {API + 'getGJUsers20.php'} returned a 403 error")
        logger.error(f"Request to {API + 'getGJUsers20.php'} failed with status code {usrResponse.status_code}")
        raise BoomlingsError(f"Request to {API + 'getGJUsers20.php'} failed with status code {usrResponse.status_code}")
    
    if usrResponse.text == "-1":
        raise NotFoundError(f"User {username} was not found")
    
    accID = formatUserString(usrResponse.text)["accountID"]

    # STEP 2: Verify password
    passResponse = verifyPassword(password, int(accID))
    return [passResponse, accID]

def verifyPassword(password: str, accID: int) -> str:
    """
    Verify if the specified password is correct.
    
    For now it's verified by loading the player's DM's
    """
    gjp = generateGJP(password)

    params = {
        "accountID": int(accID),
        "gjp2": gjp,
        "secret": SECRET
    }
    response = requests.post(API + "getGJMessages20.php", data=params, headers=HEADERS)

    if not (200 <= response.status_code < 300):
        if response.status_code == 403:
            logger.error(f"Request to {API + 'getGJUsers20.php'} returned a 403 error")
            raise HTTPForbiddenError(f"Request to {API + 'getGJUsers20.php'} returned a 403 error")
        logger.error(f"Request to {API + 'getGJUsers20.php'} failed with status code {response.status_code}")
        raise BoomlingsError(f"Request to {API + 'getGJUsers20.php'} failed with status code {response.status_code}")

    if response.text == "-1":
        raise AuthError("Failed to verify password (possibly incorrect)")

    return gjp