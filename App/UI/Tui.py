"""
 Projet : Finances-Pro-Max
 Directory : UI
 Name Of File : TUi.py
 Author : Thomas Raymond
 Author : Félix Roussin 
 Date : 10 septembre 2026

Description : UI handler whic appearsin the terminal. This UI is built with a library called Textual.
"""
# Imports to use during the creation of UIs with Textual
import asyncio
import os

import sys

from textual import on
from textual.app import App,ComposeResult
from textual.containers import Center, Container, Horizontal, Middle,Vertical
from textual.widgets import DataTable, Header, Footer, Button, Input, Label,Pretty, RadioButton, RadioSet
from textual.validation import Length, Validator
from textual.binding import Binding
from typing import ClassVar


# Import from SimpleUI which is the old UI
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from API.User import User
import UI.base as base
import time as t
import API.Fichier as fichier
import subprocess
import platform
from getpass import getpass
import pickle

# Classes modified for our App
# Class for a button
class End(Button):
    """
    Button class for eventual usages of buttons. NOT IMPLEMENTED!!!
    """
    num : int  = 0 


    def action_press(self):
        self.num += 1
        
        if(self.num%2 != 0):
            self.label = "press"
            self.add_class("press")
        else:
            self.label = "ass"
            self.remove_class("press")

# Class related to the actual lauching of the APP
class Login(App):
    """
    Manages the APP, it's the most important class
    """
    try_pwd:int = 3 # 3 tries for the pwd

    # Path related to the CSS file wich determines the format appearance of each widget represented in that file
    CSS_PATH="TCSS/login.tcss"


    BINDINGS: ClassVar[list[Binding]]=[
        Binding("ctrl+q","save_and_quit","Quit",show=True,priority=True),
    ] # I dont't know what it is...
    
    # Methods related to the App apperance
    def compose(self) -> ComposeResult:
        """
        Method related to the lauch of the App
        """
        # Calling global variables useful in the function
        global users, names,user
        
        # Reading users et usernames files to be able to verify in the inputs corresponds to an exxisting user
        info_users = fichier.read_content("users_list")
        info_names = fichier.read_content("names")
        
        # Decode binary information and update variables
        if info_users is not None: # Update all users present
            users.append(pickle.loads(info_users))
        if info_names is not None: # update all usernames present
            names.append(pickle.loads(info_names))

        # Lauches the main features
        yield Vertical(Label("$$$$$$$\\  $$\\   $$\\ $$$$$$$\\   $$$$$$\\  $$$$$$$$\\ $$$$$$$$\\ \n$$  __$$\\ $$ |  $$ |$$  __$$\\ $$  __$$\\ $$  _____|\\__$$  __|\n$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ /  \\__|$$ |         $$ |\n$$$$$$$\\ |$$ |  $$ |$$ |  $$ |$$ |$$$$\\ $$$$$\\       $$ |\n$$  __$$\\ $$ |  $$ |$$ |  $$ |$$ |\\_$$ |$$  __|      $$ |\n$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |         $$ |\n$$$$$$$  |\\$$$$$$  |$$$$$$$  |\\$$$$$$  |$$$$$$$$\\    $$ |\n\\_______/  \\______/ \\_______/  \\______/ \\________|   \\__|", id = "title")
                       ,
            Vertical(
                Horizontal(
                        Container(
                                Input(
                                    id="user",
                                    type="text",
                                    valid_empty=False,
                                    validators=[Length(5)],
                                ),
                            ), 
                        Container(
                            Input(id="pwd",
                                password=True,
                                valid_empty=False,
                                validators=[Length(4)]
                            ),
                        ), 
                        id = "inputs",),
                Horizontal(
                    Container(
                        id="errorMessage",
                    ),
                    Vertical(
                        id="buttonBox",
                    ),
                    id="errorBox"
                ),
                id="messageBox",
            ),
            id = "login",
        )
        yield Container(
                    
                    Horizontal(
                        Container(
                            RadioSet(
                                RadioButton("Depot", value="depot", id="depot"),
                                RadioButton("Retrait", value="retrait", id="retrait"),
                                RadioButton("Modifier", value="modifier", id="modification"),
                            ),
                        id="menu",
                        ),    
                        Horizontal(
                            Input(
                                id="ID"
                            ),
                            Input(
                                
                            id="chiffre"  
                            ),
                            id="montant"
                        ),
                        id="top",
                        ),
                    Horizontal(
                        Container(
                            Label(""),
                            Label(""),
                            id="info",
                        ),
                        DataTable(
                            id="table",
                        ),
                        id="middle",
                    ),
                    id="body",
                ) 

    def on_mount(self)-> None:
        """
        Method called when a mount function is called
        """
        global user
        user = None
        self.query_one("#body").display = False
        # Username
        inputUsername = self.query_one('#user', Input) 
        inputUsername.border_subtitle = "Username"

        # Password
        inputPassword = self.query_one('#pwd', Input) 
        inputPassword.border_subtitle = "Password"

    def make_rows(self, username:str, pwd:str, user:User) -> None:
        """
        Method to make the rows of the table
        """
        historic_transactions = user.get_transactions()
        formated_transactions = [("ID", "Raison", "Montant", "Date")]
        for transaction in historic_transactions:
            formated_transactions.append((str(transaction), str(historic_transactions[transaction].get_raison()) , str(historic_transactions[transaction].get_montant()), str(historic_transactions[transaction].get_date())))
        return formated_transactions

    def second_page(self, username:str, pwd:str):
        """
        Method to display the second page of the app
        """
        global user
        ROWS = []
        self.query_one("#body").display = True
        if(user == None):
            user = User(username, pwd)
        ROWS = self.make_rows(username, pwd, user)
        self.query_one("#table").add_columns(*ROWS[0])
        self.query_one("#table").add_rows(ROWS[1:])
        labels = self.query_one( "#info")
        labels.mount(Label(user.get_name()))
        labels.mount(Label(f"Solde: {sum(user.get_transactions()[id].get_montant() for id in user.get_transactions())}"))
        


    def action_save_and_quit(self):
        global user
        if user != None:
            user.save_info()
        self.exit()


    def connect(self, username:str , pwd:str ,) -> None:
        """
        Method to connect the user to the app
        """
        # Calling global variables useful in the function
        global users, names,user
            # Check if the user exists
        if username in names:
            # Check if the password is correct
            if username + pwd in users:
                self.query_one("#login", Vertical).remove()
                self.second_page(username, pwd)
                

            else:
                self.try_pwd -= 1
                if self.try_pwd > 0:
                
                    messages = self.query_one("#errorMessage")
                    self.query_one("#pwd",Input).action_select_all()
                    self.query_one("#pwd",Input).action_end
                    if self.try_pwd == 1:
                        self.query_one(".invalid", Label).remove()
                    messages.mount(Label(f"Mot de passe erroné, il reste {self.try_pwd} tentatives pour le mot de passe.", classes = "invalid",))
                else:
                        messages = self.query_one("#login", Vertical).remove()
                        self.mount(Label("Entrée refusée",classes="invalid"))
                        
        elif self.query_one_optional("#mkuser") == None:
            
            messages = self.query_one("#errorMessage")
            butttonBox = self.query_one("#buttonBox")
            error_label = self.query_one_optional(".invalid", Label)
            if error_label != None :
                error_label.remove() 
            messages.mount(Label("Utilisateur inexistant. Voulez-vous créer cet utilisateur?",id="mkuser"))
            butttonBox.mount(Button("OUI",id="yes",))
            butttonBox.mount(Button("NON",id="no",))
    
                                


    # Methods related to the reaction to user's inputs
    async def on_input_submitted(self, event: Input.Submitted):
        """
        Method called by textual when the enter key is pushed on an input
        """
        # Get the information entred

        self.username, self.pwd = self.query_one("#user", Input), self.query_one("#pwd", Input)

        if((self.username.is_valid)==False ):
            self.username.border_title = "Sorry Username need to be longer than 5 characters"
            self.username.add_class("invalid",update=True)
        else:
            self.username.remove_class("invalid",update=True)
            self.username.border_title = ""

        if((self.pwd.is_valid)==False ):
            self.pwd.border_title = "Sorry Password need to be longer than 4 characters"
            self.pwd.add_class("invalid",update=True)
        else:
            self.pwd.remove_class("invalid",update=True)
            self.pwd.border_title = ""

        if((self.username.is_valid) and (self.pwd.is_valid)):
            self.connect(self.username.value, self.pwd.value)

    def on_button_pressed(self,event:Button.Pressed):
        button_pressed = event.button.id
        global users, names,user

        if(button_pressed == "yes"):
            new_user = User((self.query_one("#user").value),(self.query_one("#pwd").value))
            user = new_user
            fichier.add_object_binary("users_list", (self.query_one("#user").value) + (self.query_one("#pwd").value))
            fichier.add_object_binary("names", (self.query_one("#user").value))
            users.append((self.query_one("#user").value) + (self.query_one("#pwd").value))
            names.append(self.query_one("#user").value) 
            self.connect(self.query_one("#user").value,self.query_one("#pwd").value)
        elif(button_pressed == "no"):
            txt = self.query_one("#errorMessage")
            buttons = self.query_one("#buttonBox")
            for Label in txt.children:
                Label.remove()
            for button in buttons.children:
                button.remove()
            name = self.query_one("#user",Input)
            pwd = self.query_one("#pwd",Input)
            pwd.action_end()
            pwd.action_delete_left_all()
            name.action_end()
            name.action_delete_left_all()
            name.action_home()

            




