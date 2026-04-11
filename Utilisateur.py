"""
Projet : Finances-Pro-Max
Autheur : Thomas Raymond
Date : 13 avril 2026

Description : Fonction qui ajoute des dépenses et des revenus

"""
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

class Utilisateur:
    _depense=[]
    _revenu=[]

    def get_depense(self):
        return self._depense

    def set_depense(self, nouvelle_depense):
        if validation_montant(nouvelle_depense):
            self._depense.append(nouvelle_depense)
        else:
            print("Dépense non valide, veuillez réessayer.")

    def get_revenu(self):
        return self._revenu

    def set_revenu(self, nouveau_revenu):
        if validation_montant(nouveau_revenu):
            self._revenu.append(nouveau_revenu)
        else:
            print("Revenu non valide, veuillez réessayer.")

    def entree_utilisateur():
        """
        Fonction qui gère l'entrée d'une dépense ou d'un revenu de l'utilisateur

        Elle ne prend rien en entrée

        Elle retourne la dépense de l'utilisateur en cents
        
        """
        utilisateur=Utilisateur()
        print("Voulez-vous entrer une dépense ou un revenu? (d/r)")
        choix = input("Entrez votre choix (d/r) : ")
        if choix == "d":
            utilisateur.set_depense(input("Entrez votre dépense en dollars CAD : ").replace(",","."))
            return utilisateur.get_depense()*100 # Mettre le prix en cents

        elif choix == "r":
            utilisateur.set_revenu(input("Entrez votre revenu en dollars CAD : ").replace(",","."))
            return utilisateur.get_revenu()*100 # Mettre le revenu en cents
            


if __name__ == "__main__":
    Utilisateur.entree_utilisateur()