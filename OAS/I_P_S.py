import requests

import tkinter as tk
from tkinter import *

import threading

import pandas

from bs4 import BeautifulSoup

import sys

import lxml.html as lh

from PIL import ImageTk, Image

from io import BytesIO

lightblue = "#F7F7F7"
yellow = "#faffbd"
blue = "#73879C"
darkblue = "#2c344c"

head_font = ("Helvetica", 15, "bold")
label_font = "Helvetica"
tkDefaultFont = label_font

url_login = "http://oas.iitmandi.ac.in/instituteprocess/common/login.aspx"
url_home = "http://oas.iitmandi.ac.in/InstituteProcess/Common/Default.aspx"
url_guest = (
    "http://oas.iitmandi.ac.in/InstituteProcess/GuestHouse/GuestHouseRequest.aspx"
)
url_seatbooking = (
    "http://oas.iitmandi.ac.in/InstituteProcess/Facility/BusSeatReservation.aspx"
)
url_passengerinfo = (
    "http://oas.iitmandi.ac.in/InstituteProcess/Facility/PassengerMain.aspx"
)
login_data = {"btnLogin": "Log in"}

root = tk.Tk()
root.title("Institute Process Solution")
root["bg"] = lightblue

img_logo = ImageTk.PhotoImage(Image.open("Assets/Images/iit_Mandi_logo.png"))
img_vision = ImageTk.PhotoImage(Image.open("Assets/Images/scaling_the_height.png"))
img_bus = ImageTk.PhotoImage(Image.open("Assets/Images/bus.png"))
img_guest = ImageTk.PhotoImage(Image.open("Assets/Images/guest.png"))
img_logout = ImageTk.PhotoImage(Image.open("Assets/Images/logout.png"))
img_passenger = ImageTk.PhotoImage(Image.open("Assets/Images/pass.png"))

sess = requests.Session()


def loginpage():
    def on_entry_click_user(event):
        """function that gets called whenever entry is clicked"""
        if E_username.get() == "LDAP Username":
            E_username.delete(0, "end")  # delete all the text in the entry
            E_username.insert(0, "")  # Insert blank for user input
            E_username.config(fg="black", bg=yellow)

    def on_focusout_user(event):
        if E_username.get() == "":
            E_username.insert(0, "LDAP Username")
            E_username.config(fg="grey", bg="white")

    def on_entry_click_password(event):
        """function that gets called whenever entry is clicked"""
        if E_password.get() == "LDAP Password":
            E_password.delete(0, "end")  # delete all the text in the entry
            E_password.insert(0, "")  # Insert blank for user input
            E_password.config(fg="black", show="*", bg=yellow)

    def on_focusout_password(event):
        if E_password.get() == "":
            E_password.insert(0, "LDAP Password")
            E_password.config(fg="grey", bg="white", show="")

    def on_Login():
        login_data["txtLoginId"] = E_username.get()
        login_data["txtPassword"] = E_password.get()
        page_login = sess.get(url_login)
        soup_login = BeautifulSoup(page_login.content, "html5lib")
        login_data["__VIEWSTATE"] = soup_login.find(
            "input", attrs={"name": "__VIEWSTATE"}
        )["value"]
        login_data["__EVENTVALIDATION"] = soup_login.find(
            "input", attrs={"name": "__EVENTVALIDATION"}
        )["value"]
        page_login = sess.post(url_login, data=login_data)
        login_tree = lh.fromstring(page_login.content)
        script_elements = login_tree.xpath("//script")
        text = str(script_elements[4].text_content())
        text = (
            text.replace("\n", "")
            .replace("\t", "")
            .replace("\r", "")
            .replace("   ", "")
        )
        if len(text) != 0:
            print("Invalid Username or Password")
        else:
            L_logo.destroy()
            L_IPS.destroy()
            E_username.destroy()
            E_password.destroy()
            B_login.destroy()
            homepage()

    # Variables
    V_username = StringVar(root)
    V_password = StringVar(root)

    # Entries
    E_username = Entry(root, textvariable=V_username)
    E_username.insert(0, "LDAP Username")
    E_username.bind("<FocusIn>", on_entry_click_user)
    E_username.bind("<FocusOut>", on_focusout_user)
    E_username.config(fg="grey", width=31)

    E_password = Entry(root, textvariable=V_password)
    E_password.insert(0, "LDAP Password")
    E_password.bind("<FocusIn>", on_entry_click_password)
    E_password.bind("<FocusOut>", on_focusout_password)
    E_password.config(fg="grey", width=31)

    # Labels
    L_logo = Label(root, image=img_logo)
    L_IPS = Label(
        root,
        text="Institute process solution",
        bg=lightblue,
        fg=darkblue,
        font=head_font,
    )

    # Buttons
    B_login = Button(root, text="Log In", command=on_Login, bg="white", fg=blue)

    # Placing
    L_logo.place(x=50, y=25)
    L_IPS.place(x=50, y=250)
    E_username.place(x=50, y=290)
    E_password.place(x=50, y=320)
    B_login.place(x=145, y=350)


def homepage():
    root.geometry("250x390+200+200")
    root["bg"] = darkblue
    print("in homepage")

    page_home = sess.get(url_home)
    page_tree = lh.fromstring(page_home.content)
    roll_no = page_tree.xpath('//span[@id = "lblUserCode"]')
    roll_no = roll_no[0].text_content()
    user = page_tree.xpath('//span[@id = "lblUserName"]')
    user = user[0].text_content()

    # Label
    L_vision = Label(root, image=img_vision)
    L_Welcome = Label(root, text="Welcome %s" % (user.upper()), bg=darkblue, fg="white")

    # Buttons
    B_guest = Button(image=img_guest, border=0)
    B_passenger = Button(image=img_passenger, border=0)
    B_logout = Button(image=img_logout, border=0)
    B_bus = Button(image=img_bus, border=0)

    # Placing
    L_vision.place(x=20, y=15)
    L_Welcome.place(x=30, y=90)
    B_guest.place(x=17, y=130)
    B_passenger.place(x=128, y=130)
    B_logout.place(x=17, y=240)
    B_bus.place(x=128, y=240)


root.geometry("358x390+200+200")
loginpage()
root.mainloop()
