import tkinter

# Setup the window first.
root = tkinter.Tk()
root.title("Flashcards")
root.geometry("400x400")

# Prepare the text variables and labels for later use inside the key handler.
text_var = tkinter.StringVar()
tkinter.Label(root, textvariable=text_var, font=("Arial", 40)).pack()

# Setup the logic in the key handler.
def key_handler(event):
    text_var.set(event.char)
    print(event.char, event.keysym, event.keycode)

root.bind("<Key>", key_handler)

root.mainloop()