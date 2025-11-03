def formatKeyValuePairs(string: str, map: dict[str, str] | None = None, separator: str = ":") -> dict[str, str]:
    """
    RobTop has a very weird key-value format scattered around in his server responses
    It's usually "key:val:key:val:..." where every second colon separates a key-value pair.

    So to parse it, I made this function that separates this weird mess into a simple dictionary. Additionally, you can specify a map to rename the keys if you want to.    

    For example:
    '1:this:2:that:3:hey:4:whatsup:5:jellybe' would become: { '1': 'this', '2':'that', '3': 'hey', '4': 'whatsup', '5': 'jellybe' } (without a map)

    More neat isn't it?
    """

    parts = string.split(separator) # We split by every single instance of the separator first

    # Then we regroup them into key-value pairs
    result = {}
    for i in range(0, len(parts) - 1, 2):
        key = parts[i]
        value = parts[i + 1]
        result[key] = value

    # If there was a map provided, we map the keys
    if map is not None:
        result = {(map[k] if k in map else k): v for k, v in result.items()}

    return result

def formatCommentObject(string: str) -> list[dict[str, str]]:
    """
    Not to be confused with a comment string

    Comment objects are basically a combination between a comment string and an author/user string, separated by a colon.

    This function just returns a list with the comment string and author/user string, both formatted already.
    """

    comment, author = string.split(":", 1)
    return [formatCommentString(comment), formatUserString(author, separator="~")]

def formatCommentString(string: str) -> dict[str, str]:
    """
    There's a reason the 'formatKeyValuePairs' function has a separator parameter.
    Since for whatever reason, a comment string in GD instead of using "key:val:key:val:...", it uses "key~val~key~val~..." (tildes instead of colons).

    But that may just be since a comment object (not to be confused with comment string) is formatted like "commentstring:authorstring".
    Why couldn't RobTop just make the comment object be separated by tilde's instead? Cuz RobTop, that's why.

    Anyways, this is just a wrapper around the 'formatKeyValuePairs' function with the correct map and separator for comment strings.
    """

    map = {
        "1": "levelID", # Level ID
        "2": "comment", # The comment in itself
        "3": "authorPlayerID", # The author's player ID
        "4": "likes", # The total liked
        # We skip "5" since "5" is unused (meant for "dislikes")
        "6": "messageID", # The message ID
        "7": "spam", # If it was flagged as spam
        "8": "authorAccID", # The author's account ID
        "9": "age", # How old the comment is
        "10": "percent", # The specified percentage put in the comment
        "11": "modBadge", # The moderator badge (if any)
        "12": "modChatColor" # A comma separated list of possible moderator chat colors (only if "modBadge" > 0)
    }

    return formatKeyValuePairs(string, map=map, separator="~")

def formatUserString(string: str, separator: str = ":") -> dict[str, str]:
    """
    An user string is a string that represents a player. Of course.

    This is just a wrapper around the 'formatKeyValuePairs' function with the correct mappings for user strings.
    """

    # I took so long to make this map and I won't even use most of the values here ;-;
    map = {
        "1": "username", # The player's username
        "2": "userID", # The player's ID
        "3": "stars", # The player's total stars
        "4": "demons", # The player's total demons
        # idk if there's even "5" in here
        "6": "ranking", # The player's ranking in the global leaderboard
        "7": "accountHighlight", # Just the account ID. Used for highlighting the player on leaderboards
        "8": "creatorpoints", # The player's total creator points
        "9": "iconID", # Only info I have is "maybe..." and a link to a GitHub issue... idk what this is
        "10": "color", # The player's primary color
        "11": "color2", # The player's secondary color
        # "12"'s also gone...
        "13": "secretCoins", # The player's total secret coins
        "14": "iconType", # The player's icon type
        "15": "special", # "The special number of the player use" what
        "16": "accountID", # The player's account ID (that only makes "accountHighlight" more confising...)
        "17": "usercoins", # The player's user coins
        "18": "messageState", # 0 = All, 1 = Friends only, 2 = None
        "19": "friendsState", # 0 = All, 1 = None
        "20": "youtube", # The player's YouTube URL (if any)
        "21": "cube", # The player's cube ID
        "22": "ship", # The player's ship ID
        "23": "ball", # The player's ball ID
        "24": "ufo", # The player's UFO ID
        "25": "wave", # The player's wave ID
        "26": "robot", # The player's robot ID
        "27": "streak", # The player's streak (there's no way to know the player's streak so this is impossible to get in the response)
        "28": "glow", # The player's glow
        "29": "isRegistered", # If the player is registered or nor
        "30": "globalRank", # The player's global rank
        "31": "friendState", # 0 = Not friended, 1 = Friended, 2 = Pending, 3 = Rejected
        # "32" to "38" are gone... RIP ToT
        "39": "friendRequests", # The player's total friend requests (notification in-game)
        "40": "newFriends", # The player's new friends (notification in-game)
        "41": "newFriendReq", # "appears on userlist endpoint to show if the friend request is new" idk fully what this means
        "42": "age", # The time since the player has submitted a levelScore (what)
        "43": "spider", # The player's spider ID
        "44": "twitter", # The player's Twitter/X URL (if any)
        "45": "twitch", # The player's Twitch URL (if any)
        "46": "diamonds", # The player's diamonds
        # RIP "47"
        "48": "explosion", # The player's explosion ID (ig that's the death effect)
        "49": "modLevel", # 0 = None, 1 = Moderator, 2 = Elder Moderator
        "50": "commentHistoryState", # 0 = All, 1 = Friends only, 2 = None
        "51": "color3", # The player's glow color
        "52": "moons", # The player's total moons
        "53": "swing", # The player's swing ID
        "54": "jetpack", # The player's jetpack ID
        "55": "allDemons", # Breakdown on the player's completed demons ({easy},{medium},{hard},{insane},{extreme},{easyPlat},{mediumPlat},{hardPlat},{insanePlat},{extremePlat},{weekly},{gauntlet})
        "56": "clasicLevels", # Breakdown on the player's completed classic levels ({auto},{easy},{normal},{hard},{harder},{insane},{daily},{gauntlet})
        "57": "platformerLevels", # Breakdown on the player's completed platformer levels ({auto},{easy},{normal},{hard},{harder},{insane})
    }

    return formatKeyValuePairs(string, map=map, separator=separator)
