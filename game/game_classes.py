"""
Classes principales du jeu Shooter Spatial
Version complète avec système de bonus corrigé
"""

from typing import List
import random


# ==============================================================================
# CLASSE DE BASE
# ==============================================================================

class ObjetVolant:
    """
    Classe de base pour tous les objets volants du jeu
    
    Tous les objets du jeu (vaisseau, ennemis, projectiles, bonus)
    héritent de cette classe de base.
    
    Attributs :
        x, y (float) : Position de l'objet sur la grille
        largeur, hauteur (float) : Dimensions de l'objet
        actif (bool) : Indique si l'objet est encore dans le jeu
    """
    
    def __init__(self, x: float, y: float, largeur: float = 1, hauteur: float = 1):
        """Initialise un objet volant avec sa position et ses dimensions"""
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.actif = True
    
    def deplacer(self, dx: float, dy: float):
        """Déplace l'objet de dx, dy"""
        self.x += dx
        self.y += dy
    
    def collision_avec(self, autre: 'ObjetVolant') -> bool:
        """Vérifie si cet objet touche un autre objet"""
        marge = 0.5
        
        return (self.x - marge < autre.x + autre.largeur and
                self.x + self.largeur + marge > autre.x and
                self.y - marge < autre.y + autre.hauteur and
                self.y + self.hauteur + marge > autre.y)


# ==============================================================================
# VAISSEAU DU JOUEUR
# ==============================================================================

