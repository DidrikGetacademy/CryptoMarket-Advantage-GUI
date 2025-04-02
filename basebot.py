# basebot.py (updated)
from Blockchain_listner import ETH_BlockChain_Listener,Solana_BlockChain_Listener
from web3_Config import BlockchainConfig
from Logger.Logger import log

class BaseBot:
    
    """Base class for all bots with common blockchain functionality
       Generic blockchain listener with transaction processing (to be overridden).
    """
    def __init__(self, listener_class=ETH_BlockChain_Listener):
        log(f"🛠 Initializing BaseBot with listener: {listener_class.__name__}")
        self.config = BlockchainConfig()
        log(f"🔗 Loaded blockchain config: {self.config.__class__.__name__}")
        
        self.listener = listener_class(handlers=[self])
        log(f"👂 Configured listener with {len(self.listener.handlers)} handlers")
        
        self.trade_executor = None
        log(f"⚙️ Completed {self.__class__.__name__} initialization")

    def process_transaction(self, tx_data):
        log("📥 Received transaction processing request")
        raise NotImplementedError

    async def start(self):
        log(f"🚀 Launching {self.__class__.__name__} listener")
        await self.listener.start_listener()
        log(f"📡 {self.__class__.__name__} listener started successfully")

    def _check_target_addresses(self, tx_data):
        """Unified address checking logic"""
        log(f"🔍 Checking target addresses in transaction: {tx_data.get('hash','Unknown')[:8]}")
        from_target = tx_data.get('from', '') in self.target_addresses
        to_target = tx_data.get('to', '') in self.target_addresses
        result = from_target or to_target
        
        log(f"📌 Address check result: FromTarget={from_target}, ToTarget={to_target}")
        log(f"🎯 Final address match: {result}")
        return result

class BaseCryptoBot(BaseBot):
    """Extends BaseBot with trading logic (executors, trade analysis, history).
    -Auto-initializes Ethereum/Solana transaction executors.
    -Implements common address-checking logic.
    """
    def __init__(self, *args, **kwargs):
        log(f"🧩 Initializing BaseCryptoBot extensions")
        super().__init__(*args, **kwargs)
        self.active_trades = []
        log(f"📦 Initialized active trades list ({len(self.active_trades)} items)")
        
        self.trade_analyzer = TradeAnalysis()
        log("📊 Trade analysis engine initialized")
        
        self.trade_history = []
        log("📚 Trade history ledger created")
        
        log("⚡ Starting executor initialization")
        self._init_executor()
        log("✅ Completed BaseCryptoBot setup")

    def _init_executor(self):
        """Initialize transaction executor based on blockchain"""
        try:
            log("🔄 Beginning executor initialization")
            if isinstance(self.listener, ETH_BlockChain_Listener):
                log(f"⛓ Detected Ethereum listener, initializing executor")
                log(f"💰 Using ETH wallet: {self.config.eth_wallet.address[:6]}...")
                self.trade_executor = Transaction_Executor_ETH_network(
                    self.config.eth_wallet.address,
                    self.config.eth_wallet.key
                )
            elif isinstance(self.listener, Solana_BlockChain_Listener):
                log(f"⛓ Detected Solana listener, initializing executor")
                log(f"💰 Using SOL wallet: {self.config.solana_wallet.pubkey()[:6]}...")
                self.trade_executor = Solana_Transaction_Executor(
                    str(self.config.solana_wallet.pubkey()),
                    self.config.solana_wallet
                )
            log(f"⚡ Successfully initialized {type(self.trade_executor).__name__}")
            log(f"🔐 Executor details: {self.trade_executor.__class__.__name__}")
        except Exception as e:
            log(f"🚨 Critical error in executor initialization: {str(e)}")
            log("🛑 Aborting due to failed executor setup")
            raise