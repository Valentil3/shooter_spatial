# 🚀 Shooter Spatial - Documentation du Projet

## 📋 Vue d'ensemble

Shooter Spatial est un jeu d'arcade en Python où le joueur contrôle un vaisseau spatial et doit détruire des ennemis tout en collectant des bonus et en évitant les collisions.

## 📁 Structure du Projet

```
shooter_spatial/
│
├── 🎮 FICHIERS PRINCIPAUX
│   ├── shooter_gui.py          # Version graphique (Tkinter) - RECOMMANDÉ
│   ├── shooter_console.py      # Version console (terminal)
│   ├── game_classes.py         # Classes du jeu (moteur, objets)
│   └── score_manager.py        # Gestion des scores et leaderboard
│
├── 🛠️ UTILITAIRES
│   ├── installer_dependencies.py   # Installation automatique des dépendances
│   ├── installer_dependencies.bat  # Lanceur Windows (créé auto)
│   ├── lancer_jeu.bat             # Lanceur du jeu (créé auto)
│   └── serveur_web.py             # Serveur HTTP pour le leaderboard
│
├── 💾 DONNÉES
│   ├── scores.json            # Scores et statistiques des joueurs
│   └── index.html            # Leaderboard HTML exporté
│
└── 📚 DOCUMENTATION
    ├── README.md             # Documentation utilisateur
    └── README_PROJET.md      # Ce fichier (documentation technique)
```

## 🎯 Fichiers par Fonction

### Jeu Principal
- **shooter_gui.py** : Version graphique avec Tkinter
  - Interface redimensionnable avec mise à l'échelle automatique
  - Contrôles musique (lecture/pause, volume ±)
  - Affichage des bonus actifs, vies, score, temps
  - Boutons Quitter et contrôles de musique

- **shooter_console.py** : Version console/terminal
  - Support ZQSD et flèches directionnelles
  - Affichage coloré avec codes ANSI
  - Musique avec pygame (optionnel)

### Logique du Jeu
- **game_classes.py** : Toutes les classes du jeu
  - `ObjetVolant` : Classe de base pour tous les objets
  - `Vaisseau` : Vaisseau du joueur (vies, tir, bonus)
  - `Ennemi` : Ennemis descendant vers le joueur
  - `Projectile` : Projectiles tirés par le vaisseau
  - `Bonus` : Bonus collectables (vie, vitesse, tir)
  - `GameEngine` : Moteur coordonnant toute la logique

### Gestion des Scores
- **score_manager.py** : Gestion complète des scores
  - Enregistrement des scores avec historique
  - Classement des meilleurs joueurs
  - Statistiques détaillées par joueur
  - Export HTML du leaderboard

### Utilitaires
- **installer_dependencies.py** : Installation automatique
  - Vérifie Python 3.7+
  - Vérifie et installe pygame (musique)
  - Crée les fichiers .bat pour Windows

- **serveur_web.py** : Serveur HTTP local
  - Lance un serveur sur le port 8000
  - Affiche le leaderboard HTML dans le navigateur
  - Actualisation en temps réel

## 🔧 Dépendances

### Obligatoires (intégrées à Python)
- `tkinter` : Interface graphique (version GUI)
- `json` : Gestion des scores
- `pathlib` : Manipulation de chemins
- `typing` : Type hints
- `threading` : Musique en arrière-plan
- `random` : Génération aléatoire
- `datetime` : Horodatage

### Optionnelles
- `pygame` : Musique de fond (recommandé mais non obligatoire)
  - Installation : `pip install pygame`
  - Le jeu fonctionne sans musique si pygame n'est pas installé

## 🚀 Installation et Lancement

### 1. Installation Automatique (Recommandé)
```bash
# Double-cliquer sur installer_dependencies.bat (Windows)
# OU en ligne de commande :
python installer_dependencies.py
```

### 2. Lancer le Jeu

#### Version Graphique (Recommandé)
```bash
# Double-cliquer sur lancer_jeu.bat (Windows)
# OU :
python shooter_gui.py
```

#### Version Console
```bash
python shooter_console.py
```

### 3. Afficher le Leaderboard Web
```bash
python serveur_web.py
# Ouvre automatiquement le navigateur sur http://localhost:8000
```

## 🎮 Fonctionnalités du Jeu

### Système de Jeu
- ✅ Vaisseau avec 3 vies (max 5)
- ✅ Ennemis avec vitesse progressive
- ✅ Système de niveaux (difficulté croissante)
- ✅ Score et statistiques
- ✅ Invincibilité temporaire après perte de vie

### Système de Bonus
- **❤️ Vie +1** : Ajoute une vie (max 5)
- **⚡ Vitesse** : Déplacement 50% plus rapide
- **= Tir Double** : Tire 2 projectiles simultanément
- **≡ Tir Triple** : Tire 3 projectiles simultanément
- **!!! Tir Rapide** : Cooldown de tir divisé par 2

### Contrôles

