import tkinter as tk

# create main window
root = tk.Tk()
root.title("My First Tkinter App")
root.geometry("500x500")

# add a label
label = tk.Label(root, text="Hello, Tkinter!")
label.pack(padx=10)

textbox = tk.Text(root, height=5, padx =10, pady = 10)
textbox.pack()

myentry = tk.Entry(root)
myentry.pack() 

buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0, weight=1)
buttonframe.columnconfigure(1, weight=1)
buttonframe.columnconfigure(2, weight=1)

btn1 = tk.Button(buttonframe, text="1")
btn1.grid(row=0, column=0, sticky="ew")

btn2 = tk.Button(buttonframe, text="2")
btn2.grid(row=0, column=1, sticky="ew")

btn3 = tk.Button(buttonframe, text="3")
btn3.grid(row=0, column=2, sticky="ew")

btn4 = tk.Button(buttonframe, text="4")
btn4.grid(row=2, column=0, sticky="ew")

btn5 = tk.Button(buttonframe, text="5")
btn5.grid(row=2, column=1, sticky="ew")

btn6 = tk.Button(buttonframe, text="6")
btn6.grid(row=2, column=2, sticky="ew")


buttonframe.pack(fill="x",)



# add a button
def on_click():
    label.config(text="Button clicked!")

button = tk.Button(root, text="Click Me", command=on_click)
button.pack(pady=10)

# run the app
root.mainloop()
