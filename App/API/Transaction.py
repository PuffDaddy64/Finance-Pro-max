 
"""
 Project : Finances-Pro-Max
 Directory : API
 Name Of File : Transaction.py
 Author : Thomas Raymond
 Author : Félix Roussin 
 Date : 27 août 2026
 
Description  : Class describing a transaction.
               The class is called from the User module to manage the information related to a particular transaction.
"""

import time as t
import datetime

class Transaction:
    def __init__(self, choix:str, id:int, raison:str, montant:str) -> None:
         """
             Initialize values
         """ 
         self.id:int = id
         self.set_raison(raison = raison)
         self.set_montant(montant, choix)
         self.set_date()

 # Methods related to the id
    # The ID does not have a set method in the transaction module because it is set by the user because of the need of a memory controlled by the user.

    def get_id(self):
        """
        Method returning the ID of the transaction
        """
        return self.id

    # The ID does not have a modify method because the ID needs to be auto generated for the program to work correctly.

# Methods related to the reason of the transaction
    def validation_raison(self, raison:str) -> bool:
        """
        Method validating the reason of the transaction
        """
        if len(raison) == 0:
            print("Vous n'avez pas entré de raison pour votre transaction.")
            self.raison_valide = False
            t.sleep(1)
            return False
        self.raison_valide = True
        return True
    
    def set_raison(self, raison: str) -> None:
        """
        Method setting the reason of the transaction
        """
        if self.validation_raison(raison = raison):
             self.raison: str = raison
    
    def get_raison(self) -> str:
        """
        Method that returns the class variable raison_transaction.
        """
        return self.raison

    def modify_raison(self, new_reason:str) -> None:
        """
        Method modifying the reason of a transaction
        """
        self.raison = new_reason

# Methods related to the amount of the transaction
    def validation_montant(self, montant_entre:str) -> bool:
         """
             Validates the new amount (montant_entre) before it's added to the array of transaction
         """
         # Valider si le montant entré est un nombre
         try:
             montant:float = float(montant_entre)
         except ValueError:
             print("Le montant doit être un nombre.")
             t.sleep(1)
             self.montant_valide:bool = False
             return False

         # Valider si le montant entré est positif
         if montant > 0:
             self.montant_valide:bool = True
             return True
         else:
             print("Le nombre doit être supérieur à 0.")
             if montant < 0:
                print("Le sytème s'occupe lui-même de gérer le concept l'ajout ou la soustraction du nombre.")
             t.sleep(1)
         self.montant_valide:bool = False
         return False

    def set_montant(self, montant:str, choix:str) -> None:
         """
         Method setting the value of the amount of the transaction.
         """    
         if self.validation_montant(montant):
             self.montant : float = float(montant) if choix == "d" else (float(montant) * -1)
         else:
             print("Le montant n'est pas valide.")
             t.sleep(2)

    def get_montant(self):
        """
            Method tat returns the amount (montant)
        """
        return self.montant

    def modify_montant(self, new_montant:float) -> None:
        self.montant = new_montant

 # Methods related to the date ofthe transaction
    def set_date(self) -> None:
        self.date:datetime.date = datetime.datetime.now().date()

    def get_date(self) -> datetime.date:
        """
            Method that returns the date
        """
        return self.date

    def validation_year(self, new_year:str) -> bool:
        try:
            year = int(new_year)
        except ValueError:
            print(f"La valeur entrée pour l'année n'est pas un nombre.")
            return False
        if year < 0 and year <= 9999: # Le 9999 provient d'une contrainte datetime.date
            print(f"Veuillez entrer une année supérieure à 0")
            return False
        return True

    def validation_month(self, new_month:str) -> bool:
            try:
                month = int(new_month)
            except ValueError:
                print(f"La valeur entrée pour le mois n'est pas un nombre.")
                return False
            if month < 1 or month > 12:
                print(f"Veuillez entrer un mois de 1 à 12")
                return False
            return True

    def validation_day(self, new_day:str) -> bool:
        try:
            day = int(new_day)
        except ValueError:
            print(f"La valeur entrée pour le jour n'est pas un nombre.")
            t.sleep(1)
            return False
        if day < 1 or day > 31:
            print(f"Veuillez entrer un jour de 1 à 31")
            t.sleep(1)
            return False
        return True

    def modify_date(self, new_year:int, new_month:int, new_day:int) -> None:
        self.date = datetime.date(year = int(new_year), month = int(new_month), day = int(new_day))

# Methods related to the transaction type
    def get_type(self) -> str:
        """
        Method acquiring the type of the transaction (Deposit(d) or Withdraw(r))
        """
        if self.get_montant() > 0:
            return "d"
        else:
            return "r"

    def modify_type(self, new_type:str) -> None:
        """
        Method to modify the type of a transaction
        """
        if new_type == "d" and self.get_type() == "r":
            self.montant *= -1
        elif new_type == "r" and self.get_type() == "d":
            self.montant *= -1
 
    # Method regrouping the completion of a validation
    def valid_transaction(self):
        """
        Method regrouping the completion of a validation
        """
        if self.montant_valide and self.raison_valide:
            return True
        return False

    # Method related to the printing of a transaction
    def print(self, format) -> None:
        """
        Method printing one particular transaction
        """
        widget = f"Transaction:\n"
        widget += f"{'ID':^{format['ID']}}{'Raison':^{format['Raison']}}{'Montant':^{format['Montant']}}{'Date':^{format['Date']}}\n"
        widget += f"{self.get_id():^{format['ID']}}{self.get_raison():^{format['Raison']}}{self.get_montant():^{format['Montant']}.2f}{str(self.get_date()):^{format['Date']}}"

        print(widget)

    # Methods related to the modification of a transaction
    def modify(self):
        """
        Method to modify informations of a transaction
        """
        while True:
            modification = input("\nQue voulez-vous modifier? (Raison(r), Montant (m), Date(d), Type(t)): ").lower()
            if modification == "r":
                new_reason = input("Entrez la nouvelle raison pour cette transaction: ")
                while not self.validation_raison(new_reason):
                    new_reason = input("Entrez la nouvelle raison pour cette transaction: ")
                self.modify_raison(new_reason)
                break
            elif modification == "m":
                new_amount = input("Entrez le nouveau montant: ")
                while not self.validation_montant(new_amount):
                    new_amount = input("Entrez le nouveau montant: ")
                if self.get_type() == "d":
                    self.modify_montant(int(new_amount))
                else:
                    self.modify_montant(-int(new_amount))
                break
            elif modification == "d":
                # Entrer l'année
                new_year = input("Entrez l'année de la transaction: ")
                while not self.validation_year(new_year):
                    new_year = input("Entrez l'année de la transaction: ")

                # Entrer le mois
                new_month = input("Entrez le mois de la transaction: ")
                while not self.validation_month(new_month):
                    new_month = input("Entrez le mois de la transaction: ")

                new_day = input("Entrez le jour de la transaction: ")
                while not self.validation_day(new_day):
                    new_day = input("Entrez le jour de la transaction: ")
                self.modify_date(int(new_year), int(new_month), int(new_day))
                break

            elif modification == "t":
                new_type = input("Entrez le nouveau type de transaction (Dépôt(d) ou Retrait(r)): ").lower()
                while new_type not in ["d", "r"]:
                    new_type = input("Entrez le nouveau type de transaction (Dépôt(d) ou Retrait(r)): ").lower()
                self.modify_type(new_type)
                break
            else:
                print("Votre entrée n'est pas dans (r, m, d, t).")
                t.sleep(1)