#### Version GUI (Graphique)
- **Q/←** : Gauche
- **D/→** : Droite
- **Z/↑** : Haut
- **S/↓** : Bas
- **Espace** : Tirer
- **P** : Pause/Reprendre musique
- **Bouton Quitter** : Quitter le jeu

#### Version Console
- **Q/←** : Gauche
- **D/→** : Droite
- **Z/↑** : Haut
- **S/↓** : Bas
- **Espace** : Tirer
- **P** : Pause/Reprendre musique
- **X / ESC** : Quitter

### Vitesse Adaptative
Le vaisseau s'adapte automatiquement à la taille de l'écran :
- Écran 30 cases → vitesse 1.0×
- Écran 60 cases → vitesse 1.5×
- Écran 90 cases → vitesse 2.0×
- Maximum : 2.5×

Formule : `vitesse = min(2.5, 1.0 + (largeur - 30) / 60)`

## 🏗️ Architecture Technique

### Pattern MVC-like
- **Model** : `game_classes.py` (logique métier)
- **View** : `shooter_gui.py` / `shooter_console.py` (affichage)
- **Controller** : Intégré dans les vues (gestion des événements)

### Système de Coordonnées
- Origine (0, 0) en haut à gauche
- X augmente vers la droite
- Y augmente vers le bas
- Positions en `float` pour précision
- Conversion en `int` pour l'affichage

### Threading
- **Thread principal** : Boucle de jeu et affichage
- **MusiqueThread** : Gestion de la musique pygame
- **SpawnerThread** : Apparition des ennemis (console)
- **BonusSpawnerThread** : Apparition des bonus (console)

### Gestion des Collisions
Système de collision rectangle avec marge de tolérance de 0.5 unité pour améliorer le gameplay.

## 📊 Système de Scores

### Format JSON
```json
{
  "NomJoueur": {
    "meilleur_score": 450,
    "parties_jouees": 12,
    "score_total": 3840,
    "historique": [
      {
        "score": 450,
        "date": "2026-02-07 15:30:45"
      }
    ]
  }
}
```

### Statistiques Calculées
- **Meilleur score** : Record personnel
- **Parties jouées** : Nombre total de parties
- **Score total** : Somme de tous les scores
- **Score moyen** : `score_total / parties_jouees`

## 🔍 Optimisations Effectuées

### Code
- ✅ Docstrings détaillées pour toutes les classes
- ✅ Type hints pour tous les paramètres
- ✅ Noms de variables explicites
- ✅ Commentaires pour la logique complexe
- ✅ Gestion d'erreurs robuste

### Performance
- ✅ Utilisation de `float` pour positions précises
- ✅ Nettoyage automatique des objets inactifs
- ✅ Optimisation du nombre d'étoiles selon taille écran
- ✅ Cooldown de tir pour éviter spam

### Maintenance
- ✅ Suppression des fichiers obsolètes
- ✅ Centralisation des configurations
- ✅ Scripts d'installation automatiques
- ✅ Documentation complète

## 🗑️ Fichiers Supprimés (Obsolètes)

- ❌ `verifier.py` → Remplacé par `installer_dependencies.py`
- ❌ `diagnostic.py` → Utile uniquement en debug
- ❌ `create_scores.py` → Fonctionnalité dans `installer_dependencies.py`

## 🐛 Débogage

### Affichage des Debug
Pour activer les messages de debug dans la console :
- Les kills d'ennemis sont affichés automatiquement
- Les changements de niveau sont affichés automatiquement

### Problèmes Courants

**Musique ne fonctionne pas**
- Installer pygame : `pip install pygame`
- Vérifier que le fichier `musique.mp3` existe
- Le jeu fonctionne sans musique

**Buttons non visibles (GUI)**
- Vérifier que `HAUTEUR_JEU = HAUTEUR_PIXELS - 180`
- Redimensionner la fenêtre

**Vaisseau trop rapide/lent**
- La vitesse s'adapte automatiquement à la taille
- Modifier `vitesse_base` dans `Vaisseau.__init__()` si nécessaire

## 📦 Distribution

Pour distribuer le jeu :

1. **Inclure tous les fichiers** de la structure
2. **Fournir `installer_dependencies.py`** pour installation auto
3. **Inclure `README.md`** pour les utilisateurs
4. **Optionnel** : Inclure `musique.mp3` pour la musique

## 🎓 Utilisation Pédagogique

Ce projet démontre :
- ✅ Programmation orientée objet (POO)
- ✅ Héritage de classes
- ✅ Gestion d'événements
- ✅ Threading et concurrence
- ✅ Persistence de données (JSON)
- ✅ Interface graphique (Tkinter)
- ✅ Terminal/Console interactif
- ✅ Gestion d'erreurs
- ✅ Type hints Python
- ✅ Documentation du code

## 📝 Licence et Crédits

Projet réalisé dans le cadre du cours de Paradigmes de Programmation.

---

**Version** : 2.0 (Février 2026)
**Python** : 3.7+
**Auteur** : Valentin L
