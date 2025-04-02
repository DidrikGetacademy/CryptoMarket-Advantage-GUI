"""
Contains gas multipliers (BASEFEE_PERCENTAGE_MULTIPLIER) and hardcoded target addresses.
"""
GLOBAL_CACHE = {}
BASEFEE_PERCENTAGE_MULTIPLIER = {
    "low": 1.10,  
    "medium": 1.20, 
    "high": 1.25  
}

TARGET_ADDRESSES = {
    'frontrunner': [
        "0xWhale1",
        "0xWhale2",
        "0xAddYourOwnAddressHere"
    ],
    'sniper': [
        "0xTokenCreator",
        "0xNewTokenContract"
    ],
    'both': [
        "0xCommonTarget"
    ]
}
