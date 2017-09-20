#! /usr/bin/env python
# coding: utf-8

from Mongo import Mongo
db = Mongo()
from MyCrypto import MyCrypto
from cursesmenu import *
from cursesmenu.items import *
import time
import getpass
import os
menu = 0


def register():

    # create user
    user = raw_input("Enter your username:")
    while (db.get_user(user)):
        user = raw_input("This username exists!\nEnter your username:")

    while True:
        password = getpass.getpass("Password for " + user + ":")
        password_again = getpass.getpass("Password for " + user + " again:")
        if(password == password_again):
            break
        else:
            print("The passwords you entered aren't the same!")

    # hashing password
    password = MyCrypto().hash_password(password)
    # create json
    web_data = dict([])
    data = dict([("user", user), ("password", password),
                 ("web_data", web_data)])
    # insert in my db
    try:
        db.insert_user(data)
        print(user + ' created!')
    except:
        print("Error on insert, try again.")

    time.sleep(1.5)


def sign_in():
    user = raw_input("Username:")
    while (not db.get_user(user)):
        user = raw_input("This username not exists!\nUsername:")

    while (True):
        user_on = db.get_user(user)
        password = getpass.getpass("Password:")
        # hashing password
        password = MyCrypto().hash_password(password)
        if(password == user_on["password"]):
            break
        else:
            print("Incorrect password! Try again...")

    logged = True
    create_logged_menu(user_on)


def nothing():
    print('oi')

##
# Menu Functions
##


def create_logged_menu(user):
    # remove sign in
    menu.items.pop(0)

    # change subtitle
    menu.subtitle = "User:" + user["user"]

    create_web = FunctionItem("Create website account", nothing)
    read_web = FunctionItem("Read website account", nothing)
    delete_web = FunctionItem("Delete website account", nothing)
    manage_account = FunctionItem("Manage your account", nothing)

    menu.append_item(create_web)
    menu.append_item(read_web)
    menu.append_item(delete_web)
    menu.append_item(manage_account)

    # remove register
    menu.items.pop(0)


def create_menu():

    global menu

    menu = CursesMenu(
        "Password Manager - Create by: Vinicius Drago Romano, Higor Augusto Bassi Rozan", 'Disconnected')

    item_register = FunctionItem("Sign in", sign_in)

    item_login = FunctionItem("Register", register)

    menu.append_item(item_register)
    menu.append_item(item_login)

    menu.show()


if __name__ == '__main__':
    create_menu()
