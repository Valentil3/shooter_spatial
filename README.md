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

**Shooter Spatial** est un jeu de tir spatial développé en Python dans le cadre d'un projet académique sur les paradigmes de programmation. Le jeu combine programmation orientée objet, événementielle et concurrente pour offrir une expérience de jeu complète et fluide.

### 🎲 Gameplay

Pilotez votre vaisseau spatial dans une bataille sans fin contre des vagues d'ennemis ! Collectez des bonus pour améliorer vos capacités, survivez le plus longtemps possible et battez les records du leaderboard mondial.

### 🌟 Pourquoi ce projet ?

- 🎓 **Pédagogique** : Démontre les paradigmes de programmation (POO, événementiel, concurrent)
- 🎮 **Ludique** : Gameplay accrocheur avec système de progression
- 💻 **Multi-plateforme** : Fonctionne sur Windows, Linux et macOS
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
- ✅ Compatible Windows/Linux/macOS

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
| **🎵 Musique personnalisable** | Ajoutez votre propre musique MP3 |

---

## 📁 Structure du projet

```
shooter_spatial/
│
├── 📂 game/                          # Dossier principal du jeu
│   ├── 🎯 game_classes.py           # Classes du jeu (moteur POO)
│   ├── 🖥️ shooter_gui.py            # Interface graphique ⭐ RECOMMANDÉ
│   ├── 💻 shooter_console.py        # Version console plein écran
│   ├── 📊 score_manager.py          # Gestion des scores avec historique
│   ├── 🌐 serveur_web.py            # Serveur HTTP pour le leaderboard
│   ├── 📄 index.html                # Page web du leaderboard
│   ├── 💾 scores.json               # Base de données des scores
│   └── 🎵 musique.mp3               # Musique de fond (optionnel)
│
├── 🚀 shooter_gui.bat               # Lanceur rapide Windows (GUI)
├── 💻 shooter_console.bat           # Lanceur rapide Windows (Console)
├── 📦 installer_dependencies.bat    # Installation automatique (Windows)
│
├── 📐 diagramme_classes.puml        # Diagramme UML des classes
├── 📄 rapport.tex                   # Rapport académique LaTeX
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
# 1. Installer pygame (pour la musique)
pip install pygame

# 2. Ajouter une musique (optionnel)
# Placer un fichier musique.mp3 dans le dossier game/
```

### Lancer le jeu

#### 🖥️ Version graphique (recommandée)

```bash
# Méthode 1 : Python
python game/shooter_gui.py

# Méthode 2 : Lanceur Windows
# Double-clic sur shooter_gui.bat
```

#### 💻 Version console

```bash
# Méthode 1 : Python
python game/shooter_console.py

# Méthode 2 : Lanceur Windows
# Double-clic sur shooter_console.bat
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
| ⬅️ **Gauche** | `←` Flèche gauche | Déplacer le vaisseau vers la gauche |
| ➡️ **Droite** | `→` Flèche droite | Déplacer le vaisseau vers la droite |
| ⬆️ **Haut** | `↑` Flèche haut | Déplacer le vaisseau vers le haut |
| ⬇️ **Bas** | `↓` Flèche bas | Déplacer le vaisseau vers le bas |
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

À la fin de chaque partie, visualisez le **classement mondial** dans votre navigateur !

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

## 🎨 Captures d'écran

> 📸 *Section à venir : Ajoutez vos propres captures d'écran du jeu !*

```
game/screenshots/
├── menu.png          # Menu principal
├── gameplay.png      # Jeu en action
├── bonus.png         # Bonus actifs
└── leaderboard.png   # Page web des scores
```

---

## 🏗️ Architecture technique

### 🎯 Paradigmes de programmation

Le projet illustre **4 paradigmes de programmation** :

| Paradigme | Utilisation | Exemple |
|-----------|-------------|---------|
| **🔷 Orienté Objet (POO)** | Structure du code | Classes `Vaisseau`, `Ennemi`, `Projectile`, `Bonus` héritant de `ObjetVolant` |
| **🔷 Procédural** | Logique de jeu | Boucle principale, gestion des collisions, mise à jour des positions |
| **🔷 Événementiel** | Gestion des entrées | Détection des touches clavier, clics de souris |
| **🔷 Concurrent** | Performance | Threads pour musique, spawn d'ennemis, serveur web |

### 📦 Modules principaux

```python
📂 game/
├── game_classes.py         # 🎯 Moteur de jeu POO
│   ├── ObjetVolant         # Classe de base abstraite
│   ├── Vaisseau            # Contrôle joueur + bonus
│   ├── Ennemi              # IA ennemis
│   ├── Projectile          # Gestion des tirs
│   ├── Bonus               # Système de bonus
│   └── GameEngine          # Moteur principal
│
├── shooter_gui.py          # 🖥️ Interface graphique (tkinter)
│   ├── Menu principal      # Navigation + animations
│   ├── Écran de jeu        # Boucle de jeu + affichage
│   ├── Gestion événements  # Clavier + souris
│   └── Thread musique      # Lecture audio asynchrone
│
├── shooter_console.py      # 💻 Version terminal
│   ├── Affichage ANSI      # Codes couleur terminal
│   ├── Détection clavier   # Input non-bloquant
│   └── Adaptation écran    # Redimensionnement auto
│
└── score_manager.py        # 📊 Persistence des données
    ├── Sauvegarde JSON     # Lecture/écriture scores
    ├── Statistiques        # Calculs agrégés
    └── Export HTML         # Génération leaderboard
