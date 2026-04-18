"""
Projet : Finances-Pro-Max
Autheur : Thomas Raymond
Date : 13 avril 2026

Description : Fonction qui ajoute des dépenses et des revenus

"""

import os
import platform

def validation_choix(choix): # Fonction à compléter
    return

def validation_montant(montant):
        while True:
            try:
                montant=float(montant[0])
            except ValueError:
                print("Veuillez entrer un nombre valide!")
                return False
            if montant<0:
                print("Vous devez entrer un nombre positif!")
                return False
            else:
                break
        return True

def ui_cleaner():
		if(platform.system() != "Linux"):
			os.system('cls')
		else:
			os.system('clear')



class Utilisateur:
	_depense=[]
	_revenu=[]

	def get_depense(self):
		depense_totale = 0
		for depense in self._depense:
			depense_totale += (depense)
		return depense_totale

	def set_depense(self, nouvelle_depense):
        	if validation_montant(nouvelle_depense):
           		self._depense.append(float(nouvelle_depense))
       		else:
           		print("Dépense non valide, veuillez réessayer.")

	def get_revenu(self):
		revenu_totale = 0 
		for revenu in self._revenu: 
			revenu_totale += (revenu)
		return revenu_totale

	def set_revenu(self, nouveau_revenu):
		if validation_montant(nouveau_revenu):
			self._revenu.append(float(nouveau_revenu))
		else:
			print("Revenu non valide, veuillez réessayer.")
	def get_solde(self):
		return self.get_revenu() - self.get_depense()
	
	def ui_endle(self):
		ui_cleaner()
		print("Votre Solde Actuel : ",self.get_solde() )
		print("Voulez-vous entrer une dépense ou un revenu? (d/r)\nQuitter: (q)")
		choix = input("Entrez votre choix (d/r/q) : ")
		return choix

	def entree_utilisateur():
		"""
		Fonction qui gère l'entrée d'une dépense ou d'un revenu de l'utilisateur

		Elle ne prend rien en entrée

		Elle retourne la dépense de l'utilisateur en cents

		"""
		solde = 0
		utilisateur=Utilisateur()
		while(True):
			choix = utilisateur.ui_endle()
			if choix == "d":
				utilisateur.set_depense(input("Entrez votre dépense en dollars CAD : ").replace(",","."))

			elif choix == "r":
				utilisateur.set_revenu(input("Entrez votre revenu en dollars CAD : ").replace(",","."))
			elif choix == "q":
				ui_cleaner()
				utilisateur.get_solde()
				break
if __name__ == "__main__":
	Utilisateur.entree_utilisateur()

