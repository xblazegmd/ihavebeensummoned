import base64
import requests
import sys
import time

from typing import Callable
from utils import API, SECRET, notify, logger, containsWord
from .errors import *
from .formatReq import *
from .saveFile import loadData
from .security import *

def commentListenerLoop(id: str, onMention: Callable, cooldown: int = 5) -> None:
    """
    Start the "look for tags in comments" like loop
    """
    lastTags = []
    
    while True:
        commentListener(id, lastTags, onMention)
        time.sleep(cooldown)

def commentListener(id: str, lastTags: list, onMention: Callable) -> None:
    """
    Get comments for a level ID and check for any tags
    """
    data = loadData()

    possibleTags = data.get("tags") # Possible tags ppl can give me
    assert possibleTags is not None # So pyright doesn't scream at me

    params = {
        "levelID": id,
        "page": 0,
        "secret": SECRET
    }

    # https://www.boomlings.com/database/getGJComments21.php
    response = requests.post(API + "getGJComments21.php", data=params, headers={"User-Agent": ""})

    if not (200 <= response.status_code < 300): # Not a success
        logger.error(f"Failed to get comments (status code: {response.status_code})")
        return # For some reason this was "sys.exit(1)" before like what
    
    # Format response
    commentsUnformatted = response.text.split("|") # This splits up every comment object in here

    comments = []
    for comment in commentsUnformatted:
        comments.append(formatCommentObject(comment))
    
    # Now check for any tags
    for c in comments:
        cstr = c[0] # Comment string
        userstr = c[1] # Author/User string

        stringEncoded: str = cstr["comment"]
        stringEncoded += "=" * (4 - (len(stringEncoded) % 4) - 1)

        try:
            string = base64.urlsafe_b64decode(stringEncoded).decode("ascii", errors="replace")
        except Exception as e:
            logger.error(f"Could not decode comment: {e} (base64: '{stringEncoded}')")
            continue

        # If I ever get tagged it'll notify me
        if any(containsWord(string.lower(), tag) for tag in possibleTags):
            if string in lastTags:
                continue # Should have already been notified abt this comment

            lastTags.append(string)

            user = userstr["username"]

            # Now I need to remove the tag
            pieces = string.split(" ")
            for piece in pieces:
                if any(tag in piece.lower() for tag in possibleTags):
                    pieces.remove(piece)
                    break
            desc = " ".join(pieces).strip()

            logger.info(f"Mention by {user}: {desc}")
            notify(f"@{user} mentioned you", desc.replace("'", "'\\''"))
            onMention(user, desc)

lastUpload = 0
cooldown = 15

def uploadComment(levelID: str, comment: str) -> int:
    """
    Write and send a comment on the specified level
    """
    global lastUpload

    now = time.time()
    if now - lastUpload < cooldown:
        remaining = int(cooldown - (now - lastUpload)) or 1 # "or 1" will make it so if the remaining time is 0 it puts it as 1 to avoid bugs
        raise CooldownError("Cooldown", remaining=remaining)

    data = loadData()

    username = data.get("username")
    assert username is not None

    commentEncoded = base64.urlsafe_b64encode(comment.encode()).decode()
    percent = 0
    
    # First we need to generate the chk
    checksum = generateChk(values=[username, commentEncoded, levelID, percent], salt="0xPT6iUrtws0J", key="29481")

    # Specify parameters
    params = {
        "accountID": data.get("accID"),
        "gjp2": getGJP(),
        "userName": username,
        "comment": commentEncoded,
        "levelID": int(levelID),
        "percent": percent,
        "chk": checksum,
        "secret": SECRET,
    }

    # https://www.boomlings.com/database/uploadGJComment21.php
    response = requests.post(API + "uploadGJComment21.php", data=params, headers={"User-Agent": ""})
    
    if not (200 <= response.status_code < 300):
        if response.status_code == 403:
            logger.error(f"Request to {API + 'uploadGJComment21.php'} returned a 403 error")
            raise HTTPForbiddenError(f"Request to {API + 'uploadGJComment21.php'} returned a 403 error")
        logger.error(f"Failed to upload comment (status code: {response.status_code}, response: {response.text})")
        raise BoomlingsError(f"Failed to upload comment (status code: {response.status_code})")

    if response.text == "-1":
        logger.error(f"Failed to upload comment (status code: {response.status_code}, response: {response.text})")
        raise BoomlingsError(f"Failed to upload comment (status code: {response.status_code}, response: {response.text})")

    lastUpload = time.time()
    return 0
