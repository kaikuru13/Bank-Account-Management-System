# GUI (Tkinter)
from tkinter import *
import os 
from PIL import ImageTk, Image 
# Main Screen
master = Tk() 
master.title('Bank of Kailas')

# Image import 
img = Image.open('bank-logo-symbol.png')
img = img.resize((150, 150))
img = ImageTk.PhotoImage(img)

# Labels 
Label(master, text = "Kailas Bank", font=('Calibri', 14)).grid(row=0, sticky = N, pady = 10)