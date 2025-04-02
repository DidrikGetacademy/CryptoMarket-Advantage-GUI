from telethon.sync import TelegramClient
import os
from dotenv import load_dotenv
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
phone_number = os.getenv("phone_number")
client = TelegramClient('session_name', API_ID, API_HASH)

async def main():
    await client.start(phone_number) 
    async for dialog in client.iter_dialogs():
        print(f"{dialog.name}: {dialog.id}")

with client:
    client.loop.run_until_complete(main())
