
 
"""
 Projet : Finances-Pro-Max
 Autheur : Thomas Raymond
 Author : Félix Roussin 
 Date : 20 avril 2026
 
 Description : Fonction qui ajoute des dépenses et des revenus
 
"""
import array as arr
import os
import platform
import time as t

 
def screen_clear():
     if(platform.system() != "Linux"):
         os.system('cls')
     else:
         os.system('clear')
 
class Transaction:
 
     def __init__(self):
         self.transaction = arr.array('d')

     def get_transaction(self):
        return self.transaction
        
     def get_solde(self):
         solde =0
         for montant in self.transaction:
             solde += montant
         return solde

     def get_historique_depot(self):
         return [montant for montant in self.get_transaction() if montant >= 0]
 
     def get_historique_retrait(self):
         return  [montant for montant in self.get_transaction() if montant < 0]
 
 
     def validation_montant(self,montant):
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
     
 
     def set_transaction(self,montant,genre):
         if self.validation_montant(montant):
             transaction = float(montant) if choix == "d" else (float(montant)*-1)
             self.transaction.append(transaction)
         else:
             print("Transaction non valide.")
             t.sleep(2)
     def __str__(self):
         return f"Votre solde est de : {self.get_solde()}$ \nVoulez-vous entrer une dépot ou un retrait? (d/r)\nQuitter: (q)"
 
if __name__ == "__main__":
     solde = 0
     transaction=Transaction()
     while(True):
         screen_clear()
         print(transaction.get_historique_depot())
         print(transaction.get_historique_retrait())
         print(transaction)
         choix = input("Entrez votre choix (d/r/q) : ")
         if choix == "d":
             transaction.set_transaction(input("Entrez votre dépot en dollars CAD : ",).replace(",","."),choix)
         elif choix == "r":
             transaction.set_transaction(input("Entrez votre retrait en dollars CAD : ").replace(",","."),choix)
         elif choix == "q":
             screen_clear()
             print("Votre solde est de : ",transaction.get_solde(),"$")
             break
         
             
 
