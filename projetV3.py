import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict


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
        
        # écart de 3

        return True, "Répartition équilibrée"


# Ce qui sera affiché dans la section du participant
