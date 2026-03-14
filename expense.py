"""
Projet : Finances-Pro-Max
Autheur : Thomas Raymond
Date : 13 mars 2025

Description : Fonction qui ajoute des dépenses

"""
class Utilisateur:
    _depense=[]
    _revenu=[]

    def validation_montant(montant):
        while True:
            try:
                montant=float(montant)
            except ValueError:
                print("Veuillez entrer un nombre valide!")
                return False
            if montant<0:
                print("Vous devez entrer un nombre positif!")
                return False
            else:
                break
        return True

    def get_depense(self):
        return self._depense

    def set_depense(self, nouvelle_depense):
        if Utilisateur.validation_montant(nouvelle_depense):
            self._depense.append(nouvelle_depense)

    def get_revenu(self):
        return self._revenu

    def set_depense(self, nouveau_revenu):
        if Utilisateur.validation_montant(nouveau_revenu):
            self._revenu.append(nouveau_revenu)

    def entree_utilisateur():
        """
        Fonction qui gère l'entrée de la dépense de l'utilisateur

        Elle ne prend rien en entrée

        Elle ne retourne rien
        
        """
        Utilisateur.set_depense(Utilisateur.self, input("Entrez votre dépense en dollars CAD : ").replace(",","."))
        return Utilisateur.get_prix()*100
            


if __name__ == "__main__":
    Utilisateur.entree_utilisateur()