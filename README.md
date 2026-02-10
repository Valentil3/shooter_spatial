# 🚀 Shooter Spatial

Un jeu de tir spatial avec système de bonus, vies multiples, difficulté progressive et leaderboard web interactif !

## 📁 Structure des fichiers

```
shooter_spatial/
├── game/
│   ├── game_classes.py          # Classes du jeu (moteur POO)
│   ├── shooter_gui.py           # Interface graphique (JEU PRINCIPAL) ⭐
│   ├── shooter_console.py       # Version console plein écran
│   ├── score_manager.py         # Gestion des scores avec historique
│   ├── serveur_web.py           # Serveur web pour le leaderboard
│   ├── scores.json              # Fichier des scores
│   └── index.html               # Page web du leaderboard
│
├── shooter_gui.bat              # Lanceur Windows (GUI)
├── shooter_console.bat          # Lanceur Windows (Console)
├── installer_dependencies.bat   # Installation automatique
├── diagramme.puml               # Diagrammes UML
├── rapport.tex                  # Rapport LaTeX
└── README.md                    # Ce fichier
```

## 🎮 Comment jouer

### Installation

1. **Installer Python 3.7+**

2. **Installer pygame (pour la musique)** :
```bash
pip install pygame
```

3. **Ajouter une musique (optionnel)** :
   - Place un fichier `musique.mp3` dans le dossier `game/`
   - Si pas de musique, le jeu fonctionne quand même !

### Lancer le jeu

**Version graphique (recommandée)** :
```bash
python game/shooter_gui.py
# ou double-clic sur shooter_gui.bat (Windows)
```

**Version console** :
```bash
python game/shooter_console.py
# ou double-clic sur shooter_console.bat (Windows)
```

## 🕹️ Commandes

### Version GUI
- **Déplacement** : Flèches directionnelles (← → ↑ ↓)
- **Tirer** : Barre d'espace
- **Pause musique** : Touche **P**
- **Quitter** : Touche **ESC** (avec confirmation)

### Version Console
- **Déplacement** : Flèches ou **ZQSD**
- **Tirer** : Barre d'espace
- **Pause musique** : Touche **P**
- **Quitter** : Touche **X** ou ESC

## 🎯 Objectif et Gameplay

### Objectif
Survivre le plus longtemps possible et accumuler le maximum de points en détruisant des ennemis !

### Système de vies
- **3 vies** au départ
- **Maximum de 5 vies** (avec bonus)
- Perte d'une vie si :
  - Un ennemi te touche
  - Un ennemi atteint le bas de l'écran
- **Invincibilité temporaire** après avoir perdu une vie (clignotement jaune)

### Scoring
- **+10 points** par ennemi détruit
- La difficulté augmente progressivement :
  - Ennemis plus rapides
  - Apparition plus fréquente
  - Niveaux de difficulté tous les 5 ennemis détruits

## 💎 Système de Bonus

Collecte des bonus qui tombent aléatoirement pour améliorer ton vaisseau !

### Types de bonus (durée : 10 secondes)

| Icône | Nom | Effet | Couleur |
|-------|-----|-------|---------|
| **+** | Vie +1 | Ajoute une vie (max 5) | Magenta |
| **>>** | Vitesse | Augmente la vitesse de 50% | Cyan |
| **=** | Tir Double | Tire 2 projectiles simultanément | Jaune |
| **≡** | Tir Triple | Tire 3 projectiles simultanément | Orange |
| **!!!** | Tir Rapide | Réduit le cooldown de tir de 50% | Rouge |

**Note** : Les bonus temporaires ne peuvent pas se cumuler du même type. Le vaisseau change de couleur selon le bonus actif !

## 📊 Système de scores

### Scores locaux

Les scores sont sauvegardés automatiquement dans `scores.json` avec :
- **Meilleur score** de chaque joueur
- **Historique** des 10 dernières parties
- **Statistiques** : nombre de parties, score moyen, score total

### Leaderboard web

À la fin de chaque partie, tu peux visualiser le classement complet dans ton navigateur !

**Option 1 - Ouverture automatique** :
- À la fin de la partie, clique sur "Voir Leaderboard Web" ou "Oui" selon la version

**Option 2 - Serveur web** :
```bash
python game/serveur_web.py
```
Puis ouvre http://localhost:8000/index.html dans ton navigateur

Le leaderboard affiche :
- 🥇🥈🥉 Médailles pour le top 3
- Classement des 20 meilleurs joueurs
- Design moderne avec animations
- Actualisation automatique

## 🎨 Fonctionnalités

