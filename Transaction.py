
 
"""
 Projet : Finances-Pro-Max
 Author : Thomas Raymond
 Author : Félix Roussin 
 Date : 21 avril 2026
 
Description : Fonction utilisable à partir du terminal qui permet à l'utilisateur de rentrer des dépenses et des revenus et d'enregistrer
son solde.
 
"""
import array as arr
import os
import platform
import time as t
from typing import Any


def screen_clear()->None:
     if(platform.system() != "Linux"):
         os.system('cls')
     else:
         os.system('clear')
 
class Transaction:
 
     def __init__(self) -> None:
         self.transaction = arr.array('d')

     def get_transaction(self) -> arr.array:
        return self.transaction
        
     def get_solde(self) -> float:
         solde = 0
         for montant in self.transaction:
             solde += montant
         return solde

     def get_historique_depot(self)-> list[float]:
         return [montant for montant in self.get_transaction() if montant >= 0]
 
     def get_historique_retrait(self) -> list[float]:
         return  [montant for montant in self.get_transaction() if montant < 0]
 
 
     def validation_montant(self,montant) -> bool:
         try:
             montant=float(montant)
         except ValueError:
             print("Saisie invalide.")
             t.sleep(1)
             return False
         if montant>0:
             return True
         else:
             print("Le nombre n'est pas positif.")
             t.sleep(1)
         return False
     
 
     def set_transaction(self,montant,choix) -> None:
         if self.validation_montant(montant):
             transaction = float(montant) if choix == "d" else (float(montant)*-1)
             self.transaction.append(transaction)
         else:
             print("Transaction non valide.")
             t.sleep(2)
     def __str__(self) -> str:
        solde=self.get_solde()
        if solde < 0:
            return f"Votre solde est de : {"\033[91m"}{solde:.2f}{"\033[0m"}$ \nVoulez-vous entrer une dépot ou un retrait? (d/r)\nQuitter: (q)"
        return f"Votre solde est de : {solde:.2f}$ \nVoulez-vous entrer une dépot ou un retrait? (d/r)\nQuitter: (q)"
     
if __name__ == "__main__":
    solde = 0
    transaction=Transaction()
    historique_depot={}
    past_lenght_liste_depot=0
    historique_retrait={}
    past_lenght_liste_retrait=0
    while(True):
        screen_clear()
        liste_retrait=transaction.get_historique_retrait()
        liste_depot=transaction.get_historique_depot()
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
        print(transaction)
        choix = input("Entrez votre choix (d/r/q) : ")
        if choix == "d":
            transaction.set_transaction(input("Entrez votre dépot en dollars CAD : ",).replace(",","."),choix)
        elif choix == "r":
            transaction.set_transaction(input("Entrez votre retrait en dollars CAD : ").replace(",","."),choix)
        elif choix == "q":
            screen_clear()
            solde=transaction.get_solde()
            if solde<0:
                print(f"Votre solde est de: {"\033[91m"}{solde:.2f}{"\033[0m"} $")
            else:
                print(f"Votre solde est de: {solde:.2f}$")
            break
         
             
 