```

### 🔄 Diagramme de classes (simplifié)

```
        ObjetVolant
        ====================================
        + x, y : float
        + largeur, hauteur : float
        + actif : bool
        ------------------------------------
        + deplacer(dx, dy)
        + collision_avec(autre) : bool
        ====================================
                    △
                    │ (hérite)
    ┌───────────────┼───────────────┬────────────┐
    │               │               │            │
Vaisseau        Ennemi       Projectile      Bonus
========        ======       ==========      =====
+ vies          + vitesse    + vitesse       + type
+ vitesse       + direction  + direction     + effet
+ bonus_actifs  + spawn()    + move()        + duree
+ tirer()       + move()                     + activer()
+ perdre_vie()
```

### 🧵 Threading

Le jeu utilise plusieurs threads pour les tâches asynchrones :

```python
Thread Principal (GUI/Console)
│
├─→ Thread Musique (pygame.mixer)
│   └─→ Lecture continue du MP3
│
├─→ Thread Spawn Ennemis
│   └─→ Création périodique d'ennemis
│
├─→ Thread Spawn Bonus
│   └─→ Apparition aléatoire de bonus
│
└─→ Thread Serveur Web (optionnel)
    └─→ HTTPServer sur port 8000
```

### 💾 Format de données (scores.json)

```json
{
  "NomJoueur": {
    "meilleur_score": 850,
    "nombre_parties": 15,
    "score_total": 4230,
    "score_moyen": 282,
    "historique": [
      {
        "score": 850,
        "date": "2026-02-10 14:30:25",
        "temps_survie": "03:45",
        "ennemis_detruits": 85
      }
    ]
  }
}
```

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

### 💎 Modifier les bonus

Dans `game_classes.py`, méthode `activer_bonus()` :

```python
def activer_bonus(self, type_bonus, frame_actuelle, duree=300):
    """
    Modifiez la durée des bonus ici
    duree : nombre de frames (300 frames ≈ 10 sec à 30 FPS)
    """
    pass
```

### 🎵 Personnaliser la musique

```python
# 1. Volume (0.0 = muet, 1.0 = max)
pygame.mixer.music.set_volume(0.3)

# 2. Changer de musique
# Remplacez game/musique.mp3 par votre fichier

# 3. Désactiver complètement
# Supprimez musique.mp3 ou désinstallez pygame
```

### 🎨 Personnaliser les couleurs (GUI)

Dans `shooter_gui.py` :

```python
# Couleurs du jeu
COULEUR_FOND = "#0a0a1a"           # Fond spatial
COULEUR_VAISSEAU = "#00ff00"       # Vaisseau (vert)
COULEUR_ENNEMI = "#ff0000"         # Ennemis (rouge)
COULEUR_PROJECTILE = "#ffff00"     # Projectiles (jaune)
COULEUR_TEXTE = "#ffffff"          # Texte (blanc)
```

---

## 🎯 Stratégies de jeu

### 🔰 Débutant (0-100 points)

```
✓ Reste au centre de l'écran
✓ Tire uniquement quand nécessaire
✓ Priorise la survie sur le score
✓ Collecte les bonus de vie en priorité
✓ Évite les coins de l'écran
```

### ⚔️ Intermédiaire (100-500 points)

```
✓ Collecte les bonus de tir (double/triple)
✓ Utilise la vitesse pour esquiver
✓ Reste constamment en mouvement
✓ Anticipe les trajectoires ennemies
✓ Maximise le nombre de tirs
```

### 🏆 Expert (500+ points)

```
✓ Combine Tir Triple + Tir Rapide = DPS max
✓ Utilise l'invincibilité pour traverser les vagues
✓ Gère parfaitement les cooldowns
✓ Optimise le temps sous bonus
✓ Maintiens un mouvement fluide et prévisible
```

### 💡 Astuces pro

| Astuce | Explication |
|--------|-------------|
| 🎯 **Vise les groupes** | Le tir triple peut éliminer plusieurs ennemis alignés |
| ⏱️ **Gère les cooldowns** | Ne spam pas la barre d'espace, attends le cooldown |
| 🛡️ **Abuse l'invincibilité** | Traverse les ennemis pendant le clignotement |
| 💎 **Bonus stratégiques** | Tir > Vitesse > Autres selon la situation |
| 📍 **Positionnement** | Reste dans les 2/3 supérieurs de l'écran |

---

## ❓ FAQ

<details>
<summary><b>🎵 Pas de musique ou erreurs audio ?</b></summary>

**Solutions :**
```bash
# Installer pygame
pip install pygame

# Vérifier que musique.mp3 existe
ls game/musique.mp3