class Vaisseau(ObjetVolant):
    """
    Vaisseau contrôlé par le joueur
    
    Le vaisseau possède :
    - 3 vies de départ (max 5)
    - Vitesse adaptative selon la taille de l'écran
    - Système de tir avec cooldown
    - Système de bonus temporaires (vitesse, tir double/triple, tir rapide)
    - Invincibilité temporaire après avoir perdu une vie
    """
    
    def __init__(self, x: float, y: float, largeur_ecran: int, hauteur_ecran: int):
        """Initialise le vaisseau avec position et dimensions d'écran"""
        super().__init__(x, y, largeur=2, hauteur=1)
        self.largeur_ecran = largeur_ecran
        self.hauteur_ecran = hauteur_ecran
        self.vies = 3
        self.invincible_jusqu_a = 0
        
        # Facteur de vitesse adapté à la taille de l'écran
        # Progression plus douce pour garder la précision sur grand écran
        # Écran 30 cases → vitesse 1.0
        # Écran 60 cases → vitesse 1.5
        # Écran 90 cases → vitesse 2.0
        # Formule : 1.0 + (largeur - 30) / 60, plafonné à 2.5
        self.vitesse_base = min(2.5, 1.0 + max(0, largeur_ecran - 30) / 60.0)
        
        # Système de tir
        self.dernier_tir = 0
        self.cooldown_tir = 10  # frames entre chaque tir
        
        # Bonus actifs
        self.vitesse_bonus = 1.0
        self.tir_double = False
        self.tir_triple = False
        self.bonus_actif_jusqu_a = {}
    
    def deplacer_gauche(self):
        """Déplace le vaisseau vers la gauche"""
        if self.x > 0:
            self.deplacer(-1 * self.vitesse_base * self.vitesse_bonus, 0)
    
    def deplacer_droite(self):
        """Déplace le vaisseau vers la droite"""
        if self.x < self.largeur_ecran - self.largeur:
            self.deplacer(1 * self.vitesse_base * self.vitesse_bonus, 0)
    
    def deplacer_haut(self):
        """Déplace le vaisseau vers le haut"""
        if self.y > self.hauteur_ecran // 2:
            self.deplacer(0, -1 * self.vitesse_base * self.vitesse_bonus)
    
    def deplacer_bas(self):
        """Déplace le vaisseau vers le bas"""
        if self.y < self.hauteur_ecran - self.hauteur - 1:
            self.deplacer(0, 1 * self.vitesse_base * self.vitesse_bonus)
    
    def peut_tirer(self, frame_actuelle: int) -> bool:
        """Vérifie si le vaisseau peut tirer"""
        return frame_actuelle - self.dernier_tir >= self.cooldown_tir
    
    def tirer(self, frame_actuelle: int) -> List['Projectile']:
        """Crée un ou plusieurs projectiles selon les bonus actifs"""
        if not self.peut_tirer(frame_actuelle):
            return []
        
        self.dernier_tir = frame_actuelle
        projectiles = []
        
        centre_x = self.x + self.largeur / 2
        
        if self.tir_triple:
            projectiles.append(Projectile(centre_x - 1, self.y - 1))
            projectiles.append(Projectile(centre_x, self.y - 1))
            projectiles.append(Projectile(centre_x + 1, self.y - 1))
        elif self.tir_double:
            projectiles.append(Projectile(centre_x - 0.5, self.y - 1))
            projectiles.append(Projectile(centre_x + 0.5, self.y - 1))
        else:
            projectiles.append(Projectile(centre_x, self.y - 1))
        
        return projectiles
    
    def perdre_vie(self):
        """Enlève une vie au vaisseau"""
        self.vies -= 1
        return self.vies <= 0
    
    def gagner_vie(self):
        """Ajoute une vie (max 5)"""
        if self.vies < 5:
            self.vies += 1
    
    def activer_bonus(self, type_bonus: str, frame_actuelle: int, duree: int = 300):
        """Active un bonus pendant une durée donnée"""
        if type_bonus == "vitesse":
            self.vitesse_bonus = 1.5
            self.bonus_actif_jusqu_a["vitesse"] = frame_actuelle + duree
        elif type_bonus == "tir_double":
            self.tir_double = True
            self.tir_triple = False
            self.bonus_actif_jusqu_a["tir_double"] = frame_actuelle + duree
        elif type_bonus == "tir_triple":
            self.tir_triple = True
            self.tir_double = False
            self.bonus_actif_jusqu_a["tir_triple"] = frame_actuelle + duree
        elif type_bonus == "tir_rapide":
            self.cooldown_tir = 5
            self.bonus_actif_jusqu_a["tir_rapide"] = frame_actuelle + duree
    
    def mettre_a_jour_bonus(self, frame_actuelle: int):
        """Désactive les bonus expirés"""
        bonus_a_retirer = []
        
        for type_bonus, frame_fin in self.bonus_actif_jusqu_a.items():
            if frame_actuelle >= frame_fin:
                bonus_a_retirer.append(type_bonus)
                
                if type_bonus == "vitesse":
                    self.vitesse_bonus = 1.0
                elif type_bonus in ["tir_double", "tir_triple"]:
                    self.tir_double = False
                    self.tir_triple = False
                elif type_bonus == "tir_rapide":
                    self.cooldown_tir = 10
        
        for type_bonus in bonus_a_retirer:
            del self.bonus_actif_jusqu_a[type_bonus]


# ==============================================================================
# ENNEMI
# ==============================================================================

class Ennemi(ObjetVolant):
    """Ennemi qui descend vers le joueur"""
    
    def __init__(self, x: float, y: float, vitesse: float):
        super().__init__(x, y, largeur=1, hauteur=1)
        self.vitesse = vitesse
        self.points = 10
        self.deplacement_fractionnaire = 0.0
    
    def avancer(self):
        """Fait descendre l'ennemi"""
        self.deplacement_fractionnaire += self.vitesse
        
        if self.deplacement_fractionnaire >= 1.0:
            pixels = int(self.deplacement_fractionnaire)
            self.deplacer(0, pixels)
            self.deplacement_fractionnaire -= pixels


# ==============================================================================
# PROJECTILE
# ==============================================================================

class Projectile(ObjetVolant):
    """Projectile tiré par le vaisseau"""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, largeur=0.5, hauteur=1)
        self.vitesse = 2
    
    def avancer(self):
        """Fait monter le projectile"""
        self.deplacer(0, -self.vitesse)


