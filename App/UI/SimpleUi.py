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

def write_memory_file(file_name,binary_infos):
    """
    Function opens a binary file in append mode to add the new informations that
    came in an argument.
    """
    memory_file=open(file_name,"ab")
    for element_pos in range(len(binary_infos)):
         if element_pos!=0:
            memory_file.write(binary_infos[element_pos])
    memory_file.close()
def store_transaction_information(liste_pour_binaire, transaction_type):
    # Store time informations
    moment=t.localtime()
    day, month, year, hour, minute, second, money = moment[2], moment[1], moment[0], moment[3], moment[4], moment[5], struct.unpack(Transaction().information_format(), liste_pour_binaire[len(liste_pour_binaire)-1])
                
    if transaction_type=="depot":
        User().set_depot_historic(day, month, year, hour, minute, second, money)
    else:
        User().set_retrait_historic(day, month, year, hour, minute, second, money)

def print_historic(liste_pour_binaire,transaction_type, past_lenght_new_element_list):
    if len(liste_pour_binaire) !=0:
        if (len(liste_pour_binaire)-1)>past_lenght_new_element_list:
            if transaction_type=="depot":
                liste_pour_binaire=User().depot_memory
            else:
                liste_pour_binaire=User().retrait_memory
            past_lenght_new_element_list+=1

        # Next sequence is used to read elements stored in liste_pour_binaire_depot
        if transaction_type=="depot":
            print("Historique des dépôts:")
        else:
            print("Historique des retraits:")
        for position in range(len(liste_pour_binaire)):
            lenght_structure=struct.calcsize(Transaction().information_format()) # Storing the numbers of bytes a struct should contain
            if position==0: # the first element contains all the structs that were previously stored before the user started this session
                offset=0
                while offset<len(liste_pour_binaire[position]):
                    # Putting back the information in its original format
                    information=struct.unpack_from(Transaction().information_format(), liste_pour_binaire[position], offset)
                    offset+=lenght_structure
                    print(f"{str(information[0]).zfill(2)}/{str(information[1]).zfill(2)}/{str(information[2]).zfill(2)} à {str(information[3]).zfill(2)}:{str(information[4]).zfill(2)}:{str(information[5]).zfill(2)} : {information[6]:.2f}$")
            else:
                # Here is the unpacking for the elements added in this session
                information=struct.unpack_from(Transaction().information_format(), liste_pour_binaire[position])
                print(f"{str(information[0]).zfill(2)}/{str(information[1]).zfill(2)}/{str(information[2]).zfill(2)} à {str(information[3]).zfill(2)}:{str(information[4]).zfill(2)}:{str(information[5]).zfill(2)} : {information[6]:.2f}$")
        print()
    return True
    
"""
Basic configuration for endeling display. So a simple Textbase User Interface(TUI)0
"""
    
    
def simple_ui()->None:
    # Initialize classes
    transaction=Transaction()
    user=User()

    # Main loop that display the app
    while(True):
         #clean the screen
         screen_clear()

         #initialize basic variable
         depot_historic=user.depot_memory
         retrait_historic=user.retrait_memory

         past_lenght_liste_depot=len(depot_historic)-1
         past_lenght_liste_retrait=len(retrait_historic)-1

         # Print historics
         print_historic(depot_historic,"depot", past_lenght_liste_depot)
         print_historic(retrait_historic,"retrait", past_lenght_liste_retrait)
         
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

            # Calling the function to write the new binary files
            write_memory_file("memory_depot_file.bin", depot_historic)
            write_memory_file("memory_retrait_file.bin", retrait_historic)
            break
         #Error if the letter is not take in charge
         else:
             print("Non Valide.")
             t.sleep(1)


