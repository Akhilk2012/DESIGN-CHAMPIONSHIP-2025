import tkinter as tk
from tkinter import scrolledtext
import sqlite3


def classify_item(query): #For the printing if item is there
    query = query.lower().strip()
    conn = sqlite3.connect("waste_classification.db")
    cursor = conn.cursor()

    cursor.execute("SELECT category, tip FROM waste_items WHERE item_name=?", (query,))
    result = cursor.fetchone()

    conn.close()
    
    if result:
        category, tip = result
        return f"{query.title()} -> {category} -> Tip: {tip}"
    else:
        return "Sorry, I don't have information on that item. Try another one!"

def send_message(event=None):
    user_input = entry.get().strip()
    if not user_input:
        return
    chat_box.config(state="normal")
    chat_box.insert(tk.END, f"Item: {user_input}\n", "user")
    chat_box.config(state="disabled")
    chat_box.see(tk.END)
    entry.delete(0, tk.END)

    if user_input.lower() in ["exit", "quit"]: #Exit
        chat_box.config(state="normal")
        chat_box.insert(tk.END, "Bot: Goodbye! \n", "bot")
        chat_box.config(state="disabled")
        chat_box.see(tk.END)
        root.after(1000, root.destroy)
    else:
        response = classify_item(user_input)
        chat_box.config(state="normal")
        chat_box.insert(tk.END, f"Bot: {response}\n\n", "bot")
        chat_box.config(state="disabled")
        chat_box.see(tk.END)

def clear_chat():
    chat_box.config(state="normal")
    chat_box.delete("1.0", tk.END)
    chat_box.insert(tk.END, welcome_message, "bot")
    chat_box.config(state="disabled")


root = tk.Tk()
root.title("Bot - Waste Classifier")
root.geometry("480x500")
root.resizable(False, False)
root.configure(bg="#f4f4f4")


chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=55, height=20, font=("Arial", 12), state="disabled")
chat_box.pack(padx=10, pady=10)
chat_box.tag_config("bot", foreground="black", font=("Arial", 12, "italic"))
chat_box.tag_config("user", foreground="blue", font=("Arial", 12, "bold"))


welcome_message = "EcoBot: Type an item and I'll tell you if it's recyclable, hazardous, or compostable. I will also add tips.\n\n"

chat_box.config(state="normal")
chat_box.insert(tk.END, welcome_message, "bot")
chat_box.config(state="disabled")


entry = tk.Entry(root, width=50, font=("Arial", 12))
entry.pack(pady=5)
entry.bind("<Return>", send_message)

button_frame = tk.Frame(root, bg="#f4f4f4")
button_frame.pack()

send_button = tk.Button(button_frame, text="Enter", command=send_message,
                        font=("Arial", 12), bg="#3A723C", fg="white", width=10)
send_button.grid(row=0, column=0, padx=5, pady=5)
                                                                                        #You can change button colors here if you want
clear_button = tk.Button(button_frame, text="Clear", command=clear_chat,
                         font=("Arial", 12), bg="#f44336", fg="white", width=10)
clear_button.grid(row=0, column=1, padx=5, pady=5)

root.mainloop()
