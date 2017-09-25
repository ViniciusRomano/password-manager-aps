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
from terminaltables import AsciiTable


# global variables
menu = []
logged_user = []


def get_password():
    while (True):
        password = getpass.getpass("Account password:")
        # hashing password
        hash_password = MyCrypto().hash_password(password)
        if(hash_password == logged_user["password"]):
            return password
        else:
            print("Incorrect password! Try again...")


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
    data = dict([("user", user), ("password", password),
                 ("web_data", [])])
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
        user = raw_input("This username does not exists!\nUsername:")

    while (True):
        user_on = db.get_user(user)
        password = getpass.getpass("Password:")
        # hashing password
        password = MyCrypto().hash_password(password)
        if(password == user_on["password"]):
            break
        else:
            print("Incorrect password! Try again...")

    create_logged_menu(user_on)


def change_password():
    global logged_user
    # type old password
    password = getpass.getpass("Your current password:")
    # check password
    if(MyCrypto().hash_password(password) == logged_user["password"]):
        # type new password
        new_password = getpass.getpass("New password:")
        while True:
            password_again = getpass.getpass(
                "New password again:")
            if(new_password == password_again):
                break
            else:
                print("The passwords you entered aren't the same!")

        # update website passwords
        new_web_data = []
        for x in logged_user["web_data"]:
            # decrypt password
            decrypt_password = MyCrypto().decrypt(x["password"].decode(
                'hex'), password)
            # encrypt and change password
            x["password"] = MyCrypto().encrypt(
                decrypt_password, new_password).encode('hex')
            # append
            new_web_data.append(x)

        logged_user["web_data"] = new_web_data
        # update user
        logged_user["password"] = MyCrypto().hash_password(new_password)
        db.update_password(logged_user)
        # update webdata
        db.insert_website(logged_user)
        print('Changed password!')
        time.sleep(1.5)
    else:
        print("Incorrect password!")
        time.sleep(1.5)


def create_website():
     # create website
    password_acc = get_password()
    website_name = raw_input("Website name:")

    while True:
        password = getpass.getpass("Password for " + website_name + ":")
        password_again = getpass.getpass(
            "Password for " + website_name + " again:")
        if(password == password_again):
            break
        else:
            print("The passwords you entered aren't the same!")

    # encrypt password
    password = MyCrypto().encrypt(password, password_acc)
    # convert to hex
    password = password.encode('hex')

    # create json
    logged_user["web_data"].append(
        {"website": website_name, "password": password})
    # insert in my db
    db.insert_website(logged_user)

    print("Website " + website_name + " added!")
    time.sleep(1)


def read_website():
    website_name = raw_input("Website name:")
    password = get_password()
    # get website data
    website = db.get_website(logged_user, website_name)
    # website doesn't exist
    if(len(website) == 1):
        print("This website does not exists!")
        time.sleep(1)
    else:
        # get pass(hex) -> decode hex -> decrypt
        print(MyCrypto().decrypt(website["web_data"][0]["password"].decode(
            'hex'), password))
        time.sleep(3)


def remove_website():
    global logged_user
    website_name = raw_input("Website name:")
    password = get_password()
    # get website data
    website = db.get_website(logged_user, website_name)
    # website doesn't exist
    if(len(website) == 1):
        print("This website does not exists!")
        time.sleep(1)
    else:
        # get pass(hex) -> decode hex -> decrypt
        db.remove_website(logged_user, website["web_data"][0]["website"])
        print("Website removed!")
        time.sleep(1.5)
    # update logged user
    logged_user = db.get_user(logged_user["user"])


def show_table():
    password = get_password()
    table_data = [["Site", "Password"]]
    for x in logged_user["web_data"]:
        # insert each website
        table_data.append([x["website"], MyCrypto().decrypt(x["password"].decode(
            'hex'), password)])

    table = AsciiTable(table_data)
    print(table.table)
    gambs = raw_input("(Press enter to back)")


def modify_website():
    global logged_user
    password_acc = get_password()
    website_name = raw_input("Website name:")
    # get website data
    website = db.get_website(logged_user, website_name)
    # website doesn't exist
    if(len(website) == 1):
        print("This website does not exists!")
        time.sleep(1)
    else:
        # get pass(hex) -> decode hex -> decrypt
        # remove website
        db.remove_website(logged_user, website["web_data"][0]["website"])
        logged_user = db.get_user(logged_user["user"])
        # insert website
        website_name = raw_input("New website name:")
        while True:
            password = getpass.getpass(
                "New password for " + website_name + ":")
            password_again = getpass.getpass(
                "New password for " + website_name + " again:")
            if(password == password_again):
                break
            else:
                print("The passwords you entered aren't the same!")

                # encrypt password
        password = MyCrypto().encrypt(password, password_acc)
        # convert to hex
        password = password.encode('hex')

        # create json
        logged_user["web_data"].append(
            {"website": website_name, "password": password})
        # insert in my db
        db.insert_website(logged_user)

        print("Website " + website_name + " updated!")
        time.sleep(1)

##
# Menu Functions
##


def create_logged_menu(user):

    # remove sign in
    menu.items.pop(0)

    # change subtitle
    menu.subtitle = "User:" + user["user"]

    show_all = FunctionItem("Show all website accounts", show_table)
    create_web = FunctionItem("Create website account", create_website)
    read_web = FunctionItem("Read website account", read_website)
    read_web = FunctionItem("Modify website account", modify_website)
    delete_web = FunctionItem("Delete website account", remove_website)
    manage_account = FunctionItem("Change your password", change_password)

    menu.append_item(show_all)
    menu.append_item(create_web)
    menu.append_item(read_web)
    menu.append_item(delete_web)
    menu.append_item(manage_account)

    # remove register
    menu.items.pop(0)

    # set 'global' user
    global logged_user

    logged_user = user


def create_menu():

    global menu

    menu = CursesMenu(
        "Password Manager - Created by: Vinicius Romano, Higor Rozan", 'Disconnected')

    item_register = FunctionItem("Sign in", sign_in)

    item_login = FunctionItem("Register", register)

    menu.append_item(item_register)
    menu.append_item(item_login)

    menu.show()


if __name__ == '__main__':
    create_menu()
