"""
 Projet : Finances-Pro-Max
 Directory : UI
 Name Of File : SimpleUi.py
 Author : Thomas Raymond
 Author : Félix Roussin 
 Date : 2 mai 2026

Description : Simple TUI Handler nothing crazy just the base 

"""


"""
Use to acces the class of the other files
"""
from API.Transaction import Transaction 
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

def memory(file_name,binary_infos):
    """
    Function opens a binary file in write mode to overwrite it and then add the new informations that
    came in an argument.
    """
    memory_file=open(file_name,"wb") # Overwrite the file
    memory_file.close()
    memory_file=open(file_name,"ab")
    for element in binary_infos:
        memory_file.write(element)
    memory_file.close()
    
"""
Basic configuration for endeling display. So a simple Textbase User Interface(TUI)0
"""
    
    
def simple_ui()->None: 
    transaction=Transaction()
    #initialize basic variable
    historique_depot : list(float) = {}
    past_lenght_liste_depot : int = 0
    historique_retrait: list(float) = {}
    past_lenght_liste_retrait: int = 0
    
    try:
        memory_depot_file=open("memory_depot_file.bin","xb")
        liste_pour_binaire_depot=[]
    except FileExistsError:
        memory_depot_file=open("memory_depot_file.bin","rb")
        liste_pour_binaire_depot=[]
        contenu=memory_depot_file.readline() # Read the information
        liste_pour_binaire_depot.append(contenu) # Store it

    try:
        memory_retrait_file=open("memory_retrait_file.bin","xb")
        liste_pour_binaire_retrait=[]
    except FileExistsError:
        memory_retrait_file=open("memory_retrait_file.bin","rb")
        liste_pour_binaire_retrait=[]
        contenu=memory_retrait_file.readline()
        liste_pour_binaire_retrait.append(contenu)

    # close both files to avoid modify them by mistake
    memory_depot_file.close()
    memory_retrait_file.close()

    # Main loop that display the app
    while(True):
         #clean the screen
         screen_clear()

         #get the array of the historic for both
         liste_retrait=transaction.get_historique_retrait()
         liste_depot=transaction.get_historique_depot()

         #find if needed to be showned
         if (len(liste_pour_binaire_depot) !=0 or len(liste_depot) !=0):
            if len(liste_depot)>past_lenght_liste_depot:
                
                # Store time informations
                moment=t.localtime()
                day, month, year, hour, minute, second, money = moment[2], moment[1], moment[0], moment[3], moment[4], moment[5], liste_depot[len(liste_depot)-1]
                
                # Next code line contains a struct.pack following the data format of a class transaction. It is like a struct in C++ but the python version
                liste_pour_binaire_depot.append(struct.pack(transaction.information_format(), day, month, year, hour, minute, second, money))

                # Printing informations
                historique_depot[f"{day}/{month}/{year} à {hour}:{minute}:{second}"]=liste_depot[len(liste_depot)-1]
                past_lenght_liste_depot+=1

            # Next sequence is used to read elements stored in liste_pour_binaire_depot
            print("Historique des dépôts:")
            for position in range(len(liste_pour_binaire_depot)):
                lenght_structure=struct.calcsize(transaction.information_format()) # Storing the numbers of bytes a struct should contain
                if position==0: # the first element contains all the structs that were previously stored before the user started this session
                    offset=0
                    while offset<len(liste_pour_binaire_depot[position]):
                        # Putting back the information in its original format
                        information=struct.unpack_from(transaction.information_format(), liste_pour_binaire_depot[position], offset)
                        offset+=lenght_structure
                        print(f"{str(information[0]).zfill(2)}/{str(information[1]).zfill(2)}/{str(information[2]).zfill(2)} à {str(information[3]).zfill(2)}:{str(information[4]).zfill(2)}:{str(information[5]).zfill(2)} : {information[6]:.2f}$")
                else:
                    # Here is the unpacking for the elements added in this session
                    information=struct.unpack_from(transaction.information_format(), liste_pour_binaire_depot[position])
                    print(f"{str(information[0]).zfill(2)}/{str(information[1]).zfill(2)}/{str(information[2]).zfill(2)} à {str(information[3]).zfill(2)}:{str(information[4]).zfill(2)}:{str(information[5]).zfill(2)} : {information[6]:.2f}$")
            print()
        # Same process as for depot (maybe putting it in a function would be a good idea)
         if (len(liste_pour_binaire_retrait) !=0 or len(liste_retrait)!=0):
            if len(liste_retrait)>past_lenght_liste_retrait:
                moment=t.localtime()
                day, month, year, hour, minute, second, money = moment[2], moment[1], moment[0], moment[3], moment[4], moment[5], liste_retrait[len(liste_retrait)-1]
            
                liste_pour_binaire_retrait.append(struct.pack(transaction.information_format(), day, month, year, hour, minute, second, money))
                historique_retrait[f"{day}/{month}/{year} à {hour}:{minute}:{second}"]=money
                past_lenght_liste_retrait+=1
            print("Historique des retraits:")
            for position in range(len(liste_pour_binaire_retrait)):
                lenght_structure=struct.calcsize(transaction.information_format())
                if position==0:
                    offset=0
                    while offset<len(liste_pour_binaire_retrait[position]):
                        information=struct.unpack_from(transaction.information_format(), liste_pour_binaire_retrait[position], offset)
                        offset+=lenght_structure
                        print(f"{str(information[0]).zfill(2)}/{str(information[1]).zfill(2)}/{str(information[2]).zfill(2)} à {str(information[3]).zfill(2)}:{str(information[4]).zfill(2)}:{str(information[5]).zfill(2)} : {information[6]:.2f}$")
                else:
                    information=struct.unpack_from(transaction.information_format(), liste_pour_binaire_retrait[position])
                    print(f"{str(information[0]).zfill(2)}/{str(information[1]).zfill(2)}/{str(information[2]).zfill(2)} à {str(information[3]).zfill(2)}:{str(information[4]).zfill(2)}:{str(information[5]).zfill(2)} : {information[6]:.2f}$")
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

            # Calling the function to write the new binary files
            memory("memory_depot_file.bin", liste_pour_binaire_depot)
            memory("memory_retrait_file.bin", liste_pour_binaire_retrait)
            break
         #Error if the letter is not take in charge
         else:
             print("Non Valide.")
             t.sleep(1)


