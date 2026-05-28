"""
 Projet : Finances-Pro-Max
 Directory : UI
 Name Of File : SimpleUi.py
 Author : Thomas Raymond
 Author : Félix Roussin 
 Date : 5 mai 2026

Description : Simple TUI Handler nothing crazy just the base. Also, there is actually a memory mangement here, but it should be moved
at another place.

"""


"""
Use to acces the class of the other files
"""
from API.Transaction import Transaction 
from API.User import User
import time as t
import API.Fichier as fichier
import os
import platform
import struct
from getpass import getpass
import hashlib




animation = [
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
    i = 0 
    while True:
        print(animation[i % len(animation)], end='\r')
        t.sleep(.1)
        i += 1
        if(i>second*17):
            break





"""
Method that cleans the screen using command prompt

    clc if your a windows user
    clear if you a Unix base user

"""
def screen_clear()->None:
     if(platform.system() == "Windows"):
         os.system('cls')
     else:
         os.system('clear')

def choice_is_due() -> str:
     return input("Vous pouvez:\nDéposer, Retirer, Quitter\nEntrez votre choix (d/r/q) : ")

"""
Basic configuration for endeling display. So a simple Textbase User Interface(TUI)0
"""

def open_session(name,pwd):
    if(User(name,pwd).get_solde()!=[]):
        screen_clear()
        print("Log in .")
        wait(1)
        return True
    else:
        print(f"File dont exist do you want to create one whit this Username?(Y,N) : ")
        choice = input()
        if( choice == "y" or choice ==  "Y"):
            screen_clear()
            print(f"Creating the account")
            wait(1)
            User(name,pwd)
            return True
        else:
            screen_clear()
            print("Back to log in then.")
            wait(1)
            return False 
            

    
    
def simple_ui()->None:
    # Initialize classes
    while(True):
        screen_clear()
        while True:
            name :str = input("What is your username : ")
            if(len(name)>0):
                break
            else:
                print(f"Need more than one digit.")

        while True:        
            pwd : str = getpass("Password : ")
            if(len(pwd)>0):
                break
            else:
                print(f"Need more than one digit.")
        if(open_session(name,pwd)):
            user=User(name,pwd)
            break

    # Main loop that display the app
    while(True):
         #clean the screen
         #clean the screen
         screen_clear()
         if(user.print_historic() != ""):
            print(user.print_historic())
        
         #dislpay historic
         
         #display the solde
         print(user)
         #User make is is choice
         choix = choice_is_due()  
         if choix == "d" or choix == "r":  
            #add transaction 
            user.add_transaction(input("Entrez votre dépot en dollars CAD : ",).replace(",","."),choix)
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


