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
from textual import on
from textual.app import App,ComposeResult
from textual.containers import Container, Horizontal,Vertical
from textual.widgets import Header, Footer, Button, Input, Label,Pretty
from textual.validation import Length, Validator

# Import from SimpleUI which is the old UI
from API.User import User
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


    #BINDINGS[] # I dont't know what it is...
    
    # Methods related to the App apperance
    def compose(self) -> ComposeResult:
        """
        Method related to the lauch of the App
        """
        # Calling global variables useful in the function
        global users, names
        
        # Reading users et usernames files to be able to verify in the inputs corresponds to an exxisting user
        info_users = fichier.read_content("users_list")
        info_names = fichier.read_content("names")
        
        # Decode binary information and update variables
        if info_users is not None: # Update all users present
            users.append(pickle.loads(info_users))
        if info_names is not None: # update all usernames present
            names.append(pickle.loads(info_names))

        # Lauches the main features
        yield Vertical(Label("$$$$$$$\\  $$\\   $$\\ $$$$$$$\\   $$$$$$\\  $$$$$$$$\\ $$$$$$$$\\ \n$$  __$$\\ $$ |  $$ |$$  __$$\\ $$  __$$\\ $$  _____|\\__$$  __|\n$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ /  \\__|$$ |         $$ |\n$$$$$$$\\ |$$ |  $$ |$$ |  $$ |$$ |$$$$\\ $$$$$\\       $$ |\n$$  __$$\\ $$ |  $$ |$$ |  $$ |$$ |\\_$$ |$$  __|      $$ |\n$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |         $$ |\n$$$$$$$  |\\$$$$$$  |$$$$$$$  |\\$$$$$$  |$$$$$$$$\\    $$ |\n\\_______/  \\______/ \\_______/  \\______/ \\________|   \\__|", id = "title"),Horizontal(
                  Container(
                        Input(
                            id="user",
                             ),
                        
                    ), 
                  Container(
                    Input(id="pwd",
                        password=True,),
                    
                    ), 
                id = "inputs"),
        Vertical(id = "messages"), id = "page")


    def on_mount(self)-> None:
        """
        Method called when a mount function is called
        """
        # Username
        inputUsername = self.query_one('#user', Input) 
        inputUsername.border_subtitle = "Username"

        # Password
        inputPassword = self.query_one('#pwd', Input) 
        inputPassword.border_subtitle = "Password"

    # Methods related to the reaction to user's inputs
    async def on_input_submitted(self, event: Input.Submitted):
        """
        Method called by textual when the enter key is pushed on an input
        """
        # Get the information entred
        self.username, self.pwd = self.query_one("#user", Input).value, self.query_one("#pwd", Input).value

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
