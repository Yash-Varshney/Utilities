import requests

import tkinter as tk
from tkinter import *

import threading

import pandas

from bs4 import BeautifulSoup

import sys

import lxml.html as lh

from PIL import ImageTk,Image

from io import BytesIO

bg_color = "#F7F7F7"
label_color = "#f8f9a7"
text_color = "#73879C"
head_font = ('Helvetica', 15,'bold')
label_font = ('Helvetica')
tkDefaultFont = label_font
url_login = "http://oas.iitmandi.ac.in/instituteprocess/common/login.aspx"
url_home = "http://oas.iitmandi.ac.in/InstituteProcess/Common/Default.aspx"
login_data = {"btnLogin" : "Log in"}

root = tk.Tk()
root.title("OAS-IIT MANDI")
root["bg"] = bg_color
img_logo = ImageTk.PhotoImage(Image.open("Assets/Images/iit_Mandi_logo.png"))
img_vision = ImageTk.PhotoImage(Image.open("Assets/Images/scaling_the_height.png"))
sess = requests.Session()

def on_entry_click_user(event):
    """function that gets called whenever entry is clicked"""
    if E_username.get() == 'LDAP Username':
       E_username.delete(0, "end") # delete all the text in the entry
       E_username.insert(0, '') #Insert blank for user input
       E_username.config(fg = "black", bg = "#faffbd")
def on_focusout_user(event):
    if E_username.get() == '':
        E_username.insert(0, 'LDAP Username')
        E_username.config(fg = 'grey',bg = "white")

def on_entry_click_password(event):
    """function that gets called whenever entry is clicked"""
    if E_password.get() == 'LDAP Password':
       E_password.delete(0, "end") # delete all the text in the entry
       E_password.insert(0, '') #Insert blank for user input
       E_password.config(fg = "black",show="*", bg = "#faffbd")
def on_focusout_password(event):
    if E_password.get() == '':
        E_password.insert(0, 'LDAP Password')
        E_password.config(fg = 'grey',bg = "white")

def on_Login():
    login_data["txtLoginId"] = E_username.get()
    login_data["txtPassword"] = E_password.get()
    page_login = sess.get(url_login)
    soup_login = BeautifulSoup(page_login.content,"html5lib")
    login_data["__VIEWSTATE"] = soup_login.find(
        "input", attrs={"name": "__VIEWSTATE"}
    )["value"]
    login_data["__EVENTVALIDATION"] = soup_login.find(
        "input", attrs={"name": "__EVENTVALIDATION"}
    )["value"]
    sess.post(url_login, data=login_data)

    
# Variables
V_username = StringVar(root)
V_password = StringVar(root)

# Entries
E_username = Entry(root,textvariable=V_username)
E_username.insert(0,'LDAP Username')
E_username.bind('<FocusIn>', on_entry_click_user)
E_username.bind('<FocusOut>', on_focusout_user)
E_username.config(fg = 'grey', width=31)

E_password = Entry(root,textvariable=V_password)
E_password.insert(0,'LDAP Password')
E_password.bind('<FocusIn>', on_entry_click_password)
E_password.bind('<FocusOut>', on_focusout_password)
E_password.config(fg = 'grey', width=31)

# Labels
L_logo = Label(root,image = img_logo)
L_IPS = Label(root, text = "Institute process solution", bg = bg_color, fg = text_color, font=head_font)

# Buttons
B_login = Button(root,text = "Log In", command = on_Login,bg = 'white', fg = text_color)

# Placing
L_logo.place(x=50,y=25)
L_IPS.place(x=50, y=250)
E_username.place(x=50, y=290)
E_password.place(x=50, y=320)
B_login.place(x=145,y=350)

root.geometry("358x390+200+200")
root.mainloop()