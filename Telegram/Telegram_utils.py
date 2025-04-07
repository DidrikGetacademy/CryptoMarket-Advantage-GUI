from telethon import TelegramClient, events
from solders.pubkey import Pubkey
import os
import asyncio
from dotenv import load_dotenv
import threading
load_dotenv()
load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
TROJAN_BOT_ID = os.getenv("TROJAN_BOT_ID")
client = TelegramClient('bot_session', API_ID, API_HASH)

CHANNELS_TO_MONITOR = [] 



####LOADS THE ID's/Names of the telegram groups
def load_Chat_group_ids():    
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    phone_number = os.getenv("phone_number")
    client = TelegramClient('session_name', API_ID, API_HASH)

    dialog_list = []

    async def main():
        await client.start(phone_number) 
        async for dialog in client.iter_dialogs():
            dialog_list.append((dialog.name, dialog.id))

    with client:
        client.loop.run_until_complete(main())

    return dialog_list







def is_valid_solana_address(address):
    """Check if the address is a valid Solana address."""
    try:
        pubkey = Pubkey.from_string(address)  
        return True
    except Exception as e:
        return False

async def buy_token_raydium(token_address):
    """Automate the buy process for a detected token address."""
    try:
        await client.send_message(TROJAN_BOT_ID, f"{token_address}")
        await asyncio.sleep(2)
    except Exception as e:
        print(f"Error buying token: {e}")


async def setup_chat_entities():
    """Set up the channels to monitor."""
    global CHANNELS_TO_MONITOR  
    chat_ids = [-1002169280333, -4697764823]
    for chat_id in chat_ids:
        try:
            entity = await client.get_entity(chat_id)
            CHANNELS_TO_MONITOR.append(entity)
        except Exception as e:
            print(f"Failed to get entity for {chat_id}: {e}")


def run_telegram_bot_in_thread(app_instance):
    """Run the Telegram bot in a separate thread."""

    Telegram_Channels = [] 
        
    async def start_telegram_bot():
        """Start the Telegram client and listen for messages."""
        await client.start()
        await setup_chat_entities()
        await client.run_until_disconnected()

    
    
    @client.on(events.NewMessage())
    async def new_message_listener(event):
        """Listen for messages in the monitored Telegram channels."""
        print(f"Received message from {event.chat_id}: {event.raw_text}")  
        if event.chat_id not in Telegram_Channels: 
            print("Message not from a monitored channel, ignoring.") 
            return 
        
        message = event.raw_text
        print(f"Processing message: {message}")  
        
        
        #Updates the Telegram Chat gui with the new messages
        app_instance.update_chat_telegram_alert(message)
        
        words = message.split()
        for word in words:
            if is_valid_solana_address(word):
                if len(word) == 44 and word.isalnum():
                    print(f"Valid Solana address found: {word}, buying token...")  
                    await buy_token_raydium(word)
                    break  


    def bot_task():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_telegram_bot())
    
        threading.Thread(target=bot_task, daemon=True).start()