"""
        # Get the wigets and input on the page
        page = self.query_one("#page", Vertical)
        inputs = self.query_one("#inputs", Horizontal)
        messages = self.query_one("#messages", Vertical)

        # Remove the messages
        await messages.remove_children()

        # Analyse the content present on the page
        if self.username and self.pwd:
            if self.username + self.pwd in users:
                self.query_one("#page", Vertical).remove()
                self.mount(Label("Bienvenue sur Finance Pro Max", id = "Budget")) # Label temporaire, ici, il faudra créer la page d'utilisation normale
            elif self.username in names:
                if self.try_pwd > 1:
                    self.try_pwd -= 1
                    messages.mount(Label(f"Mot de passe erroné, il reste {self.try_pwd} tentatives pour le mot de passe."))
                else:
                    messages.mount(Label("Entrée refusée"))
            else:
                 messages.mount(Vertical(Label("Voulez-vous créer cet utilisateur?"), Horizontal(Button("Oui"), Button("Non")), id = "Account_creation"))
        elif self.username:
            if self.username in names:
                messages.mount(Label("Utilisateur existant, vous aurez 3 tentatives pour le mot de passe"))
        else:
            messages.mount(Label("Entrez un nom d'utilisateur"))
               """ 

# Global variables
users:list = [] # Initializing the container for all users existant in te system
names:list = [] # List of usernames

def lauch_ui():
    """
    Method lauching the TUI app
    """
    app = Login()
    app.run()

# Testing environnement of the file
if __name__ == "__main__":
    app = Login()
    app.run()
