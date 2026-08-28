"""
 Projet : Finances-Pro-Max
 Directory : UI
 Name Of File : SimpleUi.py
 Author : Thomas Raymond
 Author : Félix Roussin 
 Date : 28 août 2026

Description : Simple TUI Handler, nothing crazy just the base. Also, there is actually a memory management here, but it should be moved
at another place.

"""


"""
Use to acces the class of the other files
"""

from API.User import User
import time as t
import API.Fichier as fichier
import subprocess
import platform
from getpass import getpass
import pickle


nom="" # Initializing username's variable for all functions
users=[] # Initializing the container for all names existant in te system
names=[] # List of usernames
info_users=None # Initializing the variable that'll be used for containing users complete connexion information
info_names=None # Initializing the variable that'll be used for containing username information

animation = [ # The animation is there to let the user process what is happening
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



def wait(second : int): 
    """
    Fonction printing the animation according to the waiting time passed in argument.
    """
    i = 0 
    while True:
        print(animation[i % len(animation)], end='\r')
        t.sleep(.1)
        i += 1
        if(i>second*17):
            break


def screen_clear()->None:
     """
     Function that cleans the screen using command prompt

     clc if your a windows user
     clear if you a Unix base user

     """
     if(platform.system() == "Windows"):
         _ = subprocess.call('cls', shell = True)
     else:
         _ = subprocess.call('clear', shell = True)

def choice_is_due() -> str:
     """
     Function returning the input when a choice between deposit and withdraw
     """
     return input("Vous pouvez:\nDéposer, Retirer, Quitter ou Modifier une transaction\nEntrez votre choix (d/r/q/m) : ")

def open_session(name,pwd):
    """
    Basic configuration to handle the display. A simple Textbase User Interface(TUI)
    """
    global users, names
    if name+pwd in users:
        screen_clear()
        print("Log in :")
        wait(1)
        return True
    elif name in names:
         print("Mauvais mot de passe.\nVeuillez essayer à nouveau.")
         wait(1)
         return False
    else:
        while True:
            print(f"Voulez-vous créer ce compte avec ce mot de passe et ce nom d'utilisateur?(Y,N) : ")
            choice = input()
            if choice.lower() == "y":
                screen_clear()
                print(f"Création du compte")
                wait(1)
                User(name,pwd)
                fichier.add_object_binary("users_list", name+pwd)
                fichier.add_object_binary("names", name)
                return True
            elif choice.lower()=="n":
                screen_clear()
                print("Retour à la connexion.")
                wait(1)
                return False 
            else:
                screen_clear()
                print("Votre réponse doit être oui(y) ou non(n).")
                print(f"Votre choix: «{choice}» n'est pas valide.")
                wait(1)
                screen_clear()
                continue
            
def get_username():
    """
    Function to handle what the user enters to assure there was not mistakes with what the user typed.
    """

    global users, info_users, nom

    # Initialize classes
    while True:
        screen_clear()
        print("Bienvenue sur Finance Pro Max!")
        name: str = input("Quel est votre nom d'utilisateur : ")
        nom = name
        if(len(nom)>0):
            if nom in users:
                screen_clear()
                print("Utilisateur existant.")
                print("Vous aurez trois tentatives pour le mot de passe.")
                wait(1)
                return nom
            else:
                return nom
        else:
            continue

def get_password(nom):
    """
    Function to get the user's password.
    """
    while True:        
            screen_clear()
            print("Bienvenue sur Finance Pro Max!")
            print(f"Nom d'utilisateur: {nom}")
            pwd : str = getpass("Mot de passe : ", echo_char="*")
            password=str(pwd)
            if(len(pwd)>0):
                return password
            else:
                continue
    
def simple_ui()->None:
    # Calling global variables useful in the function
    global users, names, info_users, info_names

    # Create the user variable for pylance to unserstand it exist when called in the isistance in the while loop later on.
    user = None

    # Reading users et usernames files to be able to verify in the inputs corresponds to an exxisting user
    info_users=fichier.read_content("users_list")
    info_names=fichier.read_content("names")

    # Decode binary information and set variables
    if info_users==None:
        users=[]
    else:
        users.append(pickle.loads(info_users))

    if info_names==None:
        names=[]
    else:
        names.append(pickle.loads(info_names))

    tentatives_password=0
    while True:
        name=get_username()
        while True:
            password=get_password(name)
            if(open_session(name,password)):
                    user=User(name,password)
                    break
            tentatives_password+=1
            if tentatives_password==3:
                screen_clear()
                print("Pour des raisons de cybersécurité, votre entrée a été interdite.")
                wait(3)
                break
            elif name in names:
                continue
            else:
                name=get_username()
    
        # Main loop that display the app
        #while user_validation:7
        while isinstance(user, User):
            # Save user's information each modification
            user.save_info()
            # Clean the screen
            screen_clear()
            if(user.print_historic() != ""):
                # Dislpay historic
                print(user.print_historic())
                  
            # Display the solde
            print(user)

            # User makes his choice
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
                print("Non Valide.")
                wait(1)
                continue
        break


