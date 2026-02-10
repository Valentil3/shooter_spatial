"""
Shooter Spatial - Version Console Optimisée
Version avec affichage fluide et adaptation automatique de la taille
"""

import os
import sys
import time
import random
import threading
import shutil
from pathlib import Path
from io import StringIO

# Import pour la gestion du clavier selon le système
if sys.platform == 'win32':
    import msvcrt
    import ctypes
    from ctypes import wintypes
else:
    import tty
    import termios
    import select

# Pour la musique
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

from game_classes import GameEngine, Bonus
from score_manager import ScoreManager


# ==============================================================================
# CONFIGURATION DE LA DIFFICULTÉ
# ==============================================================================

def configurer_terminal_windows():
    """Configure le terminal Windows en plein écran optimisé"""
    if sys.platform == 'win32':
        try:
            kernel32 = ctypes.windll.kernel32
            user32 = ctypes.windll.user32
            
            # Obtenir le handle de la console
            h = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            
            # Masquer le curseur pour un affichage plus propre
            class CONSOLE_CURSOR_INFO(ctypes.Structure):
                _fields_ = [("dwSize", wintypes.DWORD), ("bVisible", wintypes.BOOL)]
            
            cursor_info = CONSOLE_CURSOR_INFO()
            cursor_info.dwSize = 1
            cursor_info.bVisible = False
            kernel32.SetConsoleCursorInfo(h, ctypes.byref(cursor_info))
            
            # Obtenir le handle de la fenêtre console
            hwnd = kernel32.GetConsoleWindow()
            
            if hwnd:
                # Maximiser la fenêtre
                SW_MAXIMIZE = 3
                user32.ShowWindow(hwnd, SW_MAXIMIZE)
                
                # Forcer le focus
                user32.SetForegroundWindow(hwnd)
                
                # Attendre la maximisation
                time.sleep(0.5)
                
                # Obtenir les dimensions de l'écran
                screen_width = user32.GetSystemMetrics(0)  # SM_CXSCREEN
                screen_height = user32.GetSystemMetrics(1)  # SM_CYSCREEN
                
                # Calculer les dimensions du terminal en caractères
                # Approximation: 1 caractère ≈ 8 pixels largeur, 16 pixels hauteur
                cols = min(240, screen_width // 8)
                rows = min(90, screen_height // 16)
                
                # Définir le buffer avec ces dimensions
                coord = wintypes._COORD(cols, 9999)
                kernel32.SetConsoleScreenBufferSize(h, coord)
                
                # Redimensionner la fenêtre pour utiliser tout l'espace
                rect = wintypes.SMALL_RECT(0, 0, cols - 1, rows - 1)
                kernel32.SetConsoleWindowInfo(h, True, ctypes.byref(rect))
            
            # Activer les codes ANSI pour les couleurs
            mode = wintypes.DWORD()
            kernel32.GetConsoleMode(h, ctypes.byref(mode))
            kernel32.SetConsoleMode(h, mode.value | 0x0004)  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
            
            return True
        except Exception as e:
            print(f"⚠️  Impossible de configurer le plein écran: {e}")
            return False
    return False



def restaurer_terminal_windows():
    """Restaure l'affichage du curseur à la fin du jeu"""
    if sys.platform == 'win32':
        try:
            kernel32 = ctypes.windll.kernel32
            h = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            
            # Réafficher le curseur
            class CONSOLE_CURSOR_INFO(ctypes.Structure):
                _fields_ = [("dwSize", wintypes.DWORD), ("bVisible", wintypes.BOOL)]
            
            cursor_info = CONSOLE_CURSOR_INFO()
            cursor_info.dwSize = 25
            cursor_info.bVisible = True
            kernel32.SetConsoleCursorInfo(h, ctypes.byref(cursor_info))
        except:
            pass


def obtenir_taille_terminal():
    """Obtient la taille maximale du terminal pour le plein écran"""
    try:
        # Attendre que le terminal soit bien redimensionné
        time.sleep(0.2)
        colonnes, lignes = shutil.get_terminal_size()
        
        # Utiliser presque toute la surface disponible
        # Laisser de l'espace pour l'interface (score, commandes, etc.)
        largeur_jeu = max(100, colonnes - 4)  # Largeur maximale
        hauteur_jeu = max(40, lignes - 8)     # Hauteur maximale
        
        return largeur_jeu, hauteur_jeu
    except Exception as e:
        print(f"⚠️  Erreur détection taille: {e}")
        # Valeurs par défaut pour grand écran
        return 200, 50


class ConfigDifficulte:
    """Configuration centralisée de la difficulté du jeu"""
    
    # ========== VITESSE DES ENNEMIS ==========
    VITESSE_INITIALE = 0.3
    VITESSE_MAX = 2.0
    
    # ========== APPARITION DES ENNEMIS ==========
    SPAWN_INITIAL = 2.0
    SPAWN_MIN = 0.8
    
    # ========== PROGRESSION ==========
    ENNEMIS_PAR_NIVEAU = 5
    ENNEMIS_PAR_PALIER = 3
    
    # ========== BONUS ==========
    CHANCE_BONUS = 0.3
    INTERVALLE_BONUS_MIN = 8.0
    INTERVALLE_BONUS_MAX = 15.0
    
    # ========== GAMEPLAY ==========
    VIES_DEPART = 3
    VIES_MAX = 5
    INVINCIBILITE_FRAMES = 20
    
    # ========== TIR ==========
    COOLDOWN_TIR_NORMAL = 10
    COOLDOWN_TIR_RAPIDE = 5
    
    # ========== PERFORMANCE ==========
    FPS_CIBLE = 30
    VITESSE_MAJ = 1.0 / FPS_CIBLE
    VITESSE_INPUT = 0.01


# ==============================================================================
# GESTION DU CLAVIER MULTI-PLATEFORME
# ==============================================================================

class ClavierNonBloquant:
    """Gestion du clavier en mode non-bloquant avec support des flèches et touches maintenues"""
    
    def __init__(self):
        self.is_windows = sys.platform == 'win32'
        self.touches_maintenues = set()  # Ensemble des touches actuellement pressées
        if not self.is_windows:
            self.fd = sys.stdin.fileno()
            self.old_settings = termios.tcgetattr(self.fd)
    
    def __enter__(self):
        """Active le mode non-bloquant"""
        if not self.is_windows:
            tty.setcbreak(self.fd)
        return self
    
    def __exit__(self, *args):
        """Désactive le mode non-bloquant"""
        if not self.is_windows:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
    
    def lire_touche(self):
        """Lit une touche sans bloquer - supporte ZQSD et flèches"""
        if self.is_windows:
            # Windows
            if msvcrt.kbhit():
                char = msvcrt.getch()
                
                # Touche spéciale (flèches)
                if char in (b'\x00', b'\xe0'):
                    if msvcrt.kbhit():
                        code = msvcrt.getch()
                        # Codes des flèches sur Windows
                        if code == b'H':  # Haut
                            return 'UP'
                        elif code == b'P':  # Bas
                            return 'DOWN'
                        elif code == b'K':  # Gauche
                            return 'LEFT'
                        elif code == b'M':  # Droite
                            return 'RIGHT'
                
                # Touche normale
                try:
                    return char.decode('utf-8', errors='ignore').lower()
                except:
                    return None
        else:
            # Unix/Linux/Mac
            if select.select([sys.stdin], [], [], 0)[0]:
                char = sys.stdin.read(1)
                
                # Séquence d'échappement (flèches)
                if char == '\x1b':
                    # Lire les 2 caractères suivants
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        char2 = sys.stdin.read(1)
                        if char2 == '[':
                            if select.select([sys.stdin], [], [], 0.1)[0]:
                                char3 = sys.stdin.read(1)
                                # Codes des flèches sur Unix
                                if char3 == 'A':  # Haut
                                    return 'UP'
                                elif char3 == 'B':  # Bas
                                    return 'DOWN'
                                elif char3 == 'D':  # Gauche
                                    return 'LEFT'
                                elif char3 == 'C':  # Droite
                                    return 'RIGHT'
                    return '\x1b'  # ESC seul
                
                return char.lower()
        return None


# ==============================================================================
# THREADS POUR L'ANIMATION ET LA MUSIQUE
# ==============================================================================

class MusiqueThread(threading.Thread):
    """Thread pour la musique de fond (avec pygame si disponible)"""
    
    def __init__(self, fichier_musique="musique.mp3"):
        super().__init__(daemon=True)
        self.actif = True
        self.en_pause = False
        self.notes = ["♪", "♫", "♬", "♩"]
        self.index = 0
        # Utiliser un chemin absolu basé sur l'emplacement du script
        script_dir = Path(__file__).parent
        self.fichier_musique = script_dir / fichier_musique if not Path(fichier_musique).is_absolute() else Path(fichier_musique)
        self.musique_chargee = False
        
        # Essayer de charger la musique avec pygame
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
                if self.fichier_musique.exists():
                    pygame.mixer.music.load(str(self.fichier_musique))
                    pygame.mixer.music.set_volume(0.3)
                    self.musique_chargee = True
                else:
                    # Chercher d'autres fichiers audio dans le même dossier
                    script_dir = Path(__file__).parent
                    for fichier in ["musique.mp3"]:
                        chemin_complet = script_dir / fichier
                        if chemin_complet.exists():
                            pygame.mixer.music.load(str(chemin_complet))
                            pygame.mixer.music.set_volume(0.3)
                            self.musique_chargee = True
                            self.fichier_musique = chemin_complet
                            break
            except Exception as e:
                print(f"⚠️  Impossible de charger la musique : {e}")
    
    def run(self):
        """Boucle de musique"""
        # Démarrer la musique pygame si disponible
        if PYGAME_AVAILABLE and self.musique_chargee:
            try:
                pygame.mixer.music.play(-1)  # -1 = boucle infinie
            except:
                pass
        
        # Animation visuelle
        while self.actif:
            if not self.en_pause:
                self.index = (self.index + 1) % len(self.notes)
            time.sleep(0.5)
    
    def pause(self):
        """Met la musique en pause"""
        self.en_pause = True
        if PYGAME_AVAILABLE and self.musique_chargee:
            try:
                pygame.mixer.music.pause()
            except:
                pass
    
    def reprendre(self):
        """Reprend la musique"""
        self.en_pause = False
        if PYGAME_AVAILABLE and self.musique_chargee:
            try:
                pygame.mixer.music.unpause()
            except:
                pass
    
    def arreter(self):
        """Arrête la musique"""
        self.actif = False
        if PYGAME_AVAILABLE and self.musique_chargee:
            try:
                pygame.mixer.music.stop()
            except:
                pass
    
    def obtenir_note(self):
        """Obtient la note actuelle"""
        if self.en_pause:
            return "🔇"
        elif PYGAME_AVAILABLE and self.musique_chargee:
            return f"{self.notes[self.index]} 🎵"
        else:
            return self.notes[self.index]


class SpawnerThread(threading.Thread):
    """Thread pour faire apparaître les ennemis"""
    
    def __init__(self, game_engine: GameEngine):
        super().__init__(daemon=True)
        self.game_engine = game_engine
        self.actif = True
        self.intervalle = ConfigDifficulte.SPAWN_INITIAL
        self.vitesse = ConfigDifficulte.VITESSE_INITIALE
    
    def run(self):
        """Fait apparaître des ennemis périodiquement"""
        while self.actif and not self.game_engine.jeu_termine:
            time.sleep(self.intervalle)
            if not self.game_engine.jeu_termine:
                self.game_engine.ajouter_ennemi(self.vitesse)
    
    def ajuster_difficulte(self, ennemis_detruits):
        """Ajuste la difficulté en fonction du nombre d'ennemis détruits"""
        niveau = 1 + (ennemis_detruits // ConfigDifficulte.ENNEMIS_PAR_NIVEAU)
        
        # Augmenter la vitesse progressivement
        palier = ennemis_detruits // ConfigDifficulte.ENNEMIS_PAR_PALIER
        multiplicateur = 1.0 + (palier * 0.08)
        self.vitesse = min(
            ConfigDifficulte.VITESSE_INITIALE * multiplicateur, 
            ConfigDifficulte.VITESSE_MAX
        )
        
        # Réduire l'intervalle de spawn
        reduction = (niveau - 1) * 0.3
        self.intervalle = max(
            ConfigDifficulte.SPAWN_MIN, 
            ConfigDifficulte.SPAWN_INITIAL - reduction
        )
    
    def arreter(self):
        """Arrête le spawner"""
        self.actif = False


class BonusSpawnerThread(threading.Thread):
    """Thread pour faire apparaître les bonus"""
    
    def __init__(self, game_engine: GameEngine):
        super().__init__(daemon=True)
        self.game_engine = game_engine
        self.actif = True
    
    def run(self):
        """Fait apparaître des bonus aléatoirement"""
        while self.actif and not self.game_engine.jeu_termine:
            # Attendre un intervalle aléatoire
            temps_attente = random.uniform(
                ConfigDifficulte.INTERVALLE_BONUS_MIN,
                ConfigDifficulte.INTERVALLE_BONUS_MAX
            )
            time.sleep(temps_attente)
            
            if not self.game_engine.jeu_termine:
                # Chance de faire apparaître un bonus
                if random.random() < ConfigDifficulte.CHANCE_BONUS:
                    self.game_engine.ajouter_bonus()
    
    def arreter(self):
        """Arrête le spawner de bonus"""
        self.actif = False


# ==============================================================================
# AFFICHAGE
# ==============================================================================

# Codes couleur ANSI
class Couleur:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Couleurs de texte
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    
    # Couleurs de fond
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_BLUE = '\033[44m'


def nettoyer_ecran():
    """Nettoie l'écran du terminal"""
    if sys.platform == 'win32':
        os.system('cls')
    else:
        # Utiliser les codes ANSI pour un effacement plus rapide
        print('\033[2J\033[H', end='', flush=True)


def afficher_grille(game_engine: GameEngine, musique: MusiqueThread, ennemis_detruits: int, temps_debut: float):
    """Affiche la grille de jeu - version optimisée avec buffer pour éviter le clignotement"""
    
    # Construire tout l'affichage dans un buffer
    buffer = StringIO()
    
    # En-tête simplifié
    buffer.write(f"{Couleur.BOLD}{Couleur.YELLOW}=== SHOOTER SPATIAL ==={Couleur.RESET}\n")
    
    grille = game_engine.obtenir_grille_console()
    
    # Bordure supérieure
    buffer.write(f"{Couleur.CYAN}+{'─' * game_engine.largeur}+{Couleur.RESET}\n")
    
    # Vaisseau invincible ?
    invincible = game_engine.frame_count <= game_engine.vaisseau.invincible_jusqu_a
    
    # Grille
    for ligne in grille:
        buffer.write(f"{Couleur.CYAN}|{Couleur.RESET}")
        for char in ligne:
            if char == '^':
                # Vaisseau
                if invincible and (game_engine.frame_count % 4) < 2:
                    buffer.write(f"{Couleur.YELLOW}{Couleur.BOLD}^{Couleur.RESET}")
                else:
                    couleur = Couleur.CYAN
                    if game_engine.vaisseau.tir_triple:
                        couleur = Couleur.RED
                    elif game_engine.vaisseau.tir_double:
                        couleur = Couleur.YELLOW
                    buffer.write(f"{couleur}{Couleur.BOLD}^{Couleur.RESET}")
            elif char == 'O':
                # Ennemi
                buffer.write(f"{Couleur.RED}{Couleur.BOLD}O{Couleur.RESET}")
            elif char == '|':
                # Projectile
                buffer.write(f"{Couleur.YELLOW}{Couleur.BOLD}|{Couleur.RESET}")
            elif char in ['+', '>', '=', '≡', '!']:
                # Bonus
                buffer.write(f"{Couleur.CYAN}{Couleur.BOLD}*{Couleur.RESET}")
            else:
                buffer.write(' ')
        buffer.write(f"{Couleur.CYAN}|{Couleur.RESET}\n")
    
    # Bordure inférieure
    buffer.write(f"{Couleur.CYAN}+{'─' * game_engine.largeur}+{Couleur.RESET}\n")
    
    # Informations de jeu (sur une ligne compacte)
    vies_str = "V:" + ("*" * game_engine.vaisseau.vies) if game_engine.vaisseau.vies > 0 else "DEAD"
    temps_ecoule = int(time.time() - temps_debut)
    minutes = temps_ecoule // 60
    secondes = temps_ecoule % 60
    niveau = 1 + (ennemis_detruits // ConfigDifficulte.ENNEMIS_PAR_NIVEAU)
    
    buffer.write(f"{Couleur.GREEN}Score: {game_engine.score:4d}{Couleur.RESET} | ")
    buffer.write(f"{Couleur.MAGENTA}Niv: {niveau}{Couleur.RESET} | ")
    buffer.write(f"{Couleur.RED}{vies_str}{Couleur.RESET} | ")
    buffer.write(f"{Couleur.YELLOW}T: {minutes:02d}:{secondes:02d}{Couleur.RESET} | ")
    buffer.write(f"{Couleur.BLUE}E: {len([e for e in game_engine.ennemis if e.actif]):2d}{Couleur.RESET}\n")
    
    # Bonus actifs (si présents)
    bonus_actifs = []
    for type_bonus in game_engine.vaisseau.bonus_actif_jusqu_a.keys():
        nom = Bonus.TYPES[type_bonus]["nom"]
        bonus_actifs.append(nom)
    
    if bonus_actifs:
        buffer.write(f"{Couleur.MAGENTA}Bonus: {', '.join(bonus_actifs)}{Couleur.RESET} | ")
    
    # Musique
    if PYGAME_AVAILABLE:
        note = "♪" if not musique.en_pause else "X"
        buffer.write(f"Musique: {note}")
    
    buffer.write("\n")
    
    # Commandes (simplifié)
    buffer.write(f"{Couleur.GRAY}[ZQSD/Fleches] Bouger [ESPACE] Tir [P] Musique [X] Quitter{Couleur.RESET}\n")
    
    # Message d'invincibilité
    if invincible:
        buffer.write(f"{Couleur.YELLOW}*** INVINCIBLE ***{Couleur.RESET}\n")
    
    # Afficher tout d'un coup (évite le clignotement)
    output = buffer.getvalue()
    
    # Sur Windows, utiliser cls, sinon utiliser les codes ANSI
    if sys.platform == 'win32':
        os.system('cls')
        print(output, end='', flush=True)
    else:
        # Effacer l'écran et repositionner le curseur
        # \033[2J efface l'écran, \033[H repositionne en haut à gauche
        print('\033[2J\033[H' + output, end='', flush=True)


# ==============================================================================
# BOUCLE PRINCIPALE
# ==============================================================================

def boucle_jeu(game_engine: GameEngine, nom_joueur: str):
    """Boucle principale du jeu - version optimisée"""
    
    # Appliquer les paramètres de configuration au vaisseau
    game_engine.vaisseau.cooldown_tir = ConfigDifficulte.COOLDOWN_TIR_NORMAL
    
    # Threads
    musique = MusiqueThread()
    spawner = SpawnerThread(game_engine)
    bonus_spawner = BonusSpawnerThread(game_engine)
    
    musique.start()
    spawner.start()
    bonus_spawner.start()
    
    temps_debut = time.time()
    ennemis_detruits = 0
    musique_en_pause = False
    
    # Écran de démarrage
    nettoyer_ecran()
    print(f"\n  {Couleur.GREEN}{Couleur.BOLD}Bienvenue {nom_joueur} !{Couleur.RESET}")
    print(f"  {Couleur.YELLOW}Taille du jeu adaptée: {game_engine.largeur}×{game_engine.hauteur}{Couleur.RESET}")
    print(f"\n  {Couleur.CYAN}Démarrage dans 2 secondes...{Couleur.RESET}")
    time.sleep(2)
    
    # Clavier non-bloquant
    with ClavierNonBloquant() as clavier:
        derniere_update = time.time()
        derniere_frame = time.time()
        
        while not game_engine.jeu_termine:
            maintenant = time.time()
            delta = maintenant - derniere_frame
            
            # Contrôler le framerate
            if delta >= ConfigDifficulte.VITESSE_MAJ:
                derniere_frame = maintenant
                
                # Mise à jour du jeu
                ennemis_avant = len([e for e in game_engine.ennemis if e.actif])
                game_engine.mettre_a_jour()
                
                # Ajuster le cooldown de tir selon les bonus actifs
                if "tir_rapide" in game_engine.vaisseau.bonus_actif_jusqu_a:
                    game_engine.vaisseau.cooldown_tir = ConfigDifficulte.COOLDOWN_TIR_RAPIDE
                else:
                    game_engine.vaisseau.cooldown_tir = ConfigDifficulte.COOLDOWN_TIR_NORMAL
                
                ennemis_apres = len([e for e in game_engine.ennemis if e.actif])
                
                if ennemis_apres < ennemis_avant:
                    ennemis_tues = ennemis_avant - ennemis_apres
                    ennemis_detruits += ennemis_tues
                    spawner.ajuster_difficulte(ennemis_detruits)
                
                # Afficher l'état
                afficher_grille(game_engine, musique, ennemis_detruits, temps_debut)
            
            # Lire les touches (sans bloquer)
            touche = clavier.lire_touche()
            
            if touche:
                # Déplacements (ZQSD ou flèches)
                if touche == 'q' or touche == 'LEFT':
                    game_engine.vaisseau.deplacer_gauche()
                elif touche == 'd' or touche == 'RIGHT':
                    game_engine.vaisseau.deplacer_droite()
                elif touche == 'z' or touche == 'UP':
                    game_engine.vaisseau.deplacer_haut()
                elif touche == 's' or touche == 'DOWN':
                    game_engine.vaisseau.deplacer_bas()
                # Tir
                elif touche == ' ':
                    game_engine.tirer()
                # Musique
                elif touche == 'p':
                    musique_en_pause = not musique_en_pause
                    if musique_en_pause:
                        musique.pause()
                    else:
                        musique.reprendre()
                # Quitter
                elif touche == 'x' or touche == '\x1b':
                    game_engine.jeu_termine = True
                    break
            
            # Petit délai pour éviter de surcharger le CPU
            time.sleep(ConfigDifficulte.VITESSE_INPUT)
    
    # Arrêter les threads
    musique.arreter()
    spawner.arreter()
    bonus_spawner.arreter()
    
    # Affichage final
    nettoyer_ecran()
    afficher_grille(game_engine, musique, ennemis_detruits, temps_debut)
    
    temps_total = int(time.time() - temps_debut)
    minutes = temps_total // 60
    secondes = temps_total % 60
    
    print()
    print(f"  {Couleur.BOLD}{Couleur.CYAN}╔{'═' * 50}╗{Couleur.RESET}")
    if game_engine.vaisseau.vies > 0:
        print(f"  {Couleur.BOLD}{Couleur.CYAN}║{Couleur.YELLOW}          PARTIE TERMINÉE - VICTOIRE ! 🎉          {Couleur.CYAN}║{Couleur.RESET}")
    else:
        print(f"  {Couleur.BOLD}{Couleur.CYAN}║{Couleur.RED}            GAME OVER - DÉFAITE 💀               {Couleur.CYAN}║{Couleur.RESET}")
    print(f"  {Couleur.BOLD}{Couleur.CYAN}╚{'═' * 50}╝{Couleur.RESET}")
    print()
    print(f"  {Couleur.GREEN}Joueur:{Couleur.RESET} {Couleur.BOLD}{nom_joueur}{Couleur.RESET}")
    print(f"  {Couleur.GREEN}Score final:{Couleur.RESET} {Couleur.BOLD}{game_engine.score}{Couleur.RESET} points")
    print(f"  {Couleur.MAGENTA}Niveau atteint:{Couleur.RESET} {Couleur.BOLD}{1 + (ennemis_detruits // ConfigDifficulte.ENNEMIS_PAR_NIVEAU)}{Couleur.RESET}")
    print(f"  {Couleur.YELLOW}Temps de jeu:{Couleur.RESET} {Couleur.BOLD}{minutes:02d}:{secondes:02d}{Couleur.RESET}")
    print(f"  {Couleur.BLUE}Ennemis détruits:{Couleur.RESET} {Couleur.BOLD}{ennemis_detruits}{Couleur.RESET}")
    print()


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Fonction principale"""
    
    # Configurer le terminal Windows (plein écran)
    configurer_terminal_windows()
    
    nettoyer_ecran()
    
    # Obtenir la taille du terminal après maximisation
    largeur, hauteur = obtenir_taille_terminal()
    
    print(f"{Couleur.BOLD}{Couleur.CYAN}")
    print("╔═════════════════════════════════════════════════════════════╗")
    print("║                                                             ║")
    print("║          🚀  SHOOTER SPATIAL - CONSOLE  🚀                  ║")
    print("║                    MODE PLEIN ÉCRAN                         ║")
    print("║                                                             ║")
    print("╚═════════════════════════════════════════════════════════════╝")
    print(f"{Couleur.RESET}")
    print()
    
    if not PYGAME_AVAILABLE:
        print(f"{Couleur.YELLOW}⚠️  pygame non installé - pas de musique{Couleur.RESET}")
        print(f"{Couleur.GRAY}   Pour installer : pip install pygame{Couleur.RESET}")
        print()
    
    print(f"{Couleur.CYAN}Taille du jeu: {largeur}×{hauteur} (plein écran adapté){Couleur.RESET}")
    print()
    
    # Demander le nom du joueur
    nom_joueur = input(f"{Couleur.GREEN}Entrez votre nom:{Couleur.RESET} ").strip()
    if not nom_joueur:
        nom_joueur = "Joueur"
    
    # Charger les scores
    score_manager = ScoreManager()
    meilleur_score = score_manager.obtenir_meilleur_score(nom_joueur)
    
    if meilleur_score > 0:
        print(f"\n{Couleur.YELLOW}Votre meilleur score:{Couleur.RESET} {Couleur.BOLD}{meilleur_score}{Couleur.RESET} points")
    
    # Créer le jeu avec adaptation automatique de la taille
    game_engine = GameEngine(largeur=largeur, hauteur=hauteur)
    
    # Augmenter la vitesse du vaisseau pour une meilleure jouabilité console
    game_engine.vaisseau.vitesse_base = min(3.5, game_engine.vaisseau.vitesse_base * 1.5)
    
    # Lancer le jeu
    boucle_jeu(game_engine, nom_joueur)
    
    # Enregistrer le score
    try:
        nouveau_record = score_manager.enregistrer_score(nom_joueur, game_engine.score)
        
        if nouveau_record:
            print(f"  {Couleur.BOLD}{Couleur.YELLOW}🏆 NOUVEAU RECORD PERSONNEL ! 🏆{Couleur.RESET}")
            print()
    except Exception as e:
        print(f"  {Couleur.RED}Erreur lors de l'enregistrement du score: {e}{Couleur.RESET}")
    
    # Afficher le classement
    print()
    print(f"  {Couleur.BOLD}{Couleur.CYAN}╔{'═' * 50}╗{Couleur.RESET}")
    print(f"  {Couleur.BOLD}{Couleur.CYAN}║{Couleur.YELLOW}          CLASSEMENT DES MEILLEURS JOUEURS          {Couleur.CYAN}║{Couleur.RESET}")
    print(f"  {Couleur.BOLD}{Couleur.CYAN}╚{'═' * 50}╝{Couleur.RESET}")
    print()
    
    classement = score_manager.obtenir_classement(10)
    
    if classement:
        for i, (joueur, score) in enumerate(classement, 1):
            if i == 1:
                medaille = f"{Couleur.YELLOW}🥇{Couleur.RESET}"
                couleur = Couleur.YELLOW
            elif i == 2:
                medaille = f"{Couleur.WHITE}🥈{Couleur.RESET}"
                couleur = Couleur.WHITE
            elif i == 3:
                medaille = f"{Couleur.RED}🥉{Couleur.RESET}"
                couleur = Couleur.RED
            else:
                medaille = f"{Couleur.GRAY}{i:2d}.{Couleur.RESET}"
                couleur = Couleur.GREEN
            
            print(f"  {medaille} {couleur}{Couleur.BOLD}{joueur:.<30}{Couleur.RESET} {couleur}{score:>6}{Couleur.RESET} pts")
    else:
        print(f"  {Couleur.GRAY}Aucun score enregistré.{Couleur.RESET}")
    
    print()
    print(f"  {Couleur.BOLD}{Couleur.CYAN}╔{'═' * 50}╗{Couleur.RESET}")
    print(f"  {Couleur.BOLD}{Couleur.CYAN}║{Couleur.GREEN}              Merci d'avoir joué ! 🎮              {Couleur.CYAN}║{Couleur.RESET}")
    print(f"  {Couleur.BOLD}{Couleur.CYAN}╚{'═' * 50}╝{Couleur.RESET}")
    print()
    
    # Exporter le leaderboard HTML
    try:
        score_manager.exporter_html()
        print(f"  {Couleur.GREEN}✅ Leaderboard HTML mis à jour !{Couleur.RESET}")
    except Exception as e:
        print(f"  {Couleur.RED}⚠️  Erreur lors de l'export HTML: {e}{Couleur.RESET}")
    
    print()
    
    # Restaurer le curseur à la fin
    restaurer_terminal_windows()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        nettoyer_ecran()
        restaurer_terminal_windows()
        print(f"\n  {Couleur.YELLOW}Jeu interrompu par l'utilisateur.{Couleur.RESET}\n")
    except Exception as e:
        restaurer_terminal_windows()
        print(f"\n  {Couleur.RED}Erreur: {e}{Couleur.RESET}\n")
        import traceback
        traceback.print_exc()