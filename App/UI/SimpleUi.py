"""
 Projet : Finances-Pro-Max
 Directory : UI
 Name Of File : SimpleUi.py
 Author : Thomas Raymond
 Author : Félix Roussin 
 Date : 21 avril 2026

Description : Simple TUI Handler nothing crazy just the base 

"""


"""
Use to acces the class of the other files
"""
from API.Transaction import Transaction 
import time as t
import os
import platform
"""
Method that clean the screen using command prompt

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
Basic configuration for endeling display. So a simple Textbase User Interface(TUI)
"""
    
    
def simple_ui()->None: 
     transaction=Transaction()
    #initialize basic variable
     historique_depot : list(float) = {}
     past_lenght_liste_depot : int = 0
     historique_retrait: list(float) = {}
     past_lenght_liste_retrait: int = 0
    #main loop that displayu the app
     while(True):
         #clean the screen
         screen_clear()
         #get the array of the historic for both
         liste_retrait=transaction.get_historique_retrait()
         liste_depot=transaction.get_historique_depot()
         #find if needed to be showned
         if len(liste_depot)!=0:
             if len(liste_depot)>past_lenght_liste_depot:
                 historique_depot[liste_depot[len(liste_depot)-1]]=f"{t.localtime()[2]}/{t.localtime()[1]:02.0f}/{t.localtime()[0]:02.0f} à {t.localtime()[3]:02.0f}:{t.localtime()[4]:02.0f}:{t.localtime()[5]:02.0f}"
                 past_lenght_liste_depot+=1
             print("Historique des dépôts:")
             for element in historique_depot:
                 print(f"{element:.2f}: {historique_depot[element]}")
             print()
         if len(liste_retrait)!=0:
             if len(liste_retrait)>past_lenght_liste_retrait:
                 historique_retrait[liste_retrait[len(liste_retrait)-1]]=f"{t.localtime()[2]}/{t.localtime()[1]:02.0f}/{t.localtime()[0]:02.0f} à {t.localtime()[3]:02.0f}:{t.localtime()[4]:02.0f}:{t.localtime()[5]:02.0f}"
                 past_lenght_liste_retrait+=1
             print("Historique des retraits:")
             for element in historique_retrait:
                 print(f"{element:.2f}: {historique_retrait[element]}")
             print()
         #display the solde
         print(transaction)
         #User make is is choice
         choix = choice_is_due()       
         if choix == "d":
             #add transaction categorize as deposit
             transaction.set_transaction(input("Entrez votre dépot en dollars CAD : ",).replace(",","."),choix)
         elif choix == "r":
             #add transaction categorize as withdrew
             transaction.set_transaction(input("Entrez votre retrait en dollars CAD : ").replace(",","."),choix)
         elif choix == "q":
             #clear the screen show the solde and end the app
             screen_clear()
             solde=transaction.get_solde()
             if solde<0:
                 print(f"Votre solde est de: {"\033[91m"}{solde:.2f}{"\033[0m"} $")
             else:
                 print(f"Votre solde est de: {solde:.2f}$")
             break
         #Error if the letter is not take in charge
         else:
             print("Non Valide.")
             t.sleep(1)


