
"""
Projet : Finances-Pro-Max
Autheur : Thomas Raymond
Date : 13 avril 2026

Description : Fonction qui ajoute des dépenses et des revenus

"""
import array as arr
import os
import platform

def validation_choix(choix): # Fonction à compléter
    return


def screen_clear():
	if(platform.system() != "Linux"):
		os.system('cls')
	else:
		os.system('clear')

class Utilisateur:

	def __init__(self):
		self.__depot = arr.array('f',{0})
		self.__retrait = arr.array('f',{0})
		self.transaction = arr.array('f',{0})


	def validation_montant(self,montant):
		try:
			montant=float(montant)
		except ValueError:
			print("Veuillez entrer un nombre valide!")
			return False
		if montant>0:
                	return True
		else:
			print("Vous devez entrer un nombre positif!")
		return False


	def __set_depot(self,montant):
		self.__depot.append(montant)

	def __set_retrait(self,montant):
		self.__retrait.append(montant)

	def get_historique_depot(self):
		return __depot

	def set_transaction(self,montant,genre):
		if self.validation_montant(montant):
			transaction = float(montant)
			if(genre == "d"):
				self.__set_depot(transaction)
			else:
				transaction *= -1
				self.__set_retrait(transaction)
			self.transaction.append(transaction)
		else:
           		print("Transaction non valide, veuillez réessayer.")

	def get_historique_retrait(self):
		return self.__retrait

	def get_transaction(self):
		solde =0
		for montant in self.transaction:
			solde += montant
		return solde

	def __str__(self):
		return f"Votre solde est de : {self.get_transaction()}$ \nVoulez-vous entrer une dépot ou un retrait? (d/r)\nQuitter: (q)"

if __name__ == "__main__":
	solde = 0
	utilisateur=Utilisateur()
	while(True):
		screen_clear()
		print(utilisateur)
		choix = input("Entrez votre choix (d/r/q) : ")
		if choix == "d":
			utilisateur.set_transaction(input("Entrez votre dépot en dollars CAD : ",).replace(",","."),choix)
		elif choix == "r":
			utilisateur.set_transaction(input("Entrez votre retrait en dollars CAD : ").replace(",","."),choix)
		elif choix == "q":
			screen_clear()
			print("Votre solde est de : ",utilisateur.get_transaction(),"$")
			break

            
