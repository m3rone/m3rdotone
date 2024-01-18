import zbase32 as zb
import hashlib as hl
import requests as req

ADVANCED = "https://openpgpkey.{domain}/.well-known/openpgpkey/{domain}/hu/{encoded}?l={localpart}"
ADVANCEDPOLICY = "https://openpgpkey.{domain}/.well-known/openpgpkey/{domain}/policy"
DIRECT = "https://{domain}/.well-known/openpgpkey/hu/{encoded}?l={localpart}"
DIRECTPOLICY = "https://{domain}/.well-known/openpgpkey/policy"

class WkdResults:
    def __init__(self):
        self.advancedpolicy = False
        self.advancedpolicyerror = ""
        self.directpolicy = False
        self.directpolicyerror = ""
        self.advancedkey = False
        self.advancedkeyerror = ""
        self.directkey = False
        self.directkeyerror = ""
        self.advancedheader = False
        self.advancedheadererror = ""
        self.directheader = False
        self.directheadererror = ""

    def __repr__(self):
        return f"advancedpolicy = {self.advancedpolicy}, advancedkey = {self.advancedkey}, directpolicy = {self.directpolicy}, directkey = {self.directkey}"

def fullverify(email:str):
    results = WkdResults()
    email = email.lower()
    local, domain = email.split("@")
    localhash = hl.sha1(local.encode()).digest()
    localencode = zb.encode(localhash)

    # check advanced policy
    try:
        advancedpolicyget = req.head(ADVANCEDPOLICY.format(domain = domain))
        advancedpolicyget.raise_for_status()
    except Exception as error:
        results.advancedpolicyerror = str(error)
    else:
        results.advancedpolicy = True

    # check direct policy
    try:
        directpolicyget = req.head(DIRECTPOLICY.format(domain = domain))
        directpolicyget.raise_for_status()
    except Exception as error:
        results.directpolicyerror = str(error)
    else:
        results.directpolicy = True

    # check advanced key
    try:
        advancedkeyget = req.head(ADVANCED.format(domain = domain, encoded = localencode, localpart = local))
        advancedkeyget.raise_for_status()
    except Exception as error:
        results.advancedkeyerror = str(error)
    else:
        results.advancedkey = True

    # check direct key
    try:
        directkeyget = req.head(DIRECT.format(domain = domain, encoded = localencode, localpart = local))
        directkeyget.raise_for_status()
    except Exception as error:
        results.directkeyerror = str(error)
    else:
        results.directkey = True

    # check headers for advanced method
    if results.advancedkey:
        advancedkeyhtype = advancedkeyget.headers.get("Content-Type") # type: ignore
        if advancedkeyhtype == "application/octet-stream": 
            results.advancedheader = True
        else:
            results.advancedheadererror = str(advancedkeyhtype)

    # check headers for direct method
    if results.directkey:
        directkeyhtype = directkeyget.headers.get("Content-Type") # type: ignore
        if directkeyhtype == "application/octet-stream": 
            results.directheader = True
        else:
            results.directheadererror = str(directkeyhtype)

    return(results)
