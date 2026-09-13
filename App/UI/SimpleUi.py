"""
 Projet : Finances-Pro-Max
 Directory : UI
 Name Of File : SimpleUi.py
 Author : Thomas Raymond
 Author : Félix Roussin 
 Date : 5 septembre 2026

Description : Simple TUI Handler, nothing crazy, just the base. Also, there is actually a memory management here, but it should be moved at another place.
"""

from API.User import User
import time as t
import API.Fichier as fichier
import subprocess
import platform
from getpass import getpass
import pickle

# Global variables
users:list = [] # Initializing the container for all users existant in te system
names:list = [] # List of usernames
animation:list = [ # The animation is there to let the user process what is happening
"[        ]",
"[=       ]",
"[===     ]",
"[====    ]",
"[=====   ]",
"[======  ]",
"[======= ]",
"[========]",
"[ =======]",
"[  ======]",
"[   =====]",
"[    ====]",
"[     ===]",
"[      ==]",
"[       =]",
"[        ]",
"[        ]"
]

# Functions related to the printing in the terminal
def wait(second: int) -> None: 
    """
    Fonction printing the animation according to the waiting time passed in argument.
    """
    i:int = 0 
    while True:
        print(animation[i % len(animation)], end='\r')
        t.sleep(.1)
        i += 1
        if i > second * 17:
            break

def screen_clear() -> None:
     """
     Function that cleans the screen using command prompt

     clc if you're a windows user
     clear if you're a Unix base user

     """
     if(platform.system() == "Windows"):
         _ = subprocess.call('cls', shell = True)
     else:
         _ = subprocess.call('clear', shell = True)

# Function related to the choices made by the user
def choice_is_due() -> str:
     """
     Function returning the input when an action is needed
     """
     return input("Vous pouvez:\nDéposer, Retirer, Modifier une transaction, Quitter\nEntrez votre choix (d/r/m/q): ")

# Function related to acquiring the user's information
def open_session(name:str, pwd:str) -> bool:
    """
    Function to open the session
    """
    # Obtaining global variables
    global users, names

    # Validating the existence of the user
    if name + pwd in users:
        screen_clear()
        print("Log in :")
        wait(1)
        return True

    # Validating if the username is correct to manage password errors
    elif name in names:
         print("Mauvais mot de passe.\nVeuillez essayer à nouveau.")
         wait(1)
         return False

    # Asking the user if he wants to create an account
    else:
        while True:
            choice:str = input(f"Voulez-vous créer ce compte avec ce mot de passe et ce nom d'utilisateur?(Y,N): ")

            # Create the account
            if choice.lower() == "y":
                screen_clear()
                print(f"Création du compte")
                wait(1)
                User(name,pwd)
                fichier.add_object_binary("users_list", name + pwd)
                fichier.add_object_binary("names", name)
                return True

            # Getting back to login
            elif choice.lower() == "n":
                screen_clear()
                print("Retour à la connexion.")
                wait(1)
                return False 

            # Error management
            else:
                screen_clear()
                print("Votre réponse doit être oui(y) ou non(n).")
                wait(1)
                screen_clear()
                continue
            
def get_username() -> str:
    """
    Function to obtain user's username
    """
    # Obtening global variables
    global names

    # Obtaining the username
    while True:
        screen_clear()
        print("Bienvenue sur Finance Pro Max!")
        name:str = input("Quel est votre nom d'utilisateur : ")
        if len(name) > 0:
            if name in names:
                screen_clear()
                print("Utilisateur existant.")
                print("Vous aurez trois tentatives pour le mot de passe.")
                wait(1)
                return name
            else:
                return name
        else:
            continue

def get_password(nom:str) -> str:
    """
    Function to get the user's password.
    """
    while True:        
            screen_clear()
            print("Bienvenue sur Finance Pro Max!")
            print(f"Nom d'utilisateur: {nom}")
            pwd:str = getpass("Mot de passe : ", echo_char="*")
            if len(pwd) > 0:
                return pwd
            else:
                continue

# Function related of the UI mangement
def simple_ui() -> None:
    """
    Basic configuration to handle the display. A simple Textbase User Interface(TUI)
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

    # Section related to obtaining the user's login informations
    user:User|None = None # Create the user variable for pylance to unserstand it exist when called in the isistance in the while loop later on.
    tentatives_password:int = 1
    username:str = get_username()
    while True:
        password:str = get_password(username)
        if(open_session(username, password)):
            user = User(username, password)
            break
        elif tentatives_password == 3:
            screen_clear()
            print("Pour des raisons de cybersécurité, votre entrée a été interdite.")
            wait(3)
            break
        elif username in names:
            tentatives_password += 1
            continue
        else:
            username = get_username()
    
    # Main loop that display the app
    while isinstance(user, User):
        # Save user's information each modification
        user.save_info()

        # Clean the screen
        screen_clear()

        # Dislpay historic
        if(user.print_historic() != ""):
            print(user.print_historic())
                  
        # Display the solde
        print(user)

        # Choice management
        choix = choice_is_due()
        if choix == "m":
            if len(user.get_transactions().keys()) != 0:
                screen_clear()
                print(user.print_historic())
                id_to_modify = input(f"\nEntrez l'ID({min(user.transactions.keys())} à {max(user.transactions.keys())}) de la transaction que vous souhaitez modifier: ")
                while not user.validation_id_transaction(id_to_modify):
                    id_to_modify = input(f"Entrez l'ID({min(user.transactions.keys())} à {max(user.transactions.keys())}) de la transaction que vous souhaitez modifier: ")
                screen_clear()
                transaction_to_modify = user.get_transaction(int(id_to_modify))
                transaction_to_modify.print(user.column_format)
                transaction_to_modify.modify()
            else:
                print("Vous n'avez pas de transactions actuellement.")
                t.sleep(1)
                continue
               
        elif choix == "d":  
            #add transaction 
            user.add_transaction(input("Entrez votre dépot en dollars CAD : ",).replace(",","."),choix, input("Entrez le type de transaction: "))
            continue
        elif choix == "r":
            #add transaction 
            user.add_transaction(input("Entrez votre retrait en dollars CAD : ",).replace(",","."),choix, input("Entrez le type de transaction: "))
            continue
        elif(choix == "q"):
            #clear the screen show the solde and end the app
            screen_clear()
            print(user)
            # Calling the function to write the new binary files
            user.save_info()
            break
        #Error if the letter is not take in charge
        else:
            print("Entrée non valide.")
            wait(1)
            continue


