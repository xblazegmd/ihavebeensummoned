import base64
import hashlib

usrGJP: str | None = None

def generateGJP(password: str = "") -> str:
    """
    Geometry Dash uses this thing called a GJP. It's used for account authentication purposes (commenting, publishing levels, etc)

    Before 2.2, a GJP was the player's password XOR encoded with the key "37526", and encoded with base64.
    But in 2.2 RobTop changed the game to use GJP2. GJP2 is the player's password, salted with "mI29fmAnxgTs", and hashed with SHA1.

    This function takes in the player's password and returns a GJP2.
    """
    saltedPassword = password + "mI29fmAnxgTs" # Salt, makes food taste better, and makes us comment on a GD level
    return hashlib.sha1(saltedPassword.encode()).hexdigest()

def saveGJP(gjp: str) -> None:
    """
    Save the GJP to memory
    """
    global usrGJP
    usrGJP = base64.b64encode(gjp.encode()).decode()

def getGJP() -> str:
    """
    Get the GJP from memory
    """
    if usrGJP is None:
        raise Exception("GJP was not found")
    return base64.b64decode(usrGJP).decode()

def XOR(data: str, key: str) -> str:
    """
    XOR is an encryption method. TLDR; it messes with bytes and stuff (I still don't fully get it yet).
    
    Now XOR is used a lot when it comes to GD. It was used for making a GJP before GJP2 came, it's used for making a CHK, etc.
    So I made this function to XOR encrypt/decrypt anything.
    """
    result = []
    for i in range(len(data)):
        char = ord(data[i])
        xkey = ord(key[i % len(key)])
        result.append(chr(char ^ xkey))
    return "".join(result)

def generateChk(values: list[int | str] = [], key: str = "", salt: str = "") -> str:
    """
    Many request's in the GD servers need this thing called a checksum.
    
    A checksum (CHK) is used as a security measure, to verify that the request wasn't tampered with, and is legit.
    
    Now, GD's method of generating a checksum is:
    
    - Concatenate all specified values and add a salt if needed
    - Hash all values with SHA-1
    - XOR the hash with the specified key
    - Base64 encode the result

    This function basically just makes a checksum, with all the specified valueds, the salt, and the XOR key.
    """
    saltedValues = [*values, salt]

    stringRaw = "".join(map(str, saltedValues))

    stringHashed = hashlib.sha1(stringRaw.encode()).hexdigest()
    stringXored = XOR(stringHashed, key)
    string = base64.urlsafe_b64encode(stringXored.encode()).decode()
    
    return string
