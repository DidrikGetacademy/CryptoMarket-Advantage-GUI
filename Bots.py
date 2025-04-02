from Logger.Logger import log
from basebot import BaseCryptoBot
from Global_Config import TARGET_ADDRESSES  




class FrontRunningBot(BaseCryptoBot):
    """
            Goal: Detect swap transactions or target addresses in mempool.
            Action: Attempts to frontrun by submitting a competing transaction with higher gas.
            Triggers: Swap method detection or target address match.
    """
    def __init__(self, gas_boost):
        log("🚀 Initializing FrontRunningBot")
        super().__init__()


    def execute_frontrun():
        log("💸 Executing  frontrun order")
        return




class SnipingBot(BaseCryptoBot):
    """
            Goal: Detect newly listed tokens or target token addresses.
            Action: Executes a buy order when a target token transaction is detected.
            Triggers: Token address match or target address interaction.
    """
    def __init__(self, token_address, buy_amount):
        log(f"🎯 Initializing SnipingBot for token {token_address[:6]}...")
        super().__init__()

    def _execute_snipe():
        log("💸 Executing snipe order")
    