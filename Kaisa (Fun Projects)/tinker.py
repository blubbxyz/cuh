import tkinter as tk
from tkinter import messagebox

class MyGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tkinter Demo")

        self.label = tk.Label(self.root, text="Hello, Tkinter!")
        self.label.pack(padx=10)

        self.textbox = tk.Text(self.root, height=5, padx=10, pady=10)
        self.textbox.pack()

        self.button = tk.Button(self.root, text="Show message", command=self.show_message)
        self.button.pack(pady=10, padx=10)

        self.root.mainloop()

    def show_message(self):
        text = self.textbox.get("1.0", tk.END).strip()
        if text:
            messagebox.showinfo("Your Text", text)
        else:
            messagebox.showwarning("Empty", "Bitte Text eingeben!")

# Starte das GUI
if __name__ == "__main__":
    MyGui() 