# Tester pygame
python -c "import pygame; print('OK')"
```

Le jeu fonctionne **sans musique** si pygame n'est pas installé.
</details>

<details>
<summary><b>🌐 Le leaderboard ne s'ouvre pas ?</b></summary>

**Solutions :**
1. Vérifier que `index.html` existe dans `game/`
2. Lancer manuellement le serveur :
   ```bash
   python game/serveur_web.py
   ```
3. Ouvrir manuellement : `http://localhost:8000/index.html`
4. Vérifier que le port 8000 n'est pas occupé
</details>

<details>
<summary><b>💾 Les scores ne sont pas sauvegardés ?</b></summary>

**Causes possibles :**
- Permissions d'écriture manquantes dans le dossier
- Fichier `scores.json` corrompu
- Caractères spéciaux dans le nom du joueur

**Solution :**
```bash
# Supprimer et recréer
rm game/scores.json
# Le fichier sera recréé au prochain lancement
```
</details>

<details>
<summary><b>🐢 Jeu trop lent ou trop rapide ?</b></summary>

**Version GUI :** Le jeu s'adapte automatiquement. Si problème :
- Fermez les autres applications
- Vérifiez les pilotes graphiques

**Version Console :** Ajustez la taille du terminal
- Plus grand terminal = plus grand terrain
- Plus petit terminal = terrain plus dense
</details>

<details>
<summary><b>⌨️ Les touches ne répondent pas ?</b></summary>

**Version GUI :**
- Cliquez sur la fenêtre de jeu pour lui donner le focus
- Vérifiez que tkinter est bien installé

**Version Console :**
- Vérifiez que le terminal a le focus
- Sous Windows, le mode plein écran peut aider
- Essayez les touches alternatives (ZQSD au lieu des flèches)
</details>

<details>
<summary><b>🪟 Problèmes sous Windows ?</b></summary>

**Utilisez les lanceurs .bat :**
```batch
# Double-clic sur ces fichiers
shooter_gui.bat          # Lance la version GUI
shooter_console.bat      # Lance la version console
installer_dependencies.bat  # Installe automatiquement
```

Ces scripts gèrent automatiquement les chemins et dépendances.
</details>

<details>
<summary><b>🐧 Problèmes sous Linux/macOS ?</b></summary>

**Permissions :**
```bash
# Rendre les fichiers Python exécutables
chmod +x game/*.py

# Installer pygame
pip3 install pygame

# Lancer avec python3
python3 game/shooter_gui.py
```
</details>

---

## 🤝 Contribution

Ce projet est développé dans un cadre académique. Les contributions sont les bienvenues !

### 📝 Idées d'amélioration

- [ ] Ajouter des power-ups permanents
- [ ] Implémenter des boss de fin de niveau
- [ ] Créer différents types d'ennemis (patterns de mouvement)
- [ ] Ajouter un système de succès/achievements
- [ ] Implémenter un mode multijoueur local
- [ ] Créer un éditeur de niveaux
- [ ] Ajouter des effets sonores
- [ ] Améliorer les graphismes (sprites, explosions)

### 🐛 Rapporter un bug

Ouvrez une issue avec :
- Description du problème
- Étapes pour reproduire
- Version de Python
- Système d'exploitation
- Logs d'erreur si applicable

---

## 📝 Crédits

<div align="center">

### Développé avec ❤️ en Python

**Technologies utilisées :**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-092E20?style=for-the-badge&logo=python&logoColor=white)
![Threading](https://img.shields.io/badge/Threading-FF6B6B?style=for-the-badge&logo=python&logoColor=white)

**Bibliothèques :**
- `tkinter` - Interface graphique
- `pygame` - Audio/Musique
- `threading` - Programmation concurrente
- `json` - Persistence des données
- `http.server` - Serveur web local

**Paradigmes de programmation illustrés :**

🔷 **Orienté Objet (POO)** | 🔷 **Procédural** | 🔷 **Événementiel** | 🔷 **Concurrent**

---

### 📚 Contexte académique

Projet développé dans le cadre du cours :
**"Paradigmes de Programmation"** - Licence Informatique

**Objectifs pédagogiques atteints :**
- ✅ Maîtrise de la POO (héritage, encapsulation, polymorphisme)
- ✅ Programmation événementielle (GUI, interactions utilisateur)
- ✅ Programmation concurrente (threads, synchronisation)
- ✅ Architecture logicielle (séparation des responsabilités)
- ✅ Gestion de projet (versioning, documentation)

---

### 📄 Documentation supplémentaire

- 📐 **diagramme_classes.puml** - Diagrammes UML complets
- 📄 **rapport.tex** - Rapport académique détaillé en LaTeX
- 🌐 **index.html** - Interface web du leaderboard

---

### 📜 Licence

Ce projet est sous licence **MIT** - Voir le fichier LICENSE pour plus de détails.

---

### 🙏 Remerciements

Merci à tous ceux qui ont testé le jeu et donné leurs retours !

---

<br>

## 🎮 Prêt à jouer ? 🚀

```bash
python game/shooter_gui.py
```

**Bon jeu spatial !** 🌌✨🛸

---

*Dernière mise à jour : Février 2026*

<br>

**[⬆️ Retour en haut](#-shooter-spatial-)**

</div>
