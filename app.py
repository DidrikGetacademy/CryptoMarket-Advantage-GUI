# app.py (Tkinter version with async support)
import asyncio
import threading
import tkinter as tk
from ui_dashboard import CryptoTkinterDashboard

class AsyncTkinterApp: 
    def __init__(self):
        self.root = tk.Tk()
        self.dashboard = CryptoTkinterDashboard(self.root)
        self.loop = asyncio.new_event_loop()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def run_async(self):
        async def wrapper():
            await self.dashboard.initialize_application()
            while True:
                self.root.update()
                await asyncio.sleep(0.1)

        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(wrapper())

    def on_close(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.root.destroy()

def main():
    app = AsyncTkinterApp()
    
    # Run async loop in separate thread
    async_thread = threading.Thread(target=app.run_async, daemon=True)
    async_thread.start()
    
    # Start Tkinter main loop
    app.root.mainloop()

if __name__ == "__main__":
    main()