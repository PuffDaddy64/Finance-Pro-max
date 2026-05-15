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

def open_session(name):
    content : bool = fichier.file_exist(name)
    if(content):
        return True
    else:
        print(f"File dont exist do you want to create one whit this Username?(Y,N) : ")
        choice = input()
        if( choice == "y" or choice ==  "Y"):
            fichier.write_object_binary(name,None)
            return True
        else:
            screen_clear()
            print("Back to log in then.")
            t.sleep(1)
            return False 
            

    
    
def simple_ui()->None:
    # Initialize classes
    while(True):
        screen_clear()
        name :str = input("What is your username : ")
        if(open_session(name)):
            user=User(name)
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
             t.sleep(1)


