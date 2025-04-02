from telethon import TelegramClient, events
from solders.pubkey import Pubkey
import asyncio
import os
from dotenv import load_dotenv

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
TROJAN_BOT_ID = os.getenv("TROJAN_BOT_ID")
client = TelegramClient('bot_session', API_ID, API_HASH)

CHANNELS_TO_MONITOR = [] 






def is_valid_solana_address(address):
    print(f"🔍 Checking if '{address}' is a valid Solana address...")
    try:
        pubkey = Pubkey.from_string(address)  
        print(f"✅ Valid Solana address detected: {address}")
        return True
    except Exception as e:
        print(f"❌ Invalid Solana address: {address} | Error: {e}")
        return False








async def buy_token_raydium(token_address):
    """Automate the buy process for a detected token address."""
    try:
        print(f"🔹 Sending buy request for {token_address}...")

        # Step 1: Start buy process
        await client.send_message(TROJAN_BOT_ID, f"{token_address}")
        await asyncio.sleep(2)


    except Exception as e:
        print(f"❌ Error buying token: {e}")

  
@client.on(events.NewMessage())
async def new_message_listener(event):
    """Listen for messages in the monitored Telegram channels."""
    if event.chat_id not in [-1002169280333, -4697764823]:
        return 
    message = event.raw_text
    print(f"New message from {event.chat_id}: {message}")
    words = message.split()
    for word in words:
        if is_valid_solana_address(word):
            if len(word) == 44 and word.isalnum():
                print(f"✅ Detected valid Solana token address: {word}")
                buy_token_raydium(word)
                break  
            else:
                print(f"❌ Invalid Solana address detected: {word}")









async def setup_chat_entities():
    global CHANNELS_TO_MONITOR  
    chat_ids = [-1002169280333, -4697764823]
    for chat_id in chat_ids:
        try:
            entity = await client.get_entity(chat_id)
            CHANNELS_TO_MONITOR.append(entity)
            print(f"✅ Added channel: {chat_id}")
        except Exception as e:
            print(f"❌ Failed to get entity for {chat_id}: {e}")





async def main():
    await client.start()
    await setup_chat_entities()
    print("🤖 Bot is running & listening for token addresses...")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())

