import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import sqlite3


def classify_item(query):
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

    if user_input.lower() in ["exit", "quit"]:
        chat_box.config(state="normal")
        chat_box.insert(tk.END, "Bot: Goodbye! \n", "bot")
        chat_box.config(state="disabled")
        chat_box.see(tk.END)
        root.after(1000, root.destroy)
    else:
        response = classify_item(user_input)
        chat_box.config(state="normal")
        chat_box.insert(tk.END, f"Bot: {response}\n\n", ("bot",))
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


bg_img = Image.open("bg.png").resize((480, 500), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


chat_box = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, width=55, height=20,
    font=("Arial", 12), state="disabled",
    bg="#FFFFFF", fg="white",  
    highlightthickness=0, bd=0
)
chat_box.place(x=20, y=20, width=440, height=300)

chat_box.tag_config("bot", foreground="green", font=("Arial", 12, "italic"))
chat_box.tag_config("user", foreground="black", font=("Arial", 12, "bold"))

welcome_message = "EcoBot: Type an item and I'll tell you if it's recyclable, hazardous, or compostable. I will also add tips.\n\n"
chat_box.config(state="normal")
chat_box.insert(tk.END, welcome_message, "bot")
chat_box.config(state="disabled")

entry = tk.Entry(
    root, width=50, font=("Arial", 12),
    bg="#FFFFFF", fg="black",  #White input box and black text color
    insertbackground="black",  # cursor 
    bd=0, highlightthickness=0
)
entry.place(x=20, y=340, width=440, height=30)
entry.bind("<Return>", send_message)

send_button = tk.Button(root, text="Enter", command=send_message,
                        font=("Arial", 12), bg="#3A723C", fg="white", width=10, bd=0)
clear_button = tk.Button(root, text="Clear", command=clear_chat,
                         font=("Arial", 12), bg="#f44336", fg="white", width=10, bd=0)

send_button.place(x=120, y=400, width=100, height=35)
clear_button.place(x=260, y=400, width=100, height=35)

root.mainloop()

