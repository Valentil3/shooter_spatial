<div align="center">

# 🚀 SHOOTER SPATIAL 🌌

### *Un jeu de tir spatial développé en Python*

![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Actif-success?style=for-the-badge)

**Survie spatiale | Bonus dynamiques | Difficulté progressive | Leaderboard web**

[🎮 Démarrage rapide](#-démarrage-rapide) • [📖 Documentation](#-commandes-de-jeu) • [💎 Bonus](#-système-de-bonus) • [🏆 Scores](#-système-de-scores)

</div>

---

## 📋 Table des matières

- [🎯 À propos](#-à-propos)
- [✨ Fonctionnalités principales](#-fonctionnalités-principales)
- [📁 Structure du projet](#-structure-du-projet)
- [🚀 Démarrage rapide](#-démarrage-rapide)
- [🎮 Comment jouer](#-comment-jouer)
- [🕹️ Commandes de jeu](#️-commandes-de-jeu)
- [💎 Système de bonus](#-système-de-bonus)
- [🏆 Système de scores](#-système-de-scores)
- [🎨 Captures d'écran](#-captures-décran)
- [🏗️ Architecture technique](#️-architecture-technique)
- [⚙️ Configuration avancée](#️-configuration-avancée)
- [🎯 Stratégies de jeu](#-stratégies-de-jeu)
- [❓ FAQ](#-faq)
- [🤝 Contribution](#-contribution)
- [📝 Crédits](#-crédits)

---

## 🎯 À propos

**Shooter Spatial** est un jeu de tir spatial développé en Python dans le cadre de mon projet de Licence Informatique en Paradigme de Programmation. Le jeu combine programmation orientée objet, événementielle et concurrente pour offrir une expérience de jeu complète et fluide.

### 🎲 Gameplay

Pilotez votre vaisseau spatial dans une bataille sans fin contre des vagues d'ennemis ! Collectez des bonus pour améliorer vos capacités, survivez le plus longtemps possible et battez les records du leaderboard.

### 🌟 Pourquoi ce projet ?

- 🎓 **Pédagogique** : Démontre les paradigmes de programmation (POO, événementiel, concurrent)
- 🎮 **Ludique** : Gameplay avec système de progression
- 🌐 **Moderne** : Intègre un leaderboard web en temps réel

---

## ✨ Fonctionnalités principales

<table>
<tr>
<td width="50%">

### 🖥️ Version GUI (Graphique)
- ✅ Menu principal animé avec étoiles
- ✅ Écrans d'instructions et de scores
- ✅ Fond spatial animé en temps réel
- ✅ HUD complet (score, vies, temps, niveau)
- ✅ Indicateurs visuels des bonus actifs
- ✅ Interface redimensionnable/plein écran
- ✅ Musique de fond avec contrôles
- ✅ Chronomètre de survie
- ✅ Effets visuels (clignotement, couleurs)

</td>
<td width="50%">

### 💻 Version Console
- ✅ Affichage plein écran adaptatif
- ✅ Codes couleur ANSI pour un rendu coloré
- ✅ Support ZQSD et flèches directionnelles
- ✅ Affichage des bonus actifs
- ✅ Statistiques détaillées en fin de partie
- ✅ Détection automatique de la taille
- ✅ Musique de fond (avec pygame)
- ✅ Performance optimisée

</td>
</tr>
</table>

### 🎮 Système de jeu

| Fonctionnalité | Description |
|----------------|-------------|
| **💚 Système de vies** | 3 vies de départ, maximum 5 avec bonus |
| **⚡ Invincibilité** | Période d'invincibilité après avoir perdu une vie |
| **📈 Difficulté progressive** | Les ennemis deviennent plus rapides et plus nombreux |
| **💎 5 types de bonus** | Vie+1, Vitesse, Tir Double/Triple, Tir Rapide |
| **🎯 Système de scoring** | +10 points par ennemi, statistiques détaillées |
| **🌐 Leaderboard web** | Classement mondial avec médailles et animations |
| **🎵 Musique Immersive** | Restez concentré ! |

---

## 📁 Structure du projet

```
shooter_spatial/
│
├── 📂 game/                          # Dossier principal du jeu
│   ├── 🎯 game_classes.py           # Classes du jeu (moteur POO)
│   ├── 🖥️ shooter_gui.py            # Interface graphique
│   ├── 💻 shooter_console.py        # Version console plein écran
│   ├── 📊 score_manager.py          # Gestion des scores avec historique
│   ├── 🌐 serveur_web.py            # Serveur HTTP pour le leaderboard
│   ├── 📄 index.html                # Page web du leaderboard
│   ├── 💾 scores.json               # Base de données des scores
│   └── 🎵 musique.mp3               # Musique de fond
│
├── 🚀 shooter_gui.bat               # Lanceur rapide Windows (GUI)
├── 💻 shooter_console.bat           # Lanceur rapide Windows (Console)
├── 📦 installer_dependencies.bat    # Installation automatique (Windows)
│
├── 📐 diagramme_classes.puml        # Diagramme UML des classes
├── 📄 rapport.tex                   # Rapport LaTeX
├── 📖 README.md                     # Documentation complète
└── 🐍 __pycache__/                  # Cache Python (généré)
```

---

## 🚀 Démarrage rapide

### Prérequis

- **Python 3.7+** ([Télécharger Python](https://www.python.org/downloads/))
- **pygame** (pour la musique - optionnel)

### Installation

#### 🪟 Windows (Automatique)

```bash
# Double-clic sur ce fichier pour tout installer automatiquement
installer_dependencies.bat
```

#### 🐧 Linux / 🍎 macOS / 🪟 Windows (Manuel)

```bash
# Installer pygame (pour la musique)
pip install pygame
```

### Lancer le jeu

#### 🖥️ Version graphique (recommandée)

```bash
# Méthode 1 : Lanceur Windows
Double-clic sur shooter_gui.bat

# Méthode 2 : Python
# python game/shooter_gui.py
```

#### 💻 Version console

```bash
# Méthode 1 : Lanceur Windows
Double-clic sur shooter_console.bat

# Méthode 2 : Python
# python game/shooter_console.py
```

---

## 🎮 Comment jouer

### 🎯 Objectif

**Survivre le plus longtemps possible** et accumuler un maximum de points en détruisant des vagues d'ennemis !

### 💚 Système de vies

| État | Description |
|------|-------------|
| 🟢 **Vies de départ** | 3 vies au début de la partie |
| 🔵 **Vies maximales** | Maximum de 5 vies (avec bonus) |
| 💔 **Perte de vie** | Si un ennemi vous touche OU atteint le bas de l'écran |
| 🛡️ **Invincibilité** | Période d'invincibilité temporaire après perte d'une vie (vaisseau clignote en jaune) |
| 💀 **Game Over** | Quand toutes les vies sont perdues |

### 📊 Système de scoring

- **+10 points** par ennemi détruit
- Les **statistiques** sont enregistrées automatiquement
- Le **chronomètre** mesure votre temps de survie
- Le **niveau de difficulté** augmente tous les **5 ennemis détruits**

### 📈 Difficulté progressive

La difficulté augmente automatiquement au fil du temps :

| Niveau | Ennemis détruits | Vitesse des ennemis | Fréquence d'apparition |
|--------|------------------|---------------------|------------------------|
| 1 ⭐ | 0-4 | Lent | 3 secondes |
| 2 ⭐⭐ | 5-9 | Moyen | 2 secondes |
| 3 ⭐⭐⭐ | 10-14 | Rapide | 1.5 secondes |
| 4+ ⭐⭐⭐⭐ | 15+ | Très rapide | < 1 seconde |

---

## 🕹️ Commandes de jeu

### 🖥️ Version GUI (Interface graphique)

| Action | Touche | Description |
|--------|--------|-------------|
| ⬅️ **Gauche** | `←` ou `Q` | Déplacer le vaisseau vers la gauche |
| ➡️ **Droite** | `→` ou `D` | Déplacer le vaisseau vers la droite |
| ⬆️ **Haut** | `↑` ou `Z` | Déplacer le vaisseau vers le haut |
| ⬇️ **Bas** | `↓` ou `S` | Déplacer le vaisseau vers le bas |
| 🔫 **Tirer** | `Espace` | Tirer un projectile |
| 🎵 **Pause musique** | `P` | Mettre en pause/reprendre la musique |
| 🚪 **Quitter** | `ESC` | Quitter le jeu (avec confirmation) |

### 💻 Version Console

| Action | Touches | Description |
|--------|---------|-------------|
| ⬅️ **Gauche** | `←` ou `Q` | Déplacer le vaisseau vers la gauche |
| ➡️ **Droite** | `→` ou `D` | Déplacer le vaisseau vers la droite |
| ⬆️ **Haut** | `↑` ou `Z` | Déplacer le vaisseau vers le haut |
| ⬇️ **Bas** | `↓` ou `S` | Déplacer le vaisseau vers le bas |
| 🔫 **Tirer** | `Espace` | Tirer un projectile |
| 🎵 **Pause musique** | `P` | Mettre en pause/reprendre la musique |
| 🚪 **Quitter** | `X` ou `ESC` | Quitter le jeu |

---

## 💎 Système de bonus

Des bonus apparaissent **aléatoirement** pendant le jeu (30% de chance) pour améliorer les capacités de votre vaisseau.

### 🎁 Types de bonus

| Icône | Nom | Effet | Durée | Couleur | Cumulable |
|-------|-----|-------|-------|---------|-----------|
| **`+`** | 💚 Vie +1 | Ajoute 1 vie (max 5) | Permanent | Magenta | ❌ |
| **`>>`** | ⚡ Vitesse | Vitesse +50% | 10 sec | Cyan | ❌ |
| **`=`** | 🔫 Tir Double | Tire 2 projectiles | 10 sec | Jaune | ❌ |
| **`≡`** | 🔥 Tir Triple | Tire 3 projectiles | 10 sec | Orange | ❌ |
| **`!!!`** | ⚡ Tir Rapide | Cooldown -50% | 10 sec | Rouge | ❌ |

### 🎨 Effets visuels

- 🎨 **Changement de couleur** : Le vaisseau prend la couleur du bonus actif
- ⏱️ **Indicateur de durée** : Barre de progression visible dans l'interface
- 🚫 **Non cumulables** : Un seul bonus temporaire à la fois (le nouveau remplace l'ancien)
- 💪 **Combinaisons puissantes** : Tir Triple + Tir Rapide = dévastation maximale !

### 🎯 Stratégie bonus

```
🥉 Bronze : Collecte tous les bonus que tu vois
🥈 Argent : Priorise Tir Triple > Tir Double > Vitesse
🥇 Or     : Combine Tir Triple + Tir Rapide pour DPS maximum
```

---

## 🏆 Système de scores

### 💾 Scores locaux

Les scores sont **automatiquement sauvegardés** dans `scores.json` avec :

- 🏆 **Meilleur score** de chaque joueur
- 📜 **Historique** des 10 dernières parties
- 📊 **Statistiques complètes** :
  - Nombre total de parties jouées
  - Score moyen
  - Score total cumulé
  - Temps de survie moyen
  - Meilleure série

### 🌐 Leaderboard Web

À la fin de chaque partie, visualisez le **classement** dans votre navigateur !

#### 🚀 Option 1 : Ouverture automatique

Après une partie, cliquez sur :
- **"Voir Leaderboard Web"** (Version GUI)
- **"Oui"** à la question leaderboard (Version Console)

#### 🌐 Option 2 : Serveur web manuel

```bash
# Démarrer le serveur web
python game/serveur_web.py

# Ouvrir dans le navigateur
http://localhost:8000/index.html
```

#### ✨ Fonctionnalités du leaderboard

- 🥇🥈🥉 **Médailles** pour le top 3
- 📊 **Classement** des 20 meilleurs joueurs
- 🎨 **Design moderne** avec animations CSS
- 🔄 **Actualisation** en temps réel
- 📱 **Interface responsive** (mobile/desktop)


---

## ⚙️ Configuration avancée

### 🎮 Modifier la difficulté

Éditez `shooter_gui.py` ou `shooter_console.py` :

```python
class Config:
    # Vitesse des ennemis
    VITESSE_INITIALE = 0.1    # Vitesse de départ (plus bas = plus lent)
    VITESSE_MAX = 2.0          # Vitesse maximale
    
    # Apparition des ennemis
    SPAWN_INITIAL = 3000       # Délai initial en ms
    SPAWN_MIN = 600            # Délai minimum en ms
    
    # Bonus
    CHANCE_BONUS = 0.30        # 30% de chance (0.0 à 1.0)
```

---

## 🤝 Amélioration

Ce projet est développé dans un cadre scolaire. Les améliorations sont les bienvenues !

### 📝 Idées

- [ ] Ajouter des power-ups permanents
- [ ] Implémenter des boss de fin de niveau
- [ ] Créer différents types d'ennemis (patterns de mouvement)
- [ ] Ajouter un système de succès/achievements
- [ ] Implémenter un mode multijoueur local
- [ ] Créer un éditeur de niveaux
- [ ] Ajouter des effets sonores
- [ ] Améliorer les graphismes (sprites, explosions)


---

## 📝 Crédits

<div align="center">


**Technologies utilisées :**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-092E20?style=for-the-badge&logo=python&logoColor=white)
![Threading](https://img.shields.io/badge/Threading-FF6B6B?style=for-the-badge&logo=python&logoColor=white)

**Bibliothèques :**
- `tkinter` - Interface graphique
- `pygame` - Audio/Musique
- `threading` - Programmation concurrente
- `json` - Persistence des données

**Paradigmes de programmation illustrés :**

🔷 **Orienté Objet (POO)** | 🔷 **Procédural** | 🔷 **Événementiel** | 🔷 **Concurrent**

---

### 📜 Licence

Ce projet est sous licence **MIT** - Voir le fichier LICENSE pour plus de détails.

---

### 🙏 Remerciements

Merci à tous ceux qui ont testé le jeu et donné leurs retours !


**Bon jeu spatial !** 🌌✨🛸

---

*Dernière mise à jour : Février 2026*

<br>

**[⬆️ Retour en haut](#-shooter-spatial-)**

</div>
