# web3_Config.py
from web3 import Web3
from web3.providers.websocket import WebsocketProvider
import os
from dotenv import load_dotenv
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from Logger.Logger import log
import asyncio

class BlockchainConfig:
    """Centralized blockchain configuration and connection management"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            log("🆕 Creating new BlockchainConfig instance")
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized: 
            log("⏩ Already initialized, skipping __init__")
            return
            
        log("🔧 Initializing BlockchainConfig")
        self._load_environment()
        self._initialized = False  
        
        self.web3 = None
        self.eth_wallet = None
        self.solana_client = None
        self.solana_wallet = None

    def _load_environment(self):
        """Load and validate environment variables"""
        log("📁 Loading .env file")
        try:
            load_dotenv()
            log("✅ .env file loaded successfully")
        except Exception as e:
            log(f"🔴 Failed to load .env file: {str(e)}")
            raise

    async def initialize(self):
        """Main initialization with detailed logging"""
        log("🔁 Starting blockchain initialization")
        if self._initialized:
            log("⏩ Already initialized, skipping initialize()")
            return
        self._initialized = True
        try:
            await self._init_ethereum()
            await self._init_solana()
            log(f"🌍 Connecting to Ethereum: {os.getenv('ALCHEMY_ETHEREUM_WS_URL')[:30]}...")
            log(f"🌍 Connecting to Solana: {os.getenv('HELIUS_SOLANA_WS_URL')[:30]}...")
            eth_connected = self.web3 and self.web3.is_connected()
            sol_connected = self.solana_client and await self.solana_client.is_connected()
            await asyncio.gather(
                self._init_ethereum(),
                self._init_solana()
            )
            log("🎉 Successfully connected to both networks")
            
            if self.eth_wallet:
                log(f"🔐 Active ETH Wallet: {self.eth_wallet.address[:8]}...")
            if self.solana_wallet:
                    sol_pubkey = str(self.solana_wallet.pubkey())
                    log(f"🔐 Active SOL Wallet: {sol_pubkey[:8]}...")  # Now safe
                
            if not eth_connected:
                        raise ConnectionError("Ethereum connection failed")
            if not sol_connected:
                        raise ConnectionError("Solana connection failed")

            log("🎉 Successfully connected to both networks")
        except Exception as e:
            log(f"🔴 Initialization failed: {str(e)}")
            self._initialized = False
            raise


  
    async def _init_ethereum(self):
        """Ethereum connection setup"""
        try:
            log("⛓ Starting Ethereum initialization")
            eth_url = os.getenv("ALCHEMY_ETHEREUM_WS_URL")
            if not eth_url:
                raise ValueError("ALCHEMY_ETHEREUM_WS_URL not set in .env")
            
            log(f"🌐 Connecting to Ethereum node at {eth_url[:30]}...")
            self.web3 = Web3(WebsocketProvider(eth_url, websocket_timeout=30))
            
            if not self.web3.is_connected():
                raise ConnectionError(f"Failed to connect to Ethereum node")
                
            log(f"🟢 Ethereum connected (Chain ID: {self.web3.eth.chain_id})")
            
            # Initialize wallet
            eth_pk = os.getenv("PRIVATE_KEY_ETH_PHANTOMwallet")
            if eth_pk:
                self.eth_wallet = self.web3.eth.account.from_key(eth_pk)
                log(f"💰 ETH Wallet: {self.eth_wallet.address[:8]}...")
            else:
                log("⚠️ No Ethereum private key found")
                
        except Exception as e:
            log(f"🔴 Ethereum initialization failed: {str(e)}")
            self.web3 = None
            raise


    
   
    async def _init_solana(self):
        try:
            log("⛓ Starting Solana initialization")
            sol_url = os.getenv("HELIUS_SOLANA_WS_URL")
            sol_pk = os.getenv("PRIVATE_KEY_SOLANA")
            
            if not sol_url:
                raise ValueError("HELIUS_SOLANA_WS_URL not set in .env")
            if not sol_pk:
                raise ValueError("PRIVATE_KEY_SOLANA not set in .env")

            # Add API key validation
            if "api-key" not in sol_url.lower():
                raise ValueError("Missing API key in Solana URL")

            log(f"🌐 Connecting to Solana node at {sol_url[:30]}...")
            self.solana_client = AsyncClient(sol_url, timeout=30)
            
            # Add better error handling for connection test
            try:
                await asyncio.wait_for(self.solana_client.get_slot(), timeout=10)
                log("🟢 Solana connection verified")
            except Exception as e:
                raise ConnectionError(f"Connection test failed: {str(e)}")
            
            # Initialize wallet
            try:
                self.solana_wallet = Keypair.from_base58_string(sol_pk)
                log(f"💰 SOL Wallet: {str(self.solana_wallet.pubkey())[:8]}...")
            except Exception as e:
                raise ValueError(f"Invalid Solana private key: {str(e)}")
                
        except Exception as e:
            log(f"🔴 Solana initialization failed: {str(e)}")
            if self.solana_client:
                await self.solana_client.close()
            self.solana_client = None
            raise


    async def _connect_ethereum_node(self):
        """Establish WebSocket connection to Ethereum node"""
        web3_provider_url = os.getenv("ALCHEMY_ETHEREUM_WS_URL")
        if not web3_provider_url:
            raise ValueError("ALCHEMY_ETHEREUM_WS_URL not set in .env")
        
        log(f"🌐 Connecting to Ethereum node at {web3_provider_url[:25]}...")
        self.web3 = Web3(WebsocketProvider(web3_provider_url))
        
        if not self.web3.is_connected():
            raise ConnectionError("Failed to connect to Ethereum node")
        log(f"🟢 Ethereum connected (Chain ID: {self.web3.eth.chain_id})")

    def _init_ethereum_wallet(self):
        """Initialize Ethereum wallet from environment variable"""
        private_key = os.getenv("PRIVATE_KEY_ETH_PHANTOMwallet")
        if private_key:
            log("🔑 Initializing Ethereum wallet from private key")
            self.eth_wallet = self.web3.eth.account.from_key(private_key)
            log(f"💰 ETH Wallet: {self.eth_wallet.address[:6]}...")
        else:
            log("⚠️ No Ethereum private key found in .env")

   
    async def _connect_solana_node(self):
        """Establish connection to Solana RPC node"""
        solana_rpc_url = os.getenv("HELIUS_SOLANA_WS_URL")
        if not solana_rpc_url:
            raise ValueError("HELIUS_SOLANA_WS_URL not set in .env")
        
        log(f"🌐 Connecting to Solana node at {solana_rpc_url[:25]}...")
        self.solana_client = AsyncClient(solana_rpc_url)
        log("✅ Solana client created")

    def _init_solana_wallet(self):
        """Initialize Solana wallet from environment variable"""
        private_key = os.getenv("PRIVATE_KEY_SOLANA")
        if not private_key:
            raise ValueError("PRIVATE_KEY_SOLANA not set in .env")
        
        log("🔑 Initializing Solana wallet from private key")
        self.solana_wallet = Keypair.from_base58_string(private_key)
        log(f"💰 SOL Wallet: {str(self.solana_wallet.pubkey())[:6]}...")

    async def _verify_solana_connection(self):
        """Verify Solana connection with actual RPC call"""
        log("🔍 Testing Solana connection...")
        try:
            slot = await self.solana_client.get_slot()
            log(f"🟢 Solana connection verified (Current slot: {slot.value})")
        except Exception as e:
            raise ConnectionError(f"Solana connection test failed: {str(e)}")

    # Wallet management methods
    def set_eth_wallet(self, private_key):
        """Update Ethereum wallet dynamically"""
        if self.web3:
            self.eth_wallet = self.web3.eth.account.from_key(private_key)
            log(f"🔄 Updated ETH wallet to {self.eth_wallet.address[:6]}...")

    def set_solana_wallet(self, private_key):
        """Update Solana wallet dynamically"""
        self.solana_wallet = Keypair.from_base58_string(private_key)
        log(f"🔄 Updated SOL wallet to {self.solana_wallet.pubkey()[:6]}...")

    # Balance checking methods
    def get_eth_balance(self):
        """Get Ethereum wallet balance in ETH"""
        if not self.eth_wallet or not self.web3:
            log("⚠️ Ethereum wallet not initialized")
            return 0
            
        try:
            balance_wei = self.web3.eth.get_balance(self.eth_wallet.address)
            balance_eth = self.web3.from_wei(balance_wei, 'ether')
            log(f"💵 ETH Balance: {balance_eth:.4f}")
            return balance_eth
        except Exception as e:
            log(f"🔴 Error getting ETH balance: {str(e)}")
            return 0

    async def get_solana_balance(self):
        """Get Solana wallet balance in SOL"""
        if not self.solana_wallet or not self.solana_client:
            log("⚠️ Solana wallet not initialized")
            return 0
            
        try:
            resp = await self.solana_client.get_balance(self.solana_wallet.pubkey())
            balance_sol = resp.value / 1_000_000_000
            log(f"💵 SOL Balance: {balance_sol:.2f}")
            return balance_sol
        except Exception as e:
            log(f"🔴 Error getting SOL balance: {str(e)}")
            return 0

    # Cleanup method
    async def close(self):
        """Clean up all blockchain connections"""
        log("🔌 Closing all blockchain connections")
        if self.solana_client:
            await self.solana_client.close()
            log("✅ Solana connection closed")
        if self.web3:
            self.web3 = None
            log("✅ Ethereum connection closed")