### Version GUI (Interface Graphique)
✅ Menu principal animé avec étoiles  
✅ Écran d'instructions interactif  
✅ Écran de scores avec médailles  
✅ Fond spatial animé pendant le jeu  
✅ Affichage en temps réel : score, vies, temps, niveau  
✅ Indicateurs visuels des bonus actifs  
✅ Interface redimensionnable (support plein écran)  
✅ Musique de fond avec contrôles (pause, volume)  
✅ Chronomètre de survie  
✅ Vaisseau changeant de couleur selon les bonus  
✅ Effet de clignotement pendant l'invincibilité  

### Version Console
✅ Affichage plein écran adaptatif  
✅ Codes couleur ANSI pour un rendu coloré  
✅ Support ZQSD et flèches directionnelles  
✅ Affichage des bonus actifs  
✅ Statistiques en fin de partie  
✅ Détection automatique de la taille du terminal  

### Système technique
✅ Architecture POO propre (héritage, encapsulation, polymorphisme)  
✅ Threads pour musique et spawn d'ennemis/bonus  
✅ Détection de collisions optimisée  
✅ Difficulté progressive adaptative  
✅ Système de frames pour timing précis  
✅ Gestion d'erreurs robuste  

## 🎯 Stratégies de jeu

### Pour débutants
- Reste au centre de l'écran pour avoir plus de marge de manœuvre
- Ne tire pas en continu, économise tes tirs
- Priorise la survie au score

### Pour intermédiaires
- Collecte les bonus de tir (double/triple) en priorité
- Utilise la vitesse bonus pour esquiver plus facilement
- Reste mobile, ne campe pas dans un coin

### Pour experts
- Combine tir triple + tir rapide pour un DPS maximum
- Utilise l'invincibilité pour traverser les groupes d'ennemis
- Maximise le temps avec bonus pour un score optimal

## 🐛 Problèmes courants

**Pas de musique ?**
- Installe pygame : `pip install pygame`
- Ajoute un fichier `musique.mp3` dans `game/`
- Vérifie que le fichier n'est pas corrompu

**Le leaderboard ne s'ouvre pas ?**
- Vérifie que `index.html` est dans le dossier `game/`
- Utilise le serveur web : `python game/serveur_web.py`
- Vérifie que le port 8000 n'est pas déjà utilisé

**Scores non sauvegardés ?**
- Vérifie les permissions d'écriture dans le dossier
- Le fichier `scores.json` sera créé automatiquement

**Jeu trop lent/rapide ?**
- Version GUI : Le jeu s'adapte automatiquement
- Version Console : Redimensionne ton terminal pour ajuster la taille

**Touches ne répondent pas ?**
- Version GUI : Clique sur la fenêtre pour lui donner le focus
- Version Console : Assure-toi que le terminal a le focus

## 🔧 Configuration avancée

### Modifier la difficulté

Édite les fichiers `shooter_console.py` ou `shooter_gui.py` :

```python
class Config:
    VITESSE_INITIALE = 0.3    # Vitesse de départ des ennemis
    VITESSE_MAX = 2.0          # Vitesse max
    SPAWN_INITIAL = 2.0        # Intervalle spawn initial (secondes)
    SPAWN_MIN = 0.8            # Intervalle min
    CHANCE_BONUS = 0.3         # Probabilité d'apparition bonus (0-1)
```

### Modifier la durée des bonus

Dans `game_classes.py`, méthode `activer_bonus()` :

```python
def activer_bonus(self, type_bonus, frame_actuelle, duree=300):
    # duree en frames (300 frames ≈ 10 secondes à 30 FPS)
```

### Modifier le volume de la musique

Dans `MusiqueThread.__init__()` :

```python
pygame.mixer.music.set_volume(0.3)  # 0.0 à 1.0
```

## 📖 Documentation technique

Pour plus de détails sur l'architecture et l'implémentation :
- Consulte `README_PROJET.md` pour la documentation technique complète
- Consulte `rapport.tex` pour le rapport académique détaillé
- Consulte `diagramme.puml` pour les diagrammes UML

## 🏆 Records communautaires

Partage tes meilleurs scores avec la communauté !

- Record actuel du développeur : **850 points** 🎯
- Défi : Atteindre **1000 points** avec 5 vies restantes

## 📝 Crédits

**Développé avec ❤️ en Python**

Technologies utilisées :
- Python 3.7+
- tkinter (Interface graphique)
- pygame (Musique)
- threading (Programmation concurrente)
- json (Persistance des données)

**Paradigmes de programmation illustrés :**
- ✅ Orienté Objet (POO)
- ✅ Procédural
- ✅ Événementiel
- ✅ Concurrent

Bon jeu spatial ! 🎮🚀✨

---

💡 **Astuce finale** : Dans la version GUI, tu peux redimensionner la fenêtre en plein écran pour une expérience immersive maximale !
