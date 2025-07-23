# multilingual_gui_chatbot.py

import tkinter as tk
from tkinter import scrolledtext
from googletrans import Translator

class TranslatorChatBot:

    def __init__(self, root):
        self.translator = Translator()
        self.root = root
        self.root.title("Manual Multilingual Translator Chat System")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")

        # Your language selection
        tk.Label(root, text="Your Language Code (e.g., en, hi, ta):", bg="#f0f0f0").pack()
        self.your_lang_entry = tk.Entry(root, width=30)
        self.your_lang_entry.pack()
        # self.your_lang_entry.insert(0, "en")  # default: English

        # Recipient Language selection
        tk.Label(root, text="Recipient's Language Code (e.g., es, fr, hi, ta):", bg="#f0f0f0").pack()
        self.lang_entry = tk.Entry(root, width=30)
        self.lang_entry.pack()
        # self.lang_entry.insert(0, "en")  # default: English

        # Chat display
        self.chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, state='disabled', font=("Times New Roman", 10))
        self.chat_window.pack(pady=10)
        encryption_message = "Messages are end-to-end encrypted. Only people in this chat can read them. Learn more."
        self.update_chat(f"{encryption_message}")


        # Create a frame to hold input and send button
        self.input_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.input_frame.pack(pady=10)

        # Input field
        self.input_field = tk.Entry(self.input_frame, width=50)
        self.input_field.pack(side=tk.LEFT, padx=(0, 10))

        # Send button
        send_btn = tk.Button(self.input_frame, text=">>", command=self.send_message)
        send_btn.pack(side=tk.LEFT)
        

    def send_message(self, event = 'None'):
        user_msg = self.input_field.get()
        if not user_msg.strip():
            return

        user_lang = self.your_lang_entry.get().strip()
        recipient_lang = self.lang_entry.get().strip()

        try:
        # Validate both language codes
            if not user_lang:
                raise ValueError("Please enter your language code.")
            
            if not recipient_lang:
                raise ValueError("Please enter recipient language code.")

            # Test by translating a dummy string
            _ = self.translator.translate("test", src=user_lang, dest=recipient_lang)

            # Translate user's message
            translated_msg = self.translator.translate(user_msg, src=user_lang, dest=recipient_lang).text
            # self.update_chat(f"You (translated to {recipient_lang}): {translated_msg}")
            self.input_field.delete(0, tk.END)

            # Simulate friend's reply
            self.simulate_reply(recipient_lang, user_lang)

        except Exception as e:
            self.update_chat(f"[❌ Error] Invalid language code or translation failed: {str(e)}")
            return 

        # Detect sender language
        detected = self.translator.detect(user_msg)
        user_lang = detected.lang

        # Translate message
        translated_msg = self.translator.translate(user_msg, src=user_lang, dest=recipient_lang).text

        # Display message
        self.update_chat(f"You: {translated_msg}")

        # Clear input field
        self.input_field.delete(0, tk.END)

    def simulate_reply(self, from_lang, to_lang):
        reply_window = tk.Toplevel(self.root)
        reply_window.title("Simulate Friend's Reply")
        tk.Label(reply_window, text=f"Enter friend's message in {from_lang}:").pack()

        reply_entry = tk.Entry(reply_window, width=50)
        reply_entry.pack(padx=10, pady=10)

        def handle_reply():
            reply_text = reply_entry.get()
            translated_reply = self.translator.translate(reply_text, src=from_lang, dest=to_lang).text
            # self.update_chat(f"Friend ({from_lang}): {reply_text}")
            self.update_chat(f"Friend: {translated_reply}")
            reply_window.destroy()

        tk.Button(reply_window, text="Send Reply", command=handle_reply).pack(pady=5)

    def update_chat(self, msg):
        self.chat_window.configure(state='normal')
        self.chat_window.insert(tk.END, msg + "\n")
        self.chat_window.configure(state='disabled')
        self.chat_window.yview(tk.END)

# Launch the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorChatBot(root)
    root.mainloop()