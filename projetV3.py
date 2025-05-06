from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict

class Contribution:
    def __init__(self, nom, prenom, categorie, apport):
        self.nom = nom
        self.prenom = prenom
        self.categorie = categorie
        self.apport = apport

class gestionRepas:
    def __init__(self):
        self.contributions = []
        self.categories = ['Entrée', 'Plat', 'Dessert', 'Boisson']
        self.couleurs_etat = {
            "Critique": "#ff5757",
            "Insuffisant": "#eb7c46",
            "Suffisant": "#89bd73",
            "Abondant": "#ff5757"
        }

    def ajouter_contribution(self, contribution):
        self.contributions.append(contribution)

    def get_statistiques(self):
        counts = defaultdict(int)
        for contrib in self.contributions:
            counts[contrib.categorie] += 1
        return counts

    def valider_repas(self):
        stats = self.get_statistiques()
        total = sum(stats.values())

        if total == 0:
            return False, "Aucune contribution enregistrée!"

        manquant = [cat for cat in self.categories if stats[cat] == 0]
        if manquant:
            return False, f"Catégories manquantes: {', '.join(manquant)}"

        insuffisant = [cat for cat in self.categories if stats[cat] <= 2]
        if insuffisant:
            return False, f"Il faut au moins deux choix dans chaque catégorie: {', '.join(insuffisant)}"

        ecarts = [stats[cat] for cat in self.categories]
        if max(ecarts) - min(ecarts) > 3:
            return False, "Écart trop important entre les catégories !"

        return True, "Répartition équilibrée"

gr = gestionRepas()

def interface_participant(onglet):
    Label(onglet, text="Formulaire de contribution", font=("Helvetica", 14, "bold")).pack(pady=10)
    form_frame = Frame(onglet, bg="#f4f4f4")
    form_frame.pack(pady=10)

    Label(form_frame, text="Nom:", bg="#f4f4f4").grid(row=0, column=0, sticky="e", pady=5)
    nom_entry = Entry(form_frame)
    nom_entry.grid(row=0, column=1)

    Label(form_frame, text="Prénom:", bg="#f4f4f4").grid(row=1, column=0, sticky="e", pady=5)
    prenom_entry = Entry(form_frame)
    prenom_entry.grid(row=1, column=1)

    Label(form_frame, text="Catégorie:", bg="#f4f4f4").grid(row=2, column=0, sticky="e", pady=5)
    categorie_combo = ttk.Combobox(form_frame, values=gr.categories, state="readonly")
    categorie_combo.grid(row=2, column=1)
    categorie_combo.current(0)

    Label(form_frame, text="Apport:", bg="#f4f4f4").grid(row=3, column=0, sticky="e", pady=5)
    apport_entry = Entry(form_frame)
    apport_entry.grid(row=3, column=1)

    def enregistrer():
        nom = nom_entry.get()
        prenom = prenom_entry.get()
        categorie = categorie_combo.get()
        apport = apport_entry.get()

        if not nom or not prenom or not apport:
            messagebox.showwarning("Champs manquants", "Merci de remplir tous les champs.")
            return

        gr.ajouter_contribution(Contribution(nom, prenom, categorie, apport))
        messagebox.showinfo("Merci !", "Votre contribution a été enregistrée.")
        nom_entry.delete(0, END)
        prenom_entry.delete(0, END)
        apport_entry.delete(0, END)

    Button(onglet, text="Soumettre", command=enregistrer, bg="#4CAF50", fg="white", font=("Helvetica", 12)).pack(pady=10)

def afficher_contrib(fenetre):
    tableau_frame = Frame(fenetre)
    tableau_frame.pack(pady=20)

    headers = ["Nom", "Prénom", "Catégorie", "Apport"]
    for i, header in enumerate(headers):
        Label(tableau_frame, text=header, font=("Helvetica", 12, "bold"), borderwidth=1, relief="solid", padx=10, pady=5).grid(row=0, column=i)

    for row_index, c in enumerate(gr.contributions, start=1):
        Label(tableau_frame, text=c.nom, borderwidth=1, relief="solid", padx=10, pady=5).grid(row=row_index, column=0)
        Label(tableau_frame, text=c.prenom, borderwidth=1, relief="solid", padx=10, pady=5).grid(row=row_index, column=1)
        Label(tableau_frame, text=c.categorie, borderwidth=1, relief="solid", padx=10, pady=5).grid(row=row_index, column=2)
        Label(tableau_frame, text=c.apport, borderwidth=1, relief="solid", padx=10, pady=5).grid(row=row_index, column=3)

def afficher_recapitulatif(fenetre):
    recap_frame = Frame(fenetre)
    recap_frame.pack(pady=20)

    Label(recap_frame, text="Récapitulatif du repas", font=("Helvetica", 16, "bold")).pack(pady=10)
    conteneur_categories = Frame(recap_frame)
    conteneur_categories.pack()

    stats = gr.get_statistiques()
    plats_par_categorie = defaultdict(list)
    for cont in gr.contributions:
        plats_par_categorie[cont.categorie].append(cont.apport)

    for cat in gr.categories:
        frame_cat = Frame(conteneur_categories, bd=2, relief="groove", padx=10, pady=10)
        frame_cat.pack(side=LEFT, padx=10)

        Label(frame_cat, text=cat, font=("Helvetica", 12, "bold")).pack()
        quantite = stats[cat] if cat in stats else 0
        Label(frame_cat, text=f"Quantité : {quantite}/30", fg="green", font=("Helvetica", 10)).pack(pady=5)

        liste_frame = Frame(frame_cat, bd=1, relief="solid", width=100, height=100)
        liste_frame.pack()

        for plat in plats_par_categorie[cat]:
            Label(liste_frame, text=plat, anchor="w").pack(anchor="w")

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

def authenticate():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "1234":
        messagebox.showinfo("Connexion réussie", "Bienvenue dans l'organisation du repas de la promo !")
        login_window.destroy()
        ouvrir_organisation()
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

def interface_principale():
    global login_window, username_entry, password_entry
    login_window = Tk()
    login_window.title("Identification")
    login_window.geometry("400x350")
    login_window.config(bg="#f4f4f4")

    Label(login_window, text="Bienvenue au Repas organisé pour la Promo !", font=("Helvetica", 16), bg="#f4f4f4").pack(pady=10)

    Label(login_window, text="Je suis : ", font=("Helvetica", 12), bg="#f4f4f4").pack()

    notebook = ttk.Notebook(login_window)
    onglet_participant = ttk.Frame(notebook)
    onglet_organisateur = ttk.Frame(notebook)
    notebook.add(onglet_participant, text="Participant")
    notebook.add(onglet_organisateur, text="Organisateur")
    notebook.pack(expand=1, fill="both")

    interface_participant(onglet_participant)

    Label(onglet_organisateur, text="Connexion", font=("Helvetica", 14, "bold")).pack(pady=10)

    Label(onglet_organisateur, text="Nom d'utilisateur :", font=("Helvetica", 12)).pack()
    username_entry = ttk.Entry(onglet_organisateur)
    username_entry.pack()

    Label(onglet_organisateur, text="Mot de passe :", font=("Helvetica", 12)).pack()
    password_entry = ttk.Entry(onglet_organisateur, show="*")
    password_entry.pack()

    Button(onglet_organisateur, text="Se connecter", command=authenticate, bg="#2196F3", fg="white", font=("Helvetica", 12)).pack(pady=10)

    login_window.mainloop()

# Lancer l'application
interface_principale()
