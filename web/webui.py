from tkinter import *
import webview

tk = Tk()

def runview():
	tk.geometry('1520x840')
	webview.create_window("Antiplagiat", "http://localhost:5000/")
	webview.start()

runview()
