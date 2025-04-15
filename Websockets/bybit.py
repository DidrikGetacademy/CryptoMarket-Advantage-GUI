
import time
import hmac
import hashlib

import asyncio
import websockets
import json 
import os
from dotenv import load_dotenv
load_dotenv()
private_marketdata_wss= "wss://stream.bybit.com/v5/private"
public_marketdata_wss = "wss://stream.bybit.com/v5/public/linear"
order_entry_wss = "wss://stream.bybit.com/v5/trade"
BYBIT_APIKEY=os.getenv("bybit_api_key")
BYBIT_APISECRET=os.getenv("bybit_secret_api_key")


async def ping(ws):
    while True:
        await ws.send(json.dumps({"op": "ping"}))
        await asyncio.sleep(60)


def get_auth_payload():
    expires=int(time.time()) + 10
    signature_payload = f"{BYBIT_APIKEY}{expires}"
    signature = hmac.new(
        BYBIT_APISECRET.encode(), signature_payload.encode(), hashlib.sha256
    ).hexdigest()

    return {
        "op": "auth",
        "args": [BYBIT_APIKEY, expires, signature],
    }




async def connect_private():
    """
    Subscribe to your own account data (e.g., positions, executions)	Private (needs auth)
    """
    async with websockets.connect(private_marketdata_wss) as ws:
        auth_payload = get_auth_payload()
        await ws.send(json.dumps(auth_payload))

        response = await ws.recv()
        print("auth response:", response)

        subscribe_payload = {
            "op": "subscribe",
            "args": ["position"]
        }
        await ws.send(json.dumps(subscribe_payload))

        while True:
            message = await ws.recv()
            print("Private message: ", message)







async def connect_order_entry():
    """
    Send trading commands (e.g., place orders)	Authenticated WebSocket Order Entry
    """
    async with websockets.connect(order_entry_wss) as ws:
        await ws.send(json.dumps(get_auth_payload()))
        print(await ws.recv())

        order_payload = {
            "op": "order.create",
            "args": {
                "category": "linear",
                "symbol": "BTCUSDT",
                "side": "Buy",
                "orderType": "Limit",
                "qty": "0.01",
                "price": "30000",
                "timeInForce": "GTC",
            }
        }
        await ws.send(json.dumps(order_payload))

        while True:
            message = await ws.recv()
            print("Order message: ", message)
            




async def connect_public():
    """
    Subscribe to market data (e.g., trades, orderbook) Public
    """
    async with websockets.connect(public_marketdata_wss) as ws:
        payload = {
            "op": "subscribe",
            "args": ["publicTrade.BTCUSDT"]
        }
        await ws.send(json.dumps(payload))
        print("Subscribed to publicTrade.BTCUSDT")

        await asyncio.gather(
            ping(ws),
            receieve(ws)
        )
        while True:
            message = await ws.recv()
            print("public message: ", message)



async def receieve(ws):
    while True:
        message = await ws.recv()
        print("Public Message:", message)








asyncio.run(connect_order_entry())
asyncio.run(connect_public())        
asyncio.run(connect_private())