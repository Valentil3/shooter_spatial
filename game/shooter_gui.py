"""
Shooter Spatial - Version avec Menu d'Accueil CORRIGÉ
Tous les problèmes sont corrigés :
- Boutons fonctionnels (vrais widgets tkinter)
- Titre adapté à la largeur
- Interface responsive selon la taille d'écran
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import time
import random
import webbrowser
from pathlib import Path
from typing import Optional
from game_classes import GameEngine
from score_manager import ScoreManager

# Pour la musique
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


class Config:
    VITESSE_INITIALE = 0.05
    VITESSE_MAX = 2.0
    SPAWN_INITIAL = 3000
    SPAWN_MIN = 1200
    CHANCE_BONUS = 0.30


def obtenir_dimensions_ecran(root):
    """Obtient les dimensions optimales"""
    largeur_ecran = root.winfo_screenwidth()
    hauteur_ecran = root.winfo_screenheight()
    
    largeur = 600
    hauteur = 800
    
    if hauteur_ecran < 900:
        hauteur = int(hauteur_ecran * 0.85)
        largeur = int(hauteur * 0.75)
    
    if largeur < 400:
        largeur = 400
    if hauteur < 600:
        hauteur = 600
    
    return largeur, hauteur


class EtoileAnimee:
    def __init__(self, x, y, vitesse, taille, couleur, hauteur_max, largeur_max=None):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.taille = taille
        self.couleur = couleur
        self.hauteur_max = hauteur_max
        self.largeur_max = largeur_max if largeur_max else hauteur_max
    
    def deplacer(self):
        self.y += self.vitesse
        if self.y > self.hauteur_max:
            self.y = 0
            self.x = random.randint(0, self.largeur_max)
    
    def mettre_a_jour_dimensions(self, hauteur_max, largeur_max):
        """Met à jour les dimensions max pour le redimensionnement"""
        self.hauteur_max = hauteur_max
        self.largeur_max = largeur_max


class MusiqueThread(threading.Thread):
    def __init__(self, fichier="musique.mp3", volume=0.3):
        super().__init__(daemon=True)
        # Utiliser un chemin absolu basé sur l'emplacement du script
        script_dir = Path(__file__).parent
        self.fichier = script_dir / fichier if not Path(fichier).is_absolute() else Path(fichier)
        self.jouer = True
        self.volume = volume
        
        if PYGAME_AVAILABLE:
            try:
                # Vérifier si le fichier existe
                if not self.fichier.exists():
                    print(f"⚠️ Fichier musique non trouvé: {self.fichier}")
                    self.jouer = False
                    return
                
                pygame.mixer.init()
                pygame.mixer.music.load(str(self.fichier))
                pygame.mixer.music.set_volume(volume)
            except (pygame.error, OSError) as e:
                print(f"⚠️ Impossible de charger la musique: {e}")
                self.jouer = False
    
    def run(self):
        if PYGAME_AVAILABLE and self.jouer:
            try:
                pygame.mixer.music.play(-1)
                while self.jouer:
                    time.sleep(0.1)
            except pygame.error as e:
                print(f"⚠️ Erreur de lecture musique: {e}")
    
    def pause(self):
        if PYGAME_AVAILABLE:
            pygame.mixer.music.pause()
    
    def reprendre(self):
        if PYGAME_AVAILABLE:
            pygame.mixer.music.unpause()
    
    def arreter(self):
        self.jouer = False
        if PYGAME_AVAILABLE:
            pygame.mixer.music.stop()
    
    def set_volume(self, volume: float):
        """Change le volume (0.0 à 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        if PYGAME_AVAILABLE:
            pygame.mixer.music.set_volume(self.volume)


class MenuPrincipal:
    def __init__(self, root, callback_jouer, callback_instructions, callback_scores, largeur, hauteur):
        self.root = root
        self.callback_jouer = callback_jouer
        self.callback_instructions = callback_instructions
        self.callback_scores = callback_scores
        self.LARGEUR = largeur
        self.HAUTEUR = hauteur
        
        self.frame = tk.Frame(root, bg='black', width=self.LARGEUR, height=self.HAUTEUR)
        
        self.canvas = tk.Canvas(
            self.frame, width=self.LARGEUR, height=self.HAUTEUR,
            bg='black', highlightthickness=0
        )
        self.canvas.pack()
        
        self.etoiles = []
        self.creer_etoiles()
        self.creer_interface()
        self.animation_active = False
    
    def creer_etoiles(self):
        for i in range(100):
            x = random.randint(0, self.LARGEUR)
            y = random.randint(0, self.HAUTEUR)
            vitesse = random.uniform(0.2, 1.5)
            taille = random.randint(1, 3)
            couleur = random.choice(['white', '#ffffaa', '#aaaaff'])
            self.etoiles.append(EtoileAnimee(x, y, vitesse, taille, couleur, self.HAUTEUR, self.LARGEUR))
    
    def creer_interface(self):
        taille_titre = max(20, min(36, int(self.LARGEUR / 17)))
        taille_sous_titre = max(12, min(18, int(self.HAUTEUR / 50)))
        taille_bouton = max(14, min(20, int(self.HAUTEUR / 45)))
        
        self.canvas.create_text(
            self.LARGEUR // 2, int(self.HAUTEUR * 0.15),
            text="SHOOTER SPATIAL",
            font=('Arial', taille_titre, 'bold'),
            fill='#00ff88', tags='titre'
        )
        
        self.canvas.create_text(
            self.LARGEUR // 2, int(self.HAUTEUR * 0.22),
            text="🚀 Défendez la galaxie ! 🚀",
            font=('Arial', taille_sous_titre, 'italic'),
            fill='#88ffff', tags='sous_titre'
        )
        
        self.frame_boutons = tk.Frame(self.canvas, bg='black')
        self.canvas.create_window(
            self.LARGEUR // 2, int(self.HAUTEUR * 0.55),
            window=self.frame_boutons
        )
        
        largeur_bouton = max(20, min(30, int(self.LARGEUR / 20)))
        
        tk.Button(
            self.frame_boutons, text="▶ JOUER",
            command=self.callback_jouer,
            font=('Arial', taille_bouton, 'bold'),
            bg='#00ff88', fg='black',
            activebackground='#00dd77', activeforeground='black',
            relief=tk.FLAT, width=largeur_bouton, height=2, cursor='hand2'
        ).pack(pady=10)
        
        tk.Button(
            self.frame_boutons, text="📖 COMMENT JOUER",
            command=self.callback_instructions,
            font=('Arial', taille_bouton - 2, 'bold'),
            bg='#ffaa00', fg='black',
            activebackground='#dd8800', activeforeground='black',
            relief=tk.FLAT, width=largeur_bouton, height=2, cursor='hand2'
        ).pack(pady=10)
        
        tk.Button(
            self.frame_boutons, text="🏆 SCORES",
            command=self.callback_scores,
            font=('Arial', taille_bouton - 2, 'bold'),
            bg='#ffd700', fg='black',
            activebackground='#ffbb00', activeforeground='black',
            relief=tk.FLAT, width=largeur_bouton, height=2, cursor='hand2'
        ).pack(pady=10)
        
        tk.Button(
            self.frame_boutons, text="❌ QUITTER",
            command=self.root.quit,
            font=('Arial', taille_bouton - 2, 'bold'),
            bg='#ff4444', fg='white',
            activebackground='#dd2222', activeforeground='white',
            relief=tk.FLAT, width=largeur_bouton, height=2, cursor='hand2'
        ).pack(pady=10)
        
        taille_footer = max(9, min(11, int(self.HAUTEUR / 80)))
        self.canvas.create_text(
            self.LARGEUR // 2, int(self.HAUTEUR * 0.95),
            text="← → ↑ ↓ et ESPACE pour tirer",
            font=('Arial', taille_footer), fill='#666666'
        )
    
    def animer_fond(self):
        if not self.animation_active or not self.frame.winfo_exists():
            return
        
        self.canvas.delete('etoile')
        
        for etoile in self.etoiles:
            etoile.deplacer()
            self.canvas.create_oval(
                etoile.x - etoile.taille, etoile.y - etoile.taille,
                etoile.x + etoile.taille, etoile.y + etoile.taille,
                fill=etoile.couleur, outline='', tags='etoile'
            )
        
        self.canvas.tag_raise('titre')
        self.canvas.tag_raise('sous_titre')
        self.root.after(30, self.animer_fond)
    
    def afficher(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.animation_active = True
        self.animer_fond()
    
    def masquer(self):
        self.animation_active = False
        self.frame.pack_forget()


class EcranInstructions:
    def __init__(self, root, callback_retour, largeur, hauteur):
        self.root = root
        self.callback_retour = callback_retour
        self.largeur = largeur
        self.hauteur = hauteur
        
        self.frame = tk.Frame(root, bg='#0a0a1a', width=largeur, height=hauteur)
        self.creer_interface()
    
    def creer_interface(self):
        taille_titre = max(20, min(32, int(self.hauteur / 25)))
        taille_section = max(13, min(18, int(self.hauteur / 45)))
        taille_texte = max(10, min(14, int(self.hauteur / 60)))
        taille_bouton = max(12, min(16, int(self.hauteur / 50)))
        
        # Titre principal
        tk.Label(
            self.frame, text="📖 COMMENT JOUER",
            font=('Arial', taille_titre, 'bold'),
            fg='#00ff88', bg='#0a0a1a'
        ).pack(pady=20)
        
        # Conteneur principal scrollable
        canvas = tk.Canvas(self.frame, bg='#0a0a1a', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#0a0a1a')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # === OBJECTIF ===
        self._section(scrollable_frame, "🎯 OBJECTIF", '#ff6b6b', taille_section)
        self._texte(scrollable_frame, "Détruis les ennemis et survie le plus longtemps possible !", taille_texte + 1, '#ffffff')
        self._texte(scrollable_frame, "Chaque ennemi détruit = +10 points 💰", taille_texte, '#ffd700')
        self._separateur(scrollable_frame)
        
        # === CONTRÔLES ===
        self._section(scrollable_frame, "⌨️ CONTRÔLES", '#4ecdc4', taille_section)
        
        ctrl_frame = tk.Frame(scrollable_frame, bg='#1a2a2a')
        ctrl_frame.pack(fill=tk.X, padx=40, pady=8)
        
        controles = [
            ("←→↑↓", "Déplacer le vaisseau"),
            ("ESPACE", "Tirer 🔫"),
            ("P", "Pause/Reprendre musique 🎵 (jeu continue)"),
            ("ESC", "Quitter")
        ]
        
        for touche, desc in controles:
            row = tk.Frame(ctrl_frame, bg='#1a2a2a')
            row.pack(fill=tk.X, pady=4)
            
            tk.Label(
                row, text=touche,
                font=('Consolas', taille_texte, 'bold'),
                fg='#00ff88', bg='#0d1117',
                relief=tk.RAISED, padx=8, pady=4, width=8
            ).pack(side=tk.LEFT, padx=(0, 12))
            
            tk.Label(
                row, text=desc,
                font=('Arial', taille_texte),
                fg='#cccccc', bg='#1a2a2a', anchor='w'
            ).pack(side=tk.LEFT)
        
        self._separateur(scrollable_frame)
        
        # === GAMEPLAY ===
        self._section(scrollable_frame, "🎮 GAMEPLAY", '#ff88ff', taille_section)
        
        gameplay_frame = tk.Frame(scrollable_frame, bg='#1a1a2a')
        gameplay_frame.pack(fill=tk.X, padx=40, pady=8)
        
        infos = [
            ("👾", "Ennemis rouges", "Descendent vers toi", '#ff6666'),
            ("💚", "3 vies", "Maximum 5 avec bonus", '#66ff66'),
            ("🛡️", "Invincibilité", "Vaisseau clignote après dégât", '#ffff66'),
            ("💥", "Collision", "Ennemi touché ou atteint le bas = -1 vie", '#ffaa66'),
        ]
        
        for emoji, titre, desc, couleur in infos:
            row = tk.Frame(gameplay_frame, bg='#1a1a2a')
            row.pack(fill=tk.X, pady=3)
            
            tk.Label(
                row, text=emoji,
                font=('Arial', taille_texte + 2),
                bg='#1a1a2a', width=3
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row, text=titre,
                font=('Arial', taille_texte, 'bold'),
                fg=couleur, bg='#1a1a2a', width=12, anchor='w'
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row, text=desc,
                font=('Arial', taille_texte - 1),
                fg='#aaaaaa', bg='#1a1a2a', anchor='w'
            ).pack(side=tk.LEFT, padx=5)
        
        self._separateur(scrollable_frame)
        
        # === BONUS ===
        self._section(scrollable_frame, "💎 BONUS (10 secondes)", '#ffd700', taille_section)
        
        bonus_frame = tk.Frame(scrollable_frame, bg='#0a0a1a')
        bonus_frame.pack(fill=tk.X, padx=40, pady=8)
        
        bonus = [
            ("+", "Vie +1", "#ff00ff"),
            (">>", "Vitesse +50%", "#00ffff"),
            ("=", "Tir Double", "#ffff00"),
            ("≡", "Tir Triple", "#ff8800"),
            ("!!!", "Tir Rapide", "#ff0000")
        ]
        
        for symbole, nom, couleur in bonus:
            row = tk.Frame(bonus_frame, bg='#0a0a1a')
            row.pack(fill=tk.X, pady=2)
            
            tk.Label(
                row, text=symbole,
                font=('Consolas', taille_texte + 2, 'bold'),
                fg=couleur, bg='#000000',
                width=5, relief=tk.RAISED
            ).pack(side=tk.LEFT, padx=(0, 15))
            
            tk.Label(
                row, text=nom,
                font=('Arial', taille_texte),
                fg=couleur, bg='#0a0a1a', anchor='w'
            ).pack(side=tk.LEFT)
        
        self._texte(scrollable_frame, "💡 Le vaisseau change de couleur selon le bonus actif", taille_texte - 1, '#888888')
        self._separateur(scrollable_frame)
        
        # === ASTUCES ===
        self._section(scrollable_frame, "💡 ASTUCES", '#00ff88', taille_section)
        
        astuces_frame = tk.Frame(scrollable_frame, bg='#0a1a0a')
        astuces_frame.pack(fill=tk.X, padx=40, pady=8)
        
        astuces = [
            "✓ Reste au centre de l'écran",
            "✓ Collecte Tir Triple en priorité",
            "✓ Combine Tir Triple + Tir Rapide 🔥",
            "✓ Bouge constamment !"
        ]
        
        for astuce in astuces:
            tk.Label(
                astuces_frame, text=astuce,
                font=('Arial', taille_texte),
                fg='#88ff88', bg='#0a1a0a', anchor='w', padx=10, pady=2
            ).pack(fill=tk.X)
        
        # Espacement avant le bouton
        tk.Label(scrollable_frame, text="", bg='#0a0a1a').pack(pady=15)
        
        # Bouton retour dans le contenu scrollable
        tk.Button(
            scrollable_frame, text="◀ RETOUR",
            command=self.callback_retour,
            font=('Arial', taille_bouton, 'bold'),
            bg='#00ff88', fg='black',
            activebackground='#00dd77',
            relief=tk.FLAT, padx=30, pady=12, cursor='hand2'
        ).pack(pady=15)
        
        # Empaquetage du canvas et scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _section(self, parent, texte, couleur, taille):
        """Titre de section"""
        tk.Label(
            parent, text=texte,
            font=('Arial', taille, 'bold'),
            fg=couleur, bg='#0a0a1a'
        ).pack(pady=(12, 5))
    
    def _texte(self, parent, texte, taille, couleur='#cccccc'):
        """Label de texte"""
        tk.Label(
            parent, text=texte,
            font=('Arial', taille),
            fg=couleur, bg='#0a0a1a',
            wraplength=self.largeur - 100
        ).pack(padx=40, pady=2)
    
    def _separateur(self, parent):
        """Ligne de séparation"""
        tk.Frame(parent, bg='#333333', height=1).pack(fill=tk.X, padx=60, pady=12)
    
    def afficher(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
    
    def masquer(self):
        self.frame.pack_forget()


class EcranScores:
    def __init__(self, root, callback_retour, score_manager, largeur, hauteur):
        self.root = root
        self.callback_retour = callback_retour
        self.score_manager = score_manager
        self.largeur = largeur
        self.hauteur = hauteur
        self.tri_actuel = "score"  # Par défaut: tri par score
        self.ordre_actuel = "desc"  # Par défaut: ordre décroissant
        
        self.frame = tk.Frame(root, bg='#1a1a2e', width=largeur, height=hauteur)
        self.creer_interface()
    
    def creer_interface(self):
        taille_titre = max(18, min(28, int(self.hauteur / 28)))
        taille_texte = max(9, min(12, int(self.hauteur / 70)))
        taille_bouton = max(10, min(14, int(self.hauteur / 60)))
        
        tk.Label(
            self.frame, text="🏆 MEILLEURS SCORES",
            font=('Arial', taille_titre, 'bold'),
            fg='#ffd700', bg='#1a1a2e'
        ).pack(pady=15)
        
        # Boutons de tri
        frame_tri = tk.Frame(self.frame, bg='#1a1a2e')
        frame_tri.pack(pady=5)
        
        # Groupe Score
        frame_score = tk.Frame(frame_tri, bg='#1a1a2e')
        frame_score.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_score, text="🏆↓",
            command=lambda: self.changer_tri("score", "desc"),
            font=('Arial', taille_bouton - 2, 'bold'),
            bg='#00ff88' if (self.tri_actuel == "score" and self.ordre_actuel == "desc") else '#555555',
            fg='black' if (self.tri_actuel == "score" and self.ordre_actuel == "desc") else 'white',
            relief=tk.FLAT, padx=6, pady=4, cursor='hand2'
        ).pack(side=tk.LEFT, padx=1)
        
        tk.Button(
            frame_score, text="🏆↑",
            command=lambda: self.changer_tri("score", "asc"),
            font=('Arial', taille_bouton - 2, 'bold'),
            bg='#00ff88' if (self.tri_actuel == "score" and self.ordre_actuel == "asc") else '#555555',
            fg='black' if (self.tri_actuel == "score" and self.ordre_actuel == "asc") else 'white',
            relief=tk.FLAT, padx=6, pady=4, cursor='hand2'
        ).pack(side=tk.LEFT, padx=1)
        
        # Groupe Date
        frame_date = tk.Frame(frame_tri, bg='#1a1a2e')
        frame_date.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_date, text="📅↓",
            command=lambda: self.changer_tri("date", "desc"),
            font=('Arial', taille_bouton - 2, 'bold'),
            bg='#00ff88' if (self.tri_actuel == "date" and self.ordre_actuel == "desc") else '#555555',
            fg='black' if (self.tri_actuel == "date" and self.ordre_actuel == "desc") else 'white',
            relief=tk.FLAT, padx=6, pady=4, cursor='hand2'
        ).pack(side=tk.LEFT, padx=1)
        
        tk.Button(
            frame_date, text="📅↑",
            command=lambda: self.changer_tri("date", "asc"),
            font=('Arial', taille_bouton - 2, 'bold'),
            bg='#00ff88' if (self.tri_actuel == "date" and self.ordre_actuel == "asc") else '#555555',
            fg='black' if (self.tri_actuel == "date" and self.ordre_actuel == "asc") else 'white',
            relief=tk.FLAT, padx=6, pady=4, cursor='hand2'
        ).pack(side=tk.LEFT, padx=1)
        
        # Groupe Pseudo
        frame_pseudo = tk.Frame(frame_tri, bg='#1a1a2e')
        frame_pseudo.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_pseudo, text="👤 Z→A",
            command=lambda: self.changer_tri("pseudo", "desc"),
            font=('Arial', taille_bouton - 2, 'bold'),
            bg='#00ff88' if (self.tri_actuel == "pseudo" and self.ordre_actuel == "desc") else '#555555',
            fg='black' if (self.tri_actuel == "pseudo" and self.ordre_actuel == "desc") else 'white',
            relief=tk.FLAT, padx=6, pady=4, cursor='hand2'
        ).pack(side=tk.LEFT, padx=1)
        
        tk.Button(
            frame_pseudo, text="👤 A→Z",
            command=lambda: self.changer_tri("pseudo", "asc"),
            font=('Arial', taille_bouton - 2, 'bold'),
            bg='#00ff88' if (self.tri_actuel == "pseudo" and self.ordre_actuel == "asc") else '#555555',
            fg='black' if (self.tri_actuel == "pseudo" and self.ordre_actuel == "asc") else 'white',
            relief=tk.FLAT, padx=6, pady=4, cursor='hand2'
        ).pack(side=tk.LEFT, padx=1)
        
        # Frame pour le classement (sera mis à jour dynamiquement)
        self.frame_classement = tk.Frame(self.frame, bg='#1a1a2e')
        self.frame_classement.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.afficher_classement()
        
        frame_boutons = tk.Frame(self.frame, bg='#1a1a2e')
        frame_boutons.pack(pady=10)
        
        tk.Button(
            frame_boutons, text="🌐 WEB",
            command=self.ouvrir_web,
            font=('Arial', taille_bouton, 'bold'),
            bg='#0088ff', fg='white',
            relief=tk.FLAT, padx=10, pady=6, cursor='hand2'
        ).pack(side=tk.LEFT, padx=3)
        
        tk.Button(
            frame_boutons, text="◀ RETOUR",
            command=self.callback_retour,
            font=('Arial', taille_bouton, 'bold'),
            bg='#00ff88', fg='black',
            relief=tk.FLAT, padx=10, pady=6, cursor='hand2'
        ).pack(side=tk.LEFT, padx=3)
    
    def changer_tri(self, nouveau_tri, nouvel_ordre):
        """Change le mode de tri et l'ordre, puis actualise l'affichage"""
        if self.tri_actuel != nouveau_tri or self.ordre_actuel != nouvel_ordre:
            self.tri_actuel = nouveau_tri
            self.ordre_actuel = nouvel_ordre
            # Recréer toute l'interface pour mettre à jour les boutons et le classement
            for widget in self.frame.winfo_children():
                widget.destroy()
            self.creer_interface()
    
    def afficher_classement(self):
        """Affiche le classement selon le tri et l'ordre actuels"""
        taille_texte = max(8, min(11, int(self.hauteur / 75)))
        
        classement = self.score_manager.obtenir_classement(10, tri=self.tri_actuel, ordre=self.ordre_actuel)
        
        if not classement:
            tk.Label(
                self.frame_classement,
                text="Aucun score\n\nLancez une partie !",
                font=('Arial', taille_texte + 2),
                fg='#888888', bg='#1a1a2e'
            ).pack(pady=30)
        else:
            for i, (joueur, score, date, _) in enumerate(classement, 1):
                if i == 1 and self.tri_actuel == "score" and self.ordre_actuel == "desc":
                    bg, fg, med = '#2a2a1e', '#ffd700', '🥇'
                elif i == 2 and self.tri_actuel == "score" and self.ordre_actuel == "desc":
                    bg, fg, med = '#2a2a2a', '#c0c0c0', '🥈'
                elif i == 3 and self.tri_actuel == "score" and self.ordre_actuel == "desc":
                    bg, fg, med = '#2a2520', '#cd7f32', '🥉'
                else:
                    bg, fg, med = '#1a1a2e', '#00ff88', f'{i}.'
                
                frame_ligne = tk.Frame(self.frame_classement, bg=bg)
                frame_ligne.pack(fill=tk.X, pady=1)
                
                tk.Label(
                    frame_ligne, text=med,
                    font=('Arial', taille_texte, 'bold'),
                    fg=fg, bg=bg, width=4
                ).pack(side=tk.LEFT, padx=3)
                
                tk.Label(
                    frame_ligne, text=joueur,
                    font=('Courier', taille_texte, 'bold'),
                    fg='white', bg=bg, anchor='w'
                ).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
                
                tk.Label(
                    frame_ligne, text=f"{score} pts",
                    font=('Courier', taille_texte, 'bold'),
                    fg=fg, bg=bg, anchor='e', width=10
                ).pack(side=tk.LEFT, padx=3)
                
                # Afficher la date
                date_courte = date.split()[0] if date != "Inconnue" else "---"
                tk.Label(
                    frame_ligne, text=date_courte,
                    font=('Courier', taille_texte - 2),
                    fg='#888888', bg=bg, anchor='e', width=12
                ).pack(side=tk.LEFT, padx=3)
    
    def ouvrir_web(self):
        try:
            self.score_manager.exporter_html()
            script_dir = Path(__file__).parent
            chemin = script_dir / "index.html"
            if chemin.exists():
                webbrowser.open(f"file:///{chemin.as_posix()}")
            else:
                messagebox.showwarning(
                    "Fichier manquant",
                    f"Le fichier index.html est introuvable dans:\n{script_dir}"
                )
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le leaderboard web:\n{e}")
    
    def afficher(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
    
    def masquer(self):
        self.frame.pack_forget()


class ShooterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shooter Spatial")
        
        self.LARGEUR_PIXELS, self.HAUTEUR_PIXELS = obtenir_dimensions_ecran(root)
        self.TAILLE_CASE = 20
        
        # Hauteur du canvas de jeu : laisser place pour infos (120px) + boutons (60px)
        self.HAUTEUR_JEU = self.HAUTEUR_PIXELS - 180
        
        # Activer le redimensionnement (pour permettre le plein écran)
        self.root.resizable(True, True)
        self.root.geometry(f"{self.LARGEUR_PIXELS}x{self.HAUTEUR_PIXELS}")
        self.centrer_fenetre()
        
        # Détecter le redimensionnement de la fenêtre
        self.root.bind('<Configure>', self.sur_redimensionnement)
        self.derniere_taille = (self.LARGEUR_PIXELS, self.HAUTEUR_PIXELS)
        self.redimensionnement_en_cours = False
        
        # Volume de la musique (0.0 à 1.0)
        self.volume_musique = 0.3
        
        self.game_engine = GameEngine(
            largeur=self.LARGEUR_PIXELS // self.TAILLE_CASE,
            hauteur=self.HAUTEUR_JEU // self.TAILLE_CASE
        )
        
        self.score_manager = ScoreManager()
        self.nom_joueur = ""
        self.jeu_en_cours = False
        
        self.ennemis_detruits = 0
        self.niveau_difficulte = 1
        self.vitesse_actuelle = Config.VITESSE_INITIALE
        self.intervalle_spawn = Config.SPAWN_INITIAL
        
        self.musique = None
        self.timer_jeu = None
        self.timer_spawn = None
        self.timer_chrono = None
        self.temps_debut = 0
        
        self.etoiles = []
        self.creer_fond_anime()
        
        self.frame_jeu: tk.Frame | None = None
        self.canvas: tk.Canvas | None = None
        
        self.menu = MenuPrincipal(
            root, self.lancer_jeu, self.afficher_instructions,
            self.afficher_scores, self.LARGEUR_PIXELS, self.HAUTEUR_PIXELS
        )
        
        self.ecran_instructions = EcranInstructions(
            root, self.retour_menu,
            self.LARGEUR_PIXELS, self.HAUTEUR_PIXELS
        )
        
        self.ecran_scores = EcranScores(
            root, self.retour_menu, self.score_manager,
            self.LARGEUR_PIXELS, self.HAUTEUR_PIXELS
        )
        
        self.menu.afficher()
    
    def centrer_fenetre(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.LARGEUR_PIXELS) // 2
        y = (self.root.winfo_screenheight() - self.HAUTEUR_PIXELS) // 2
        self.root.geometry(f"{self.LARGEUR_PIXELS}x{self.HAUTEUR_PIXELS}+{x}+{y}")
    
    def sur_redimensionnement(self, event):
        """Gère le redimensionnement de la fenêtre"""
        # Ne traiter que les événements de la fenêtre principale
        if event.widget != self.root:
            return
        
        # Éviter les appels multiples pendant le redimensionnement
        if self.redimensionnement_en_cours:
            return
        
        nouvelle_largeur = event.width
        nouvelle_hauteur = event.height
        
        # Vérifier si la taille a vraiment changé
        if (nouvelle_largeur, nouvelle_hauteur) == self.derniere_taille:
            return
        
        # Limites minimales
        if nouvelle_largeur < 400 or nouvelle_hauteur < 600:
            return
        
        self.derniere_taille = (nouvelle_largeur, nouvelle_hauteur)
        self.redimensionnement_en_cours = True
        
        # Mettre à jour les dimensions
        self.LARGEUR_PIXELS = nouvelle_largeur
        self.HAUTEUR_PIXELS = nouvelle_hauteur
        self.HAUTEUR_JEU = self.HAUTEUR_PIXELS - 180
        
        # Recréer le fond animé avec les nouvelles dimensions
        self.etoiles = []
        self.creer_fond_anime()
        
        # Si en jeu, ajuster le canvas et le moteur
        if self.canvas and self.jeu_en_cours:
            self.canvas.config(width=self.LARGEUR_PIXELS, height=self.HAUTEUR_JEU)
            
            # Mettre à jour les dimensions du moteur de jeu
            nouvelle_largeur_jeu = self.LARGEUR_PIXELS // self.TAILLE_CASE
            nouvelle_hauteur_jeu = self.HAUTEUR_JEU // self.TAILLE_CASE
            
            # Ajuster la position du vaisseau si nécessaire
            ratio_x = nouvelle_largeur_jeu / self.game_engine.largeur
            ratio_y = nouvelle_hauteur_jeu / self.game_engine.hauteur
            
            self.game_engine.largeur = nouvelle_largeur_jeu
            self.game_engine.hauteur = nouvelle_hauteur_jeu
            self.game_engine.vaisseau.largeur_ecran = nouvelle_largeur_jeu
            self.game_engine.vaisseau.hauteur_ecran = nouvelle_hauteur_jeu
            
            # Mettre à jour la vitesse de base en fonction de la nouvelle largeur
            # Progression douce pour garder la précision
            self.game_engine.vaisseau.vitesse_base = min(2.5, 1.0 + max(0, nouvelle_largeur_jeu - 30) / 60.0)
            
            # Ajuster la position du vaisseau proportionnellement
            self.game_engine.vaisseau.x = self.game_engine.vaisseau.x * ratio_x
            self.game_engine.vaisseau.y = self.game_engine.vaisseau.y * ratio_y
            
            # S'assurer que le vaisseau reste dans les limites
            if self.game_engine.vaisseau.x < 0:
                self.game_engine.vaisseau.x = 0
            if self.game_engine.vaisseau.x > nouvelle_largeur_jeu - self.game_engine.vaisseau.largeur:
                self.game_engine.vaisseau.x = nouvelle_largeur_jeu - self.game_engine.vaisseau.largeur
            if self.game_engine.vaisseau.y > nouvelle_hauteur_jeu - self.game_engine.vaisseau.hauteur - 1:
                self.game_engine.vaisseau.y = nouvelle_hauteur_jeu - self.game_engine.vaisseau.hauteur - 1
        
        self.redimensionnement_en_cours = False
    
    def creer_fond_anime(self):
        # Adapter le nombre d'étoiles à la taille de l'écran
        nb_etoiles = min(150, max(50, (self.LARGEUR_PIXELS * self.HAUTEUR_JEU) // 4000))
        for i in range(nb_etoiles):
            x = random.randint(0, self.LARGEUR_PIXELS)
            y = random.randint(0, self.HAUTEUR_JEU)
            vitesse = random.uniform(0.3, 2.0)
            taille = random.randint(1, 3)
            couleur = random.choice(['white', '#ffffaa', '#aaaaff'])
            self.etoiles.append(EtoileAnimee(x, y, vitesse, taille, couleur, self.HAUTEUR_JEU, self.LARGEUR_PIXELS))
    
    def lancer_jeu(self):
        self.nom_joueur = simpledialog.askstring(
            "Nom", "Votre nom:", parent=self.root
        ) or "Joueur"
        
        self.menu.masquer()
        self.creer_interface_jeu()
        self.reinitialiser_jeu()
        self.demarrer_partie()
    
    def afficher_instructions(self):
        self.menu.masquer()
        self.ecran_instructions.afficher()
    
    def afficher_scores(self):
        self.menu.masquer()
        self.ecran_scores.afficher()
    
    def retour_menu(self):
        self.ecran_instructions.masquer()
        self.ecran_scores.masquer()
        if self.frame_jeu:
            self.frame_jeu.pack_forget()
        self.menu.afficher()
    
    def creer_interface_jeu(self):
        if self.frame_jeu:
            self.frame_jeu.destroy()
        
        taille_info = max(11, min(15, int(self.HAUTEUR_PIXELS / 55)))
        taille_bouton = max(9, min(12, int(self.HAUTEUR_PIXELS / 75)))
        
        self.frame_jeu = tk.Frame(self.root, bg='black')
        
        # INFOS EN HAUT (avant le canvas)
        frame_info = tk.Frame(self.frame_jeu, bg='black')
        frame_info.pack(fill=tk.X, padx=10, pady=5)
        
        # Première ligne : Score et Temps
        frame_ligne1 = tk.Frame(frame_info, bg='black')
        frame_ligne1.pack(fill=tk.X)
        
        self.label_score = tk.Label(
            frame_ligne1, text="Score: 0 | Niveau: 1",
            font=('Arial', taille_info, 'bold'),
            fg='#00ff88', bg='black'
        )
        self.label_score.pack(side=tk.LEFT, padx=5)
        
        self.label_temps = tk.Label(
            frame_ligne1, text="Temps: 0s",
            font=('Arial', taille_info, 'bold'),
            fg='#ffaa00', bg='black'
        )
        self.label_temps.pack(side=tk.RIGHT, padx=5)
        
        # Deuxième ligne : Vies
        frame_ligne2 = tk.Frame(frame_info, bg='black')
        frame_ligne2.pack(fill=tk.X, pady=3)
        
        self.label_vies = tk.Label(
            frame_ligne2, text="❤️ ❤️ ❤️",
            font=('Arial', taille_info + 2, 'bold'),
            fg='#ff4444', bg='black'
        )
        self.label_vies.pack(side=tk.LEFT, padx=5)
        
        # Troisième ligne : Bonus
        frame_bonus = tk.Frame(frame_info, bg='black')
        frame_bonus.pack(fill=tk.X, pady=2)
        
        self.label_bonus = tk.Label(
            frame_bonus, text="",
            font=('Arial', taille_info - 1, 'bold'),
            fg='#ffff00', bg='black',
            anchor='w'
        )
        self.label_bonus.pack(side=tk.LEFT, padx=5)
        
        # CANVAS DE JEU (au milieu)
        self.canvas = tk.Canvas(
            self.frame_jeu, width=self.LARGEUR_PIXELS,
            height=self.HAUTEUR_JEU, bg='black', highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # BOUTONS EN BAS (après le canvas)
        frame_boutons = tk.Frame(self.frame_jeu, bg='#0a0a0a')
        frame_boutons.pack(fill=tk.X, pady=8, padx=10)
        
        # Boutons de contrôle de la musique (gauche)
        frame_musique = tk.Frame(frame_boutons, bg='#0a0a0a')
        frame_musique.pack(side=tk.LEFT)
        
        self.bouton_musique = tk.Button(
            frame_musique, text="🔇 Musique OFF",
            command=self.toggle_musique,
            font=('Arial', taille_bouton, 'bold'),
            bg='#666666', fg='white',
            state=tk.DISABLED,
            activebackground='#777777',
            relief=tk.RAISED,
            bd=2,
            padx=15, pady=8, cursor='hand2'
        )
        self.bouton_musique.pack(side=tk.LEFT, padx=2)
        
        # Boutons volume
        self.bouton_volume_moins = tk.Button(
            frame_musique, text="🔉",
            command=self.diminuer_volume,
            font=('Arial', taille_bouton + 2),
            bg='#444444', fg='white',
            state=tk.DISABLED,
            activebackground='#555555',
            relief=tk.RAISED,
            bd=2,
            padx=8, pady=8, cursor='hand2'
        )
        self.bouton_volume_moins.pack(side=tk.LEFT, padx=2)
        
        self.label_volume = tk.Label(
            frame_musique, text="30%",
            font=('Arial', taille_bouton - 1, 'bold'),
            fg='#ffaa00', bg='#0a0a0a',
            width=4
        )
        self.label_volume.pack(side=tk.LEFT, padx=2)
        
        self.bouton_volume_plus = tk.Button(
            frame_musique, text="🔊",
            command=self.augmenter_volume,
            font=('Arial', taille_bouton + 2),
            bg='#444444', fg='white',
            state=tk.DISABLED,
            activebackground='#555555',
            relief=tk.RAISED,
            bd=2,
            padx=8, pady=8, cursor='hand2'
        )
        self.bouton_volume_plus.pack(side=tk.LEFT, padx=2)
        
        # Bouton quitter (droite)
        self.bouton_menu = tk.Button(
            frame_boutons, text="❌ Quitter le jeu",
            command=self.quitter_partie,
            font=('Arial', taille_bouton, 'bold'),
            bg='#ff4444', fg='white',
            activebackground='#dd2222',
            relief=tk.RAISED,
            bd=2,
            padx=20, pady=8, cursor='hand2'
        )
        self.bouton_menu.pack(side=tk.RIGHT, padx=5)
        
        self.frame_jeu.pack(fill=tk.BOTH, expand=True)
        self.configurer_evenements()
    
    def configurer_evenements(self):
        self.root.bind('<KeyPress>', self.touche_appuyee)
        self.root.bind('<KeyRelease>', self.touche_relachee)
        
        self.touches = {
            'Left': False, 'Right': False,
            'Up': False, 'Down': False, 'space': False
        }
    
    def touche_appuyee(self, event):
        if event.keysym in self.touches:
            self.touches[event.keysym] = True
        elif event.keysym.lower() == 'p':
            self.toggle_musique()
    
    def touche_relachee(self, event):
        if event.keysym in self.touches:
            self.touches[event.keysym] = False
    
    def reinitialiser_jeu(self):
        self.game_engine = GameEngine(
            largeur=self.LARGEUR_PIXELS // self.TAILLE_CASE,
            hauteur=self.HAUTEUR_JEU // self.TAILLE_CASE
        )
        
        self.ennemis_detruits = 0
        self.niveau_difficulte = 1
        self.vitesse_actuelle = Config.VITESSE_INITIALE
        self.intervalle_spawn = Config.SPAWN_INITIAL
        
        self.jeu_en_cours = False
        self.temps_debut = 0
        
        for key in self.touches:
            self.touches[key] = False
    
    def demarrer_partie(self):
        self.jeu_en_cours = True
        self.temps_debut = time.time()
        
        if PYGAME_AVAILABLE:
            try:
                self.musique = MusiqueThread(volume=self.volume_musique)
                self.musique.start()
                self.bouton_musique.config(
                    state=tk.NORMAL, 
                    text="🔊 Musique ON",
                    bg='#00aa44'
                )
                self.bouton_volume_moins.config(state=tk.NORMAL)
                self.bouton_volume_plus.config(state=tk.NORMAL)
                self.label_volume.config(text=f"{int(self.volume_musique * 100)}%")
            except Exception as e:
                print(f"⚠️ Impossible de démarrer la musique: {e}")
        
        self.boucle_jeu()
        self.spawn_ennemis()
        self.mettre_a_jour_chrono()
    
    def toggle_musique(self):
        if not self.musique:
            return
        
        if "🔊" in self.bouton_musique['text']:
            # Musique active -> on met en pause
            self.musique.pause()
            self.bouton_musique.config(
                text="🔇 Musique OFF",
                bg='#666666'
            )
            print("🔇 Musique mise en pause")
        else:
            # Musique en pause -> on reprend
            self.musique.reprendre()
            self.bouton_musique.config(
                text="🔊 Musique ON",
                bg='#00aa44'
            )
            print("🔊 Musique reprise")
    
    def augmenter_volume(self):
        if not self.musique:
            return
        
        self.volume_musique = min(1.0, self.volume_musique + 0.1)
        self.musique.set_volume(self.volume_musique)
        self.label_volume.config(text=f"{int(self.volume_musique * 100)}%")
        print(f"🔊 Volume: {int(self.volume_musique * 100)}%")
    
    def diminuer_volume(self):
        if not self.musique:
            return
        
        self.volume_musique = max(0.0, self.volume_musique - 0.1)
        self.musique.set_volume(self.volume_musique)
        self.label_volume.config(text=f"{int(self.volume_musique * 100)}%")
        print(f"🔉 Volume: {int(self.volume_musique * 100)}%")
    
    def quitter_partie(self):
        if self.jeu_en_cours:
            if not messagebox.askyesno("Quitter", "Quitter ? Score non enregistré"):
                return
        
        self.jeu_en_cours = False
        
        if self.timer_jeu:
            self.root.after_cancel(self.timer_jeu)
        if self.timer_spawn:
            self.root.after_cancel(self.timer_spawn)
        if self.timer_chrono:
            self.root.after_cancel(self.timer_chrono)
        
        if self.musique:
            self.musique.arreter()
            self.musique = None
        
        self.retour_menu()
    
    def mettre_a_jour_chrono(self):
        if not self.jeu_en_cours:
            return
        
        temps = int(time.time() - self.temps_debut)
        self.label_temps.config(text=f"Temps: {temps}s")
        self.timer_chrono = self.root.after(1000, self.mettre_a_jour_chrono)
    
    def spawn_ennemis(self):
        if not self.jeu_en_cours:
            return
        
        self.game_engine.ajouter_ennemi(self.vitesse_actuelle)
        
        if random.random() < Config.CHANCE_BONUS:
            self.game_engine.ajouter_bonus()
        
        self.timer_spawn = self.root.after(self.intervalle_spawn, self.spawn_ennemis)
    
    def augmenter_difficulte(self):
        if self.ennemis_detruits % 10 == 0 and self.ennemis_detruits > 0:
            self.niveau_difficulte += 1
            
            if self.vitesse_actuelle < Config.VITESSE_MAX:
                self.vitesse_actuelle += 0.1
            
            if self.intervalle_spawn > Config.SPAWN_MIN:
                self.intervalle_spawn = max(Config.SPAWN_MIN, self.intervalle_spawn - 200)
            
            print(f"\n🔥 NIVEAU {self.niveau_difficulte} ! Vitesse: {self.vitesse_actuelle:.1f} | Spawn: {self.intervalle_spawn}ms\n")
    
    def boucle_jeu(self):
        if not self.jeu_en_cours:
            return
        
        if self.touches['Left']:
            self.game_engine.vaisseau.deplacer_gauche()
        if self.touches['Right']:
            self.game_engine.vaisseau.deplacer_droite()
        if self.touches['Up']:
            self.game_engine.vaisseau.deplacer_haut()
        if self.touches['Down']:
            self.game_engine.vaisseau.deplacer_bas()
        if self.touches['space']:
            self.game_engine.tirer()
        
        ennemis_avant = sum(1 for e in self.game_engine.ennemis if e.actif)
        self.game_engine.mettre_a_jour()
        ennemis_apres = sum(1 for e in self.game_engine.ennemis if e.actif)
        
        if ennemis_apres < ennemis_avant:
            nb_tues = ennemis_avant - ennemis_apres
            self.ennemis_detruits += nb_tues
            print(f"💥 {nb_tues} ennemi(s) détruit(s) ! Total: {self.ennemis_detruits} | Score: {self.game_engine.score}")
            self.augmenter_difficulte()
        
        if self.game_engine.jeu_termine:
            self.fin_de_partie()
            return
        
        self.mettre_a_jour_interface()
        
        self.timer_jeu = self.root.after(50, self.boucle_jeu)
    
    def mettre_a_jour_interface(self):
        self.label_score.config(text=f"Score: {self.game_engine.score} | Niveau: {self.niveau_difficulte}")
        self.label_vies.config(text=" ".join(["❤️"] * self.game_engine.vaisseau.vies))
        self.label_temps.config(text=f"Temps: {int(time.time() - self.temps_debut)}s")
        
        # Afficher les bonus actifs
        bonus_txt = ""
        v = self.game_engine.vaisseau
        bonus_actifs = []
        
        if v.tir_triple:
            bonus_actifs.append("≡Triple")
        elif v.tir_double:
            bonus_actifs.append("=Double")
        
        if v.vitesse_bonus > 1.0:
            bonus_actifs.append(">>Vitesse")
        
        if v.cooldown_tir < 10:
            bonus_actifs.append("!!!Rapide")
        
        if bonus_actifs:
            bonus_txt = "⚡ Bonus actifs: " + " | ".join(bonus_actifs)
        
        self.label_bonus.config(text=bonus_txt)
        
        self.dessiner()
    
    def dessiner(self):
        self.canvas.delete('all')
        
        for etoile in self.etoiles:
            etoile.deplacer()
            self.canvas.create_oval(
                etoile.x - etoile.taille, etoile.y - etoile.taille,
                etoile.x + etoile.taille, etoile.y + etoile.taille,
                fill=etoile.couleur, outline=''
            )
        
        for b in self.game_engine.bonus:
            if b.actif:
                bx = int(b.x * self.TAILLE_CASE)
                by = int(b.y * self.TAILLE_CASE)
                t = self.TAILLE_CASE
                
                self.canvas.create_oval(
                    bx, by, bx + t, by + t,
                    fill=b.info['couleur'], outline='white', width=2
                )
                
                self.canvas.create_text(
                    bx + t//2, by + t//2,
                    text=b.info['icone'],
                    font=('Arial', 8, 'bold'), fill='black'
                )
        
        v = self.game_engine.vaisseau
        if v.actif:
            inv = self.game_engine.frame_count < v.invincible_jusqu_a
            
            x1 = int(v.x * self.TAILLE_CASE)
            y1 = int(v.y * self.TAILLE_CASE)
            w = v.largeur * self.TAILLE_CASE
            h = v.hauteur * self.TAILLE_CASE
            cx = x1 + w / 2
            
            if inv:
                couleur = '#ffff00'
            elif v.tir_triple:
                couleur = '#ff8800'
            elif v.tir_double:
                couleur = '#ffff00'
            else:
                couleur = '#00ffff'
            
            corps = [cx, y1, x1 + w*0.2, y1+h, x1 + w*0.8, y1+h]
            self.canvas.create_polygon(corps, fill=couleur, outline='white', width=2)
            
            aile_g = [x1+w*0.2, y1+h*0.5, x1, y1+h, x1+w*0.2, y1+h]
            self.canvas.create_polygon(aile_g, fill='#0088ff', outline='white')
            
            aile_d = [x1+w*0.8, y1+h*0.5, x1+w, y1+h, x1+w*0.8, y1+h]
            self.canvas.create_polygon(aile_d, fill='#0088ff', outline='white')
            
            self.canvas.create_oval(
                cx-3, y1+h*0.4-3, cx+3, y1+h*0.4+3,
                fill='white', outline='#00aaff'
            )
        
        for e in self.game_engine.ennemis:
            if e.actif:
                ex = int(e.x * self.TAILLE_CASE)
                ey = int(e.y * self.TAILLE_CASE)
                t = self.TAILLE_CASE
                
                self.canvas.create_oval(
                    ex, ey+t*0.3, ex+t, ey+t*0.7,
                    fill='#ff3333', outline='#ff8800', width=2
                )
        
        for p in self.game_engine.projectiles:
            if p.actif:
                px = int(p.x * self.TAILLE_CASE)
                py = int(p.y * self.TAILLE_CASE)
                w = p.largeur * self.TAILLE_CASE
                h = p.hauteur * self.TAILLE_CASE
                
                self.canvas.create_rectangle(
                    px, py, px+w, py+h,
                    fill='#ffff00', outline='#ffff00'
                )
    
    def fin_de_partie(self):
        self.jeu_en_cours = False
        
        if self.timer_jeu:
            self.root.after_cancel(self.timer_jeu)
        if self.timer_spawn:
            self.root.after_cancel(self.timer_spawn)
        if self.timer_chrono:
            self.root.after_cancel(self.timer_chrono)
        
        if self.musique:
            self.musique.arreter()
            self.musique = None
        
        temps = int(time.time() - self.temps_debut)
        m, s = temps // 60, temps % 60
        
        try:
            nouveau = self.score_manager.enregistrer_score(
                self.nom_joueur, self.game_engine.score
            )
            self.score_manager.exporter_html()
        except Exception as e:
            print(f"⚠️ Erreur lors de l'enregistrement du score: {e}")
            nouveau = False
        
        msg = (
            f"🎮 GAME OVER 🎮\n\n"
            f"Joueur: {self.nom_joueur}\n"
            f"Score: {self.game_engine.score} points\n"
            f"Niveau atteint: {self.niveau_difficulte}\n"
            f"Temps de jeu: {m:02d}:{s:02d}\n"
            f"Ennemis détruits: {self.ennemis_detruits}"
        )
        
        if nouveau:
            msg += "\n\n🏆 NOUVEAU RECORD PERSONNEL ! 🏆"
        
        # Afficher le message de fin
        messagebox.showinfo("Partie terminée", msg)
        
        # Créer une fenêtre de dialogue personnalisée
        dialog = tk.Toplevel(self.root)
        dialog.title("Que voulez-vous faire ?")
        dialog.geometry("450x250")
        dialog.configure(bg='#1a1a2e')
        dialog.resizable(False, False)
        
        # Centrer la fenêtre
        dialog.transient(self.root)
        dialog.grab_set()
        
        x = self.root.winfo_x() + (self.root.winfo_width() - 450) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 250) // 2
        dialog.geometry(f"450x250+{x}+{y}")
        
        # Label
        tk.Label(
            dialog,
            text="Que voulez-vous faire ?",
            font=('Arial', 16, 'bold'),
            fg='#00ff88',
            bg='#1a1a2e'
        ).pack(pady=25)
        
        # Frame pour les boutons principaux
        frame_btns = tk.Frame(dialog, bg='#1a1a2e')
        frame_btns.pack(pady=15)
        
        def rejouer():
            dialog.destroy()
            self.lancer_jeu()
        
        def voir_scores():
            dialog.destroy()
            self.retour_menu()
            self.afficher_scores()
        
        def retour():
            dialog.destroy()
            self.retour_menu()
        
        # Bouton Rejouer
        tk.Button(
            frame_btns,
            text="🔄 REJOUER",
            command=rejouer,
            font=('Arial', 13, 'bold'),
            bg='#00ff88',
            fg='black',
            activebackground='#00dd77',
            relief=tk.FLAT,
            width=16,
            height=2,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=8)
        
        # Bouton Voir Scores
        tk.Button(
            frame_btns,
            text="🏆 SCORES",
            command=voir_scores,
            font=('Arial', 13, 'bold'),
            bg='#ffd700',
            fg='black',
            activebackground='#ffbb00',
            relief=tk.FLAT,
            width=16,
            height=2,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=8)
        
        # Bouton Web (sous les principaux)
        def ouvrir_web():
            try:
                script_dir = Path(__file__).parent
                fichier_html = script_dir / "index.html"
                if fichier_html.exists():
                    webbrowser.open(f"file:///{fichier_html.as_posix()}")
                else:
                    messagebox.showwarning(
                        "Fichier manquant",
                        f"Le fichier index.html est introuvable dans:\n{script_dir}"
                    )
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ouvrir le navigateur:\n{e}")
        
        tk.Button(
            dialog,
            text="🌐 Web",
            command=ouvrir_web,
            font=('Arial', 12, 'bold'),
            bg='#00aaff',
            fg='white',
            activebackground='#0088dd',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2'
        ).pack(pady=(5, 2))
        
        # Bouton Menu (séparé en bas)
        tk.Button(
            dialog,
            text="◀ Menu Principal",
            command=retour,
            font=('Arial', 11),
            bg='#555555',
            fg='white',
            activebackground='#444444',
            relief=tk.FLAT,
            padx=25,
            pady=10,
            cursor='hand2'
        ).pack(pady=(2, 20))


def main():
    root = tk.Tk()
    app = ShooterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()