
 
"""
 Projet : Finances-Pro-Max
 Directory : API
 Name Of File : Transaction.py
 Author : Thomas Raymond
 Author : Félix Roussin 
 Date : 5 mai 2026
 
Description  : Class for the transaction handling with deposit and withdrew
                The Class is call from the frontend (UI) for displaying info.
"""
import array as arr
import time as t
from typing import Any

 
class Transaction:

    def __init__(self) -> None:
         """
         Method that is call a constructor and initialize value for the object first 
         """ 
         self.transaction = arr.array('d')

    def information_format(self): 
         return "B B H B B B d" # B = 1 byte unsigned ; H = 2 bytes unsigned ; d = double float signed (4 bytes). So 7 bytes total

    def get_transaction(self) -> arr.array:
        return self.transaction

    def get_solde(self) -> float:
         solde = 0
         for montant in self.transaction:
             solde += montant
         return solde

    """
     Valid the new montant before its added to the array of transaction
    """
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

    """
    Method that get call when the object is parameter of a print() so the look of an opbject
    """
    def __str__(self) -> str:
        solde=self.get_solde()
        if solde < 0:
            return f"Votre solde est de : {"\033[91m"}{solde:.2f}{"\033[0m"}$ \n"
        return f"Votre solde est de : {solde:.2f}$ \n"
     
         
             
 
