import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict
from tkinter import *

class Contribution:
    # représente la contribution de chaque étudiant
    def __init__(self, nom, prenom, categorie, apport):
        self.nom = nom
        self.prenom = prenom
        self.categorie = categorie
        self.apport = apport

class gestionRepas:
    # représente la logique de l'organisation des repas
    def __init__(self):
        self.contributions = []
        self.categories = ['Entrée', 'Plat', 'Dessert', 'Boisson']
        self.couleurs_etat = {
            "Critique": "#ff5757",
            "Insuffisant": "#eb7c46",
            "Suffisant": "#89bd73",
            "Abondant": "#ff5757"
        }

        

    # ajouter une nouvelle contribution
    def ajouter_contribution(self, contribution):
        self.contributions.append(contribution)

    # avoir les statistiques des contributions actuelles
    def get_statistiques(self):
        counts = defaultdict(int)
        """defaultdict est une sous-classe de dict qui permet de définir une valeur par défaut pour les clés inexistantes. Tu n’as donc pas besoin de vérifier si une clé existe avant d’y ajouter une valeur."""
        for contrib in self.contributions:
            counts[contrib. categorie] += 1
        # Renvoie un dictionnaire indiquant combien de contributions il y a pour chaque catégorie
        return counts
    
    # valider un repas si le repas est équilibré
    def valider_repas(self):
        # on récupère les statistiques actuelles
        stats = self.get_statistiques
        # on calcule le total des stats pour vérifier si le repas est équilibré
        total = sum(stats.values())

        if total == 0: 
            return False, "Aucune contribution enregistrée!"
        
        # vérifier s'il y a une catégorie manquante dans le repas
        manquant = [cat for cat in self.categories if stats[cat] == 0]
        if manquant:
            return False, f"Catégories manquantes: {', '.join(manquant)}"
        
        # vérifier qu'il y a au moins deux choix dans chaque catégorie
        insuffisant = [cat for cat in self.categories if stats[cat] <= 2]
        if insuffisant:
            return False, f"Il faut au moins deux choix dans chaque catégorie: {', '. join(insuffisant)}"
        
        #ici nous vérifions si la répartition entre les catégories est vérifier. Si il y a plus de 3 de différence le repas ne peut pas se faire 
        # On évalue donc l'écart entre le plus petit nombre de contribution et le plus grand nombre 
        ecarts = [stats[cat] for cat in self.categories]
        if max(ecarts) - min(ecarts) > 3 :
            return False, "Écart trop important entre les catégories (il y a plus de 3 contributions de différence) ! "

        #si toutes les conditions sont vérifiées alors le repas est valide
        return True, "Répartition équilibrée"


# Ce qui sera affiché dans la section du participant
#ici il faut faire la fonction pour écrire le formulaire de contribution avec les Label (nom, prénom...) 
    # et aussi une fonction qui va enregistrer la contribution en utilisant la classe Contribution
    # def interface_participant(fenetre_parent) : 

gr = gestionRepas()

def afficher_contrib(fenetre):
        tableau_frame = Frame(fenetre)
        tableau_frame.pack(pady=20)

        #on crée les en-têtes de notre tableau
        headers = ["Nom", "Prénom", "Catégorie", "Apport"]
        for i, header in enumerate(headers):
            Label(tableau_frame, text=header, font=("Helvetica", 12, "bold"), borderwidth=1, relief="solid", padx=10, pady=5).grid(row=0, column=i)

        #on remplit le tableau en utilisant les attributs de la classe Contribution 
        for colonne_index, c in enumerate(gr.contributions) :
            Label(tableau_frame, text=c.nom, borderwidth=1, relief="solid", padx=10, pady=5).grid(row=colonne_index, column=0)
            Label(tableau_frame, text=c.categorie, borderwidth=1, relief="solid", padx=10, pady=5).grid(row=colonne_index, column=0)
            Label(tableau_frame, text=c.apport, borderwidth=1, relief="solid", padx=10, pady=5).grid(row=colonne_index, column=0)

