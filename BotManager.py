from Bots import FrontRunningBot, SnipingBot
from Logger.Logger import log
import asyncio

class BotOrchestrator:
    """Manages bot lifecycle based on config (enable/disable bots).
      -Dynamically initializes FrontRunningBot or SnipingBot.
      -Starts all bots asynchronously.
    """
    def __init__(self, config):
        log("🎛️ Initializing Bot Orchestrator")
        self.bots = []
        log(f"⚙️ Loaded configuration: { {k:v for k,v in config.items() if k != 'snipe_token'} }")
        self._init_bots(config)
        log(f"🤖 Total bots initialized: {len(self.bots)}")

    def _init_bots(self, config):
        log("🛠️ Starting bot initialization process")
        
        if config.get('frontrunning_enabled'):
            log("🚦 Frontrunning enabled - initializing bot")
            gas_boost = config.get('gas_multiplier', 1.20)
            self.bots.append(FrontRunningBot(gas_boost))
            log("✅ FrontRunningBot added to active bots")
        else:
            log("⏭️ Frontrunning disabled in config")

        if config.get('sniping_enabled'):
            log("🎯 Sniping enabled - initializing bot")
            log(f"🔫 Snipe parameters - Tokens: {list(config['snipe_tokens'].keys())}")

            if not config.get('snipe_tokens'):
                log("⏭️ No snipe tokens configured")
                return
            for token, amount in config['snipe_tokens'].items():
                 log(f"🔫 Initializing snipe for {token[:6]}... - Amount: {amount} ETH")
                 self.bots.append(SnipingBot(
                    token_address=token,
                    buy_amount=amount
                ))
                 log(f"✅ Added SnipingBot for {token[:6]}...")
        log(f"📊 Bot initialization complete - Total bots: {len(self.bots)}")

    async def start_all(self):
        """Start all bots asynchronously"""
        log(f"🚀 Starting all {len(self.bots)} bot(s)")
        tasks = []
        for index, bot in enumerate(self.bots):
            log(f"🔌 Starting bot {index+1}/{len(self.bots)} - {bot.__class__.__name__}")
            tasks.append(bot.start())
        await asyncio.gather(*tasks)
        log("✅ All bots started successfully")