# ==============================================================================
# BONUS
# ==============================================================================

class Bonus(ObjetVolant):
    """Bonus qui tombe du ciel"""
    
    TYPES = {
        "vie": {"nom": "Vie +1", "couleur": "#ff00ff", "icone": "+", "poids": 15},
        "vitesse": {"nom": "Vitesse", "couleur": "#00ffff", "icone": ">>", "poids": 25},
        "tir_double": {"nom": "Tir Double", "couleur": "#ffff00", "icone": "=", "poids": 25},
        "tir_triple": {"nom": "Tir Triple", "couleur": "#ff8800", "icone": "≡", "poids": 15},
        "tir_rapide": {"nom": "Tir Rapide", "couleur": "#ff0000", "icone": "!!!", "poids": 20},
    }
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, largeur=1, hauteur=1)
        self.vitesse = 0.5
        
        types_disponibles = list(self.TYPES.keys())
        poids = [self.TYPES[t]["poids"] for t in types_disponibles]
        self.type = random.choices(types_disponibles, weights=poids, k=1)[0]
        
        self.info = self.TYPES[self.type]
    
    def avancer(self):
        """Fait descendre le bonus"""
        self.deplacer(0, self.vitesse)


# ==============================================================================
# MOTEUR DE JEU
# ==============================================================================