#fonction pour afficher les contributions de chaque catégorie du repas avec des Frame pour chacun 
def afficher_recapitulatif(fenetre):
    recap_frame = Frame(fenetre)
    recap_frame.pack(pady=20)

    Label(recap_frame, text="Récapitulatif du repas", font=("Helvetica", 16, "bold")).pack(pady=10)

    conteneur_categories = Frame(recap_frame)
    conteneur_categories.pack()

    stats = gr.get_statistiques()

    plats_par_categorie = defaultdict(list)
    for cont in gr.contributions :
        plats_par_categorie[cont.categorie].append(cont.apport)

    for cat in gr.categories :
        frame_cat = Frame(conteneur_categories, bd=2, relief="groove", padx=10, pady=10)
        frame_cat.pack(side=LEFT, padx=10)

        Label(frame_cat, text=cat, font=("Helvetica", 12, "bold")).pack()

        quantite = stats[cat] if cat in stats else 0
        Label(frame_cat, text=f"Quantité : {quantite}/30", fg="green", font=("Helvetica", 10)).pack(pady=5)

        liste_frame = Frame(frame_cat, bd=1, relief="solid", width=100, height=100)
        liste_frame.pack()

        for plat in plats_par_categorie[cat] :
            Label(liste_frame, text=plat, anchor="w").pack(anchor="w")

#fonction pour ouvrir la fenetre de l'organisateur 
def ouvrir_organisation():
        global room_selection_window
        room_selection_window = Tk()
        room_selection_window.title("Organisation repas de la promo")
        room_selection_window.geometry("600x500")
        room_selection_window.config(bg="#f4f4f4")

        Label(room_selection_window, text="Liste des contributions", font=("Helvetica", 14), bg="#f4f4f4").pack(pady=10)
        afficher_contrib(room_selection_window)

        Label(room_selection_window, font=("Helvetica", 14)).pack(pady=20)
        afficher_recapitulatif(room_selection_window)


# Fonction pour vérifier l'identification de l'organisateur 
def authenticate():
    username = username_entry.get()
    password = password_entry.get()
        
    if username == "utilisateur" and password == "1234":
        messagebox.showinfo("Connexion réussie", "Bienvenue dans l'organisation du repas de la promo !")
        login_window.destroy()
        ouvrir_organisation()
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")


def interface_principale():
    #on rend globale les 3 variables pour les utiliser dans une autre fonction (authenticate)
    global login_window, username_entry, password_entry
    login_window = Tk()
    login_window.title("Identification")
    login_window.geometry("400x320")
    login_window.config(bg="#f4f4f4")



    Label(login_window, text="Bienvenue au Repas organisé pour la Promo ! ", font=("Helvetica, 16"), bg="#f4f4f4").pack()

     # Création des onglets participant et organisateur 

    Label(login_window, text="Je suis : ", font=("Helvetica", 12), bg="#f4f4f4").pack()

    #utilisation de notebook pour organiser les 2 pages participant et organisateur dans un seul conteneur
    notebook = ttk.Notebook(login_window)
    onglet_participant = ttk.Frame(notebook)
    onglet_organisateur = ttk.Frame(notebook)
    notebook.add(onglet_participant, text="Participant")
    notebook.add(onglet_organisateur, text="Organisateur")
    notebook.pack(expand=1, fill="both")


    # interface_participant(onglet_participant)

    #côté organisateur : objets pour l'identification 
    Label(login_window, text="Connexion", font=("Helvetica", 16, "bold"), bg="#f4f4f4").pack(pady=10)

    Label(login_window, text="Nom d'utilisateur :", font=("Helvetica", 12), bg="#f4f4f4").pack()
    username_entry = ttk.Entry(login_window, font=("Helvetica", 12))
    username_entry.pack(pady=5)

    Label(login_window, text="Mot de passe :", font=("Helvetica", 12), bg="#f4f4f4").pack()
    password_entry = ttk.Entry(login_window, font=("Helvetica", 12), show="*")
    password_entry.pack(pady=5)

    ttk.Button(login_window, text="Se connecter", command=authenticate, style="Modern.TButton").pack(pady=10)

    login_window.mainloop()
    

   
if __name__ == "__main__":
    interface_principale()
    
