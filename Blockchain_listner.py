# Blockchain_listner.py
from Logger.Logger import log
import websockets
import json
import os
import asyncio
from web3_Config import BlockchainConfig

class BaseBlockchainListener:
    """Base class for blockchain listeners"""
    def __init__(self, handlers=None):
        log(f"🔧 Initializing BaseBlockchainListener")
        self.config = BlockchainConfig()
        self.handlers = handlers or []
        log(f"👥 Configured with {len(self.handlers)} handler(s)")
        log(f"🌐 Using chain ID: {self.config.web3.eth.chain_id if self.config.web3 else 'N/A'}")


class ETH_BlockChain_Listener(BaseBlockchainListener):
    """Listens to Ethereum mempool for pending transactions, filters by whale addresses.
    -Streams real-time transactions.
    -Passes relevant transactions to bots for processing.
    """
    def __init__(self, handlers=None, whale_addresses=None):
        log("⛓ Initializing Ethereum blockchain listener")
        super().__init__(handlers)
        self.whale_addresses = whale_addresses or []
        log(f"🐳 Tracking {len(self.whale_addresses)} whale addresses" if self.whale_addresses else "⚠️ No whale addresses configured")
        self.web3 = self.config.web3
        log(f"🔗 Connected to Ethereum node: {self.web3.provider.endpoint_uri[:25]}..." if self.web3 else "🔴 No Ethereum connection")
        self.subscription_id = None

    async def listen_eth_mempool(self):
        log("📡 Starting Ethereum mempool listener via WebSocket")
        max_retries = 5
        retry_delay = 3
        
        for attempt in range(max_retries):
            try:
                self.subscription_id = await self.web3.eth.subscribe("newPendingTransactions")
                log(f"🔎 Created subscription (ID: {self.subscription_id[:8]})")
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    log(f"🔴 Failed to create subscription after {max_retries} attempts: {str(e)}")
                    return
                log(f"⚠️ Subscription failed (attempt {attempt+1}/{max_retries}): {str(e)}")
                await asyncio.sleep(retry_delay)

        async for subscription_response in self.web3.eth.subscription_manager.listen_to_new_pending_transactions():
            try:
                if subscription_response['subscription'] != self.subscription_id:
                    continue

                tx_hash = subscription_response['result']
                log(f"📥 New pending transaction detected: {tx_hash.hex()[:12]}...")

                # Get full transaction details
                try:
                    tx_details = self.web3.eth.get_transaction(tx_hash)
                except Exception as e:
                    log(f"⚠️ Failed to get transaction details: {str(e)}")
                    continue

                log(f"📄 Transaction details: {tx_details['hash'].hex()[:8]}... From: {tx_details['from'][:6]}...")

                # Skip non-whale transactions if whale list exists
                if self.whale_addresses and tx_details.get('from') not in self.whale_addresses:
                    log("🐳 Skipping non-whale transaction")
                    continue

                # Process with handlers
                log(f"👨💻 Processing with {len(self.handlers)} handler(s)")
                for handler in self.handlers:
                    try:
                        log(f"➡️ Passing transaction to {handler.__class__.__name__}")
                        handler.process_transaction(tx_details)
                    except Exception as e:
                        log(f"🔴 Handler error ({handler.__class__.__name__}): {str(e)}")

            except Exception as e:
                log(f"🔴 Ethereum listener error: {str(e)}")
                log("⏳ Retrying in 1 second...")
                await asyncio.sleep(1)

    async def start_listener(self):
        log("🚀 Starting Ethereum listener")
        await self.listen_eth_mempool()

class Solana_BlockChain_Listener(BaseBlockchainListener):
    """Monitors Solana transactions via WebSocket for a specific wallet.
    -Streams real-time transactions.
    -Passes relevant transactions to bots for processing.
    """
    def __init__(self, handlers=None):
        log("⛓ Initializing Solana blockchain listener")
        super().__init__(handlers)
        self.wallet_address = str(self.config.solana_wallet.pubkey())
        log(f"💰 Monitoring wallet: {self.wallet_address[:6]}...")
        log(f"🔗 Solana client status: {'Connected' if self.config.solana_client else 'Not connected'}")
        try:
            self.wallet_address = str(self.config.solana_wallet.pubkey())
        except AttributeError:
            log("🔴 No Solana wallet initialized")
            self.wallet_address = ""
    async def listen_solana_mempool(self):
        log("📡 Starting Solana mempool listener")
        ws_url = f"wss://mainnet.helius-rpc.com/?api-key={os.getenv('HELIUS_API_KEY')}"
        log(f"🔗 Connecting to Solana WS endpoint: {ws_url[:30]}...")
        
        async with websockets.connect(ws_url) as ws:
            log("🟢 WebSocket connection established")
            subscription = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "logsSubscribe",
                "params": [{"mentions": [self.wallet_address]}, {"commitment": "confirmed"}]
            }
            log("📨 Sending subscription request")
            await ws.send(json.dumps(subscription))
            log("👂 Listening for Solana transactions...")
            
            while True:
                try:
                    log("🔄 Polling WebSocket connection")
                    response = await ws.recv()
                    log(f"📥 Received response ({len(response)} bytes)")
                    tx_data = json.loads(response)
                    log(f"📄 Transaction data: {str(tx_data)[:100]}...")
                    
                    log(f"👨💻 Processing with {len(self.handlers)} handler(s)")
                    for handler in self.handlers:
                        log(f"➡️ Passing transaction to {handler.__class__.__name__}")
                        handler.process_transaction(tx_data)
                except Exception as e:
                    log(f"🔴 Solana listener error: {str(e)}")
                    log("⏳ Retrying in 1 second...")
                    await asyncio.sleep(1)

    async def start_listener(self):
        log("🚀 Starting Solana listener")
        await self.listen_solana_mempool()