class GameEngine:
    """
    Moteur principal qui gère toute la logique du jeu
    
    Le GameEngine coordonne :
    - Les mouvements de tous les objets
    - Les collisions entre objets
    - Le système de score
    - L'état général du jeu (en cours / terminé)
    - L'apparition des bonus
    
    Usage :
        engine = GameEngine(largeur=40, hauteur=20)
        engine.tirer()  # Le vaisseau tire
        engine.mettre_a_jour()  # Met à jour tous les objets (1 frame)
    """
    
    def __init__(self, largeur: int = 40, hauteur: int = 20):
        """Initialise le moteur avec les dimensions de la grille de jeu"""
        self.largeur = largeur
        self.hauteur = hauteur
        
        self.vaisseau = Vaisseau(
            x=largeur // 2,
            y=hauteur - 3,
            largeur_ecran=largeur,
            hauteur_ecran=hauteur
        )
        
        self.ennemis: List[Ennemi] = []
        self.projectiles: List[Projectile] = []
        self.bonus: List[Bonus] = []
        
        self.score = 0
        self.jeu_termine = False
        self.frame_count = 0
    
    def ajouter_ennemi(self, vitesse: float = 0.5):
        """Ajoute un nouvel ennemi"""
        x = random.randint(0, self.largeur - 2)
        ennemi = Ennemi(x, 0, vitesse)
        self.ennemis.append(ennemi)
    
    def ajouter_bonus(self):
        """Ajoute un bonus aléatoire"""
        x = random.randint(1, self.largeur - 2)
        bonus_obj = Bonus(x, 0)
        self.bonus.append(bonus_obj)
    
    def tirer(self):
        """Le vaisseau tire"""
        projectiles = self.vaisseau.tirer(self.frame_count)
        self.projectiles.extend(projectiles)
    
    def _peut_ramasser_bonus(self, type_bonus: str) -> bool:
        """Vérifie si un bonus peut être ramassé"""
        # Le bonus "vie" peut toujours être ramassé (mais sera ignoré si vies >= 5)
        if type_bonus == "vie":
            return self.vaisseau.vies < 5
        
        # Les autres bonus ne peuvent pas être ramassés s'ils sont déjà actifs
        return type_bonus not in self.vaisseau.bonus_actif_jusqu_a
    
    def mettre_a_jour(self):
        """Met à jour tous les objets du jeu"""
        if self.jeu_termine:
            return
        
        self.frame_count += 1
        self.vaisseau.mettre_a_jour_bonus(self.frame_count)
        
        # Déplacer les ennemis
        for ennemi in self.ennemis:
            ennemi.avancer()
            if ennemi.y >= self.hauteur - 1:
                ennemi.actif = False
                if self.vaisseau.perdre_vie():
                    self.jeu_termine = True
                    return
        
        # Déplacer les projectiles
        for projectile in self.projectiles:
            projectile.avancer()
        
        # Déplacer les bonus
        for bonus_obj in self.bonus:
            bonus_obj.avancer()
        
        # Vérifier les collisions
        self._verifier_collisions()
        
        # Nettoyer les objets inactifs
        self.ennemis = [e for e in self.ennemis if e.actif and e.y < self.hauteur]
        self.projectiles = [p for p in self.projectiles if p.actif and p.y > 0]
        self.bonus = [b for b in self.bonus if b.actif and b.y < self.hauteur]
    
    def _verifier_collisions(self):
        """Vérifie toutes les collisions"""
        # Collision vaisseau-ennemi (avec invincibilité)
        if self.frame_count > self.vaisseau.invincible_jusqu_a:
            for ennemi in self.ennemis:
                if not ennemi.actif:
                    continue
                
                if self.vaisseau.collision_avec(ennemi):
                    ennemi.actif = False
                    if self.vaisseau.perdre_vie():
                        self.jeu_termine = True
                    else:
                        self.vaisseau.invincible_jusqu_a = self.frame_count + 20
        
        # Collision projectile-ennemi
        for projectile in self.projectiles:
            if not projectile.actif:
                continue
            
            for ennemi in self.ennemis:
                if not ennemi.actif:
                    continue
                
                if projectile.collision_avec(ennemi):
                    projectile.actif = False
                    ennemi.actif = False
                    self.score += ennemi.points
                    break
        
        # Collision vaisseau-bonus
        for bonus_obj in self.bonus:
            if not bonus_obj.actif:
                continue
            
            if self.vaisseau.collision_avec(bonus_obj):
                bonus_obj.actif = False
                # Appliquer le bonus seulement s'il peut être ramassé
                if self._peut_ramasser_bonus(bonus_obj.type):
                    self._appliquer_bonus(bonus_obj.type)
    
    def _appliquer_bonus(self, type_bonus: str):
        """Applique l'effet d'un bonus"""
        if type_bonus == "vie":
            # Vie : toujours applicable si < 5 vies
            if self.vaisseau.vies < 5:
                self.vaisseau.gagner_vie()
        else:
            # Power-up temporaire
            self.vaisseau.activer_bonus(type_bonus, self.frame_count)
    
    def obtenir_grille_console(self) -> List[List[str]]:
        """Génère la grille pour l'affichage console"""
        # Créer une grille vide
        grille = [[' ' for _ in range(self.largeur)] for _ in range(self.hauteur)]
        
        # Placer les bonus
        for bonus_obj in self.bonus:
            if bonus_obj.actif:
                x = int(bonus_obj.x)
                y = int(bonus_obj.y)
                if 0 <= x < self.largeur and 0 <= y < self.hauteur:
                    grille[y][x] = bonus_obj.info["icone"][0] if bonus_obj.info["icone"] else '*'
        
        # Placer les ennemis
        for ennemi in self.ennemis:
            if ennemi.actif:
                x = int(ennemi.x)
                y = int(ennemi.y)
                if 0 <= x < self.largeur and 0 <= y < self.hauteur:
                    grille[y][x] = 'O'
        
        # Placer les projectiles
        for projectile in self.projectiles:
            if projectile.actif:
                x = int(projectile.x)
                y = int(projectile.y)
                if 0 <= x < self.largeur and 0 <= y < self.hauteur:
                    grille[y][x] = '|'
        
        # Placer le vaisseau
        v = self.vaisseau
        x = int(v.x)
        y = int(v.y)
        if 0 <= x < self.largeur and 0 <= y < self.hauteur:
            grille[y][x] = '^'
            # Ajouter la largeur du vaisseau
            if x + 1 < self.largeur:
                grille[y][x + 1] = '^'
        
        return grille