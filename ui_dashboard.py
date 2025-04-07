import customtkinter as ctk
import threading
from smolagents import CodeAgent, HfApiModel, FinalAnswerTool,Tool, DuckDuckGoSearchTool, UserInputTool, GoogleSearchTool, VisitWebpageTool,PythonInterpreterTool,TransformersModel
import yaml
from Telegram.Telegram_utils import run_telegram_bot_in_thread,client,load_Chat_group_ids
import threading













ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CryptoTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Crypto Tracker Dashboard")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", self.exit_fullscreen) 

        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=10)
        self.sidebar.pack(side="left", fill="y", padx=15, pady=15)

        self.wallet_button = ctk.CTkButton(self.sidebar, text="Wallet Tracker", command=self.show_wallet_Tracking_System)
        self.wallet_button.pack(pady=15, padx=10, fill="x")

        self.Telegram_button = ctk.CTkButton(self.sidebar, text="Telegram Tracker", command=self.Telegram_Tracker_System)
        self.Telegram_button.pack(pady=15, padx=10, fill="x")


        self.Twitter_button = ctk.CTkButton(self.sidebar, text="Twitter Tracker", command=self.show_Twitter_Tracking_system)
        self.Twitter_button.pack(pady=15, padx=10, fill="x")

        self.BotConfig_BTN = ctk.CTkButton(self.sidebar, text="Bot's configuration", command=self.show_bot_configuration)
        self.BotConfig_BTN.pack(pady=15, padx=10, fill="x")

        self.Agent = ctk.CTkButton(self.sidebar, text="AI Agent Teammate", command=self.show_Agent_chat)
        self.Agent.pack(pady=15, padx=10, fill="x")

        self.exit_button = ctk.CTkButton(self.sidebar, text="Exit", fg_color="red", command=self.quit)
        self.exit_button.pack(pady=15, padx=10, fill="x")

        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.pack(side="right", expand=True, fill="both", padx=15, pady=15)

        self.content_label = ctk.CTkLabel(self.content_frame, text="Welcome to Crypto Tracker", font=("Arial", 24))
        self.content_label.pack(pady=50)

        self.loading_label  = ctk.CTkLabel(self.content_frame,text="")
        self.is_processing = False

  


    def show_Twitter_Tracking_system(self):
        self.update_content("Telegram Tracker")
        Twitter_Tracker_Frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        Twitter_Tracker_Frame.pack(side="top", expand=True, fill="both", padx=15, pady=15)

        Live_Twitter_Alert_Frame = ctk.CTkFrame(Twitter_Tracker_Frame, corner_radius=10)
        Live_Twitter_Alert_Frame.pack(side="left", expand=True, fill="both", padx=15, pady=15)

        Telegram_Title = ctk.CTkLabel(Live_Twitter_Alert_Frame, text="Live Alert Notifications", font=("Arial", 18, "bold"))
        Telegram_Title.pack(pady=10)

        large_font = ctk.CTkFont(family="Arial", size=18) 
        self.chat_display_Twitter = ctk.CTkTextbox(
        Live_Twitter_Alert_Frame,
        wrap="word",
        state="disabled",
        text_color="white",
        font=large_font
        )
        self.chat_display_Twitter.pack(expand=True, fill="both", pady=10, padx=10)


        Twitter_Config_frame = ctk.CTkFrame(Twitter_Tracker_Frame, corner_radius=10)
        Twitter_Config_frame.pack(side="left", expand=True, fill="both", padx=15, pady=15)

        Twitter_Title = ctk.CTkLabel(Twitter_Config_frame, text="Twitter Configuration", font=("Arial", 18, "bold"))
        Twitter_Title.pack(pady=10)

        self.Twitter_Start_Tracking_BTN = ctk.CTkButton(
            Twitter_Config_frame, 
            text="Start Telegram Tracker", 
            command=None
        )
        self.Twitter_Start_Tracking_BTN.pack(pady=10)



    def show_wallet_Tracking_System(self):
        self.update_content("Wallet Address Tracker")
                #FRAME CONTAINER FOR BOTS
        Wallet_Tracker_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        Wallet_Tracker_frame.pack(side="top", expand=True, fill="both", padx=15, pady=15)


        Whale_frame = ctk.CTkFrame(Wallet_Tracker_frame, corner_radius=10)
        Whale_frame.pack(side="left", expand=True, fill="both", padx=15, pady=15)

        Whale_Title = ctk.CTkLabel(Whale_frame, text="Whale Tracker", font=("Arial", 18, "bold"))
        Whale_Title.pack(pady=10)


        Insider_Frame = ctk.CTkFrame(Wallet_Tracker_frame, corner_radius=10)
        Insider_Frame.pack(side="left", expand=True, fill="both", padx=15, pady=15)

        Insider_Title = ctk.CTkLabel(Insider_Frame, text="Insider Tracker", font=("Arial", 18, "bold"))
        Insider_Title.pack(pady=10)





    def Telegram_Tracker_System(self):
        self.update_content("Telegram Tracker")
        Telegram_Tracker_Frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        Telegram_Tracker_Frame.pack(side="top", expand=True, fill="both", padx=15, pady=15)

        Live_Alert_Frame = ctk.CTkFrame(Telegram_Tracker_Frame, corner_radius=10)
        Live_Alert_Frame.pack(side="left", expand=True, fill="both", padx=15, pady=15)

        Telegram_Title = ctk.CTkLabel(Live_Alert_Frame, text="Live Alert Notifications", font=("Arial", 18, "bold"))
        Telegram_Title.pack(pady=10)

        large_font = ctk.CTkFont(family="Arial", size=18) 
        self.chat_display_telegram = ctk.CTkTextbox(
        Live_Alert_Frame,
        wrap="word",
        state="disabled",
        text_color="white",
        font=large_font
        )
        self.chat_display_telegram.pack(expand=True, fill="both", pady=10, padx=10)


        Telegram_Config_frame = ctk.CTkFrame(Telegram_Tracker_Frame, corner_radius=10)
        Telegram_Config_frame.pack(side="left", expand=True, fill="both", padx=15, pady=15)

        Telegram_Title = ctk.CTkLabel(Telegram_Config_frame, text="Telegram Configurations", font=("Arial", 18, "bold"))
        Telegram_Title.pack(pady=10)

        self.Telegram_Start_Tracking_BTN = ctk.CTkButton(
            Telegram_Config_frame, 
            text="Start Telegram Tracker", 
            command=self.start_telegram_tracking
        )
        self.Telegram_Start_Tracking_BTN.pack(pady=10)

        self.Telegram_STOP_Tracking_BTN = ctk.CTkButton(
            Telegram_Config_frame, 
            text="Stop Tracker", 
            command=self.start_telegram_tracking,
            fg_color="red"
        )
        self.Telegram_STOP_Tracking_BTN.pack(pady=10)
        self.Telegram_STOP_Tracking_BTN.pack_forget() 

        self.fetch_Channel_ids_BTN = ctk.CTkButton(
            Telegram_Config_frame,
            text="Fetch Telegram Channel id's",
            command=self.fetch_telegrams_ids,
        )
        self.fetch_Channel_ids_BTN.pack(pady=10)

        self.Telegram_ids_textbox = ctk.CTkTextbox(
            Telegram_Config_frame,
            wrap="word",
            state="disabled",
            text_color="white",
            font=large_font,
            height=500,
            width=500
        )
        self.Telegram_ids_textbox.pack(side="right",pady=10, padx=10)

        self.add_group_tracking_BTN = ctk.CTkButton(
            Telegram_Config_frame,
            text="Add group to tracking List",
            command=None,
        )
        self.add_group_tracking_BTN.pack(pady=10)

        self.Group_Tracking_Textbox = ctk.CTkTextbox(
            Telegram_Config_frame,
            wrap="word",
            state="disabled",
            text_color="white",
            font=large_font,
            height=500,
            width=500
        )
        self.Group_Tracking_Textbox.pack(side="right", pady=10, padx=10)



    def fetch_telegrams_ids(self):
        dialog_data = load_Chat_group_ids()
        dialog_info = "\n\n".join([f"Name: {dialog[0]}\nID: {dialog[1]}" for dialog in dialog_data])
        self.update_dialog_display(dialog_info)


    
    def update_dialog_display(self,dialog_info):
        self.Telegram_ids_textbox.configure(state="normal")
        self.Telegram_ids_textbox.delete("1.0", "end")
        self.Telegram_ids_textbox.insert("end",dialog_info)
        self.Telegram_ids_textbox.configure(state="disabled")
            

            

    def stop_telegram_tracking(self):
        """Stops the telegram bot.."""
        if hasattr(self, "bot_thread") and self.bot_thread.is_alive():
            print("Stopping telegram bot...")
            self.Telegram_STOP_Tracking_BTN.pack_forget()
            self.Telegram_Start_Tracking_BTN.configure(state="normal")
            client.disconnect()


    def start_telegram_tracking(self):
        self.Telegram_Start_Tracking_BTN.configure(state="disabled")
        self.Telegram_STOP_Tracking_BTN.pack(pady=10)
        self.bot_thread = threading.Thread(target=run_telegram_bot_in_thread, args=(self,),daemon=True)
        self.bot_thread.start()


    def update_chat_telegram_alert(self, message):
        """Update chat display with new message"""
        self.chat_display_telegram.configure(state="normal")
        self.chat_display_telegram.insert("end", message + "\n")
        self.chat_display_telegram.configure(state="disabled")
        self.chat_display_telegram.see("end")



    def show_Agent_chat(self):

        self.update_content("The LearnReflect Agent")

        # AGENT CHAT FRAME (Main Container)
        agent_chat_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        agent_chat_frame.pack(expand=True, fill="both", padx=15, pady=15)


        self.loading_label = ctk.CTkLabel(agent_chat_frame, text="")
        self.loading_label.pack_forget()  # Start hidden

        # LEFT SIDE (Chat UI - 50%)
        chat_frame = ctk.CTkFrame(agent_chat_frame, width=700, corner_radius=10)
        chat_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        # CHAT DISPLAY (Read-Only)
        large_font = ctk.CTkFont(family="Arial", size=18) 
        self.chat_display = ctk.CTkTextbox(
        chat_frame,
        wrap="word",
        state="disabled",
        text_color="white",
        font=large_font
        )
        self.chat_display.pack(expand=True, fill="both", pady=10, padx=10)

        # Input Frame (Align entry & button)
        input_frame = ctk.CTkFrame(chat_frame)
        input_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        # User Input
        self.user_input = ctk.CTkEntry(
        input_frame,
        placeholder_text="Type a message...",
        width=450,
        font=large_font
        )
        self.user_input.pack(side="left", padx=5, fill="x", expand=True)

        # Enter key to send
        self.user_input.bind("<Return>", self.send_message)

        # Send Button
        send_button = ctk.CTkButton(input_frame, text="Send", command=self.send_message)
        send_button.pack(side="right", padx=5)

        # RIGHT SIDE (Reserved for Future Use - 50%)
        right_frame = ctk.CTkFrame(agent_chat_frame, width=700, corner_radius=10)
        right_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        # Placeholder Label (So the right side is visible)
        right_label = ctk.CTkLabel(right_frame, text="Right Side Content Here", font=("Arial", 18))
        right_label.pack(pady=20)

    def send_message(self,event=None):
        """Handle user message & and AI response"""
        if self.is_processing:
            return
        
        user_message = self.user_input.get().strip()
        if not user_message:
            return
        
        self.update_chat("You: " + user_message + "\n")
        self.user_input.delete(0, "end")

        self.loading_label.pack(pady=5)
        self.loading_label.configure(text="AI is thinking...")

        self.is_processing = True
        threading.Thread(
            target=self.run_agent_async,
            args=(user_message,),
            daemon=True
        ).start()



    def update_chat(self, message):
        """Update chat display with new message"""
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", message)
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")   # Auto-scroll





    def run_agent_async(self, user_message):
        """Get response from LLM"""
        try:
       
            final_answer = FinalAnswerTool()
            model = HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct")
            #model = TransformersModel("./Agent/local_model")
  

            with open(r"C:\Users\didri\Desktop\Programmering\TradingBots Program\Agent\prompts.yaml", 'r') as stream:
                prompt_templates = yaml.safe_load(stream)
    
            image_generation_tool = Tool.from_space(
                "black-forest-labs/FLUX.1-schnell",
                name="image_generator",
                description="Generate an image from a prompt"
            )
            agent = CodeAgent(
                    model=model,
                    tools=[final_answer, image_generation_tool], 
                    max_steps=6,
                    verbosity_level=1,
                    prompt_templates=prompt_templates,
                )
            
            Response = agent.run(user_message)

            self.after(0, self.handle_agent_response, Response)
            
           
        except Exception as e:
            self.after(0,self.update_chat(f"Error: {str(e)}\n"))
        finally: 
            self.after(0,self.finish_processing)



    def handle_agent_response(self, response):
            """Handle successful response"""
            if isinstance(response, dict) and "final_answer" in response:
                self.update_chat("LearnReflect Agent: " + response["final_answer"] + "\n")
            elif isinstance(response, str):
                self.update_chat("LearnReflect Agent: " + response.strip() + "\n")
            else:
                self.update_chat("Error: Invalid response format\n")

    def finish_processing(self):
        """Clean up after processing"""
        if self.loading_label.winfo_exists():  
                self.loading_label.pack_forget()
        self.is_processing = False


    def show_bot_configuration(self):
        self.update_content("The ultimate Botsystem")

        #FRAME CONTAINER FOR BOTS
        bot_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        bot_frame.pack(side="top", expand=True, fill="both", padx=15, pady=15)


        ###SNIPER SIDE FRAME
        sniper_frame = ctk.CTkFrame(bot_frame, corner_radius=10)
        sniper_frame.pack(side="left", expand=True, fill="both", padx=15, pady=15)

        sniper_title = ctk.CTkLabel(sniper_frame, text="Sniper Bot", font=("Arial", 18, "bold"))
        sniper_title.pack(pady=10)

        sniper_content = ctk.CTkLabel(sniper_frame, text="Sniper bot settings and configurations go here.", font=("Arial", 14))
        sniper_content.pack(pady=10)

        sniper_sell_frame = ctk.CTkFrame(sniper_frame, corner_radius=10)
        sniper_sell_frame.pack(pady=15, fill="x")


        ###FRONTRUNNER SIDE FRAME
        frontrunner_frame = ctk.CTkFrame(bot_frame, corner_radius=10)
        frontrunner_frame.pack(side="left", expand=True, fill="both", padx=15, pady=15)

        frontrunner_title = ctk.CTkLabel(frontrunner_frame, text="Frontrunner Bot", font=("Arial", 18, "bold"))
        frontrunner_title.pack(pady=10)

        frontrunner_content = ctk.CTkLabel(frontrunner_frame, text="Frontrunner bot settings and configurations go here.", font=("Arial", 14))
        frontrunner_content.pack(pady=10)

        frontrunner_sell_frame = ctk.CTkFrame(frontrunner_frame, corner_radius=10)
        frontrunner_sell_frame.pack(pady=15, fill="x")
        

        ###SNIPER CONFIG
        sell_label_sniper = ctk.CTkLabel(sniper_sell_frame, text="Set Auto Sell Delay (minutes):", font=("Arial", 14))
        sell_label_sniper.pack(side="left", padx=10)
        self.sell_entry_sniper = ctk.CTkEntry(sniper_sell_frame, placeholder_text="Enter minutes", width=120)
        self.sell_entry_sniper.pack(side="left", padx=10)
        self.run_SniperBOT = ctk.CTkButton(sniper_frame, text="Run Sniper Bot", command="")
        self.run_SniperBOT.pack(side="bottom", pady=20, anchor="center")  



        ###Frontrunner CONFIG
        sell_label_sniper = ctk.CTkLabel(frontrunner_sell_frame, text="Set Auto Sell Delay (minutes):", font=("Arial", 14))
        sell_label_sniper.pack(side="left", padx=10)
        self.sell_entry_frontrunner = ctk.CTkEntry(frontrunner_sell_frame, placeholder_text="Enter minutes", width=120)
        self.sell_entry_frontrunner.pack(side="left", padx=10)
        self.Run_FrontRunnerBOT = ctk.CTkButton(frontrunner_frame, text="Run Frontunner BOT", command="")
        self.Run_FrontRunnerBOT.pack(side="bottom", pady=20, anchor="center") 




    #BOT CONFIG sell function 
    def apply_sell_delay(self):
        minutes = self.sell_entry.get() 
        print(f"Auto sell will occur after {minutes} minute(s).")





    def update_content(self, text):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.content_label = ctk.CTkLabel(self.content_frame, text=text, font=("Arial", 24))
        self.content_label.pack(pady=50)



    def exit_fullscreen(self, event=None):
        """Exit fullscreen when ESC is pressed"""
        self.attributes("-fullscreen", False)

if __name__ == "__main__":
    app = CryptoTrackerApp()
    app.mainloop()
