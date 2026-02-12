"""
Script d'installation automatique des dépendances pour Shooter Spatial
Vérifie et installe tous les packages nécessaires pour jouer au jeu
"""

import sys
import subprocess
import os
from pathlib import Path


def verifier_python_version():
    """Vérifie que la version de Python est compatible"""
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro} détecté")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ ERREUR: Python 3.7 ou supérieur requis")
        print(f"   Version actuelle: {version.major}.{version.minor}")
        return False
    
    print("✅ Version de Python compatible")
    return True


def verifier_package(package_name, import_name=None):
    """Vérifie si un package est installé"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        return True
    except ImportError:
        return False


def installer_package(package_name):
    """Installe un package via pip"""
    print(f"📦 Installation de {package_name}...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"✅ {package_name} installé avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation de {package_name}")
        print(f"   {e}")
        return False


def verifier_tkinter():
    """Vérifie que tkinter est disponible"""
    try:
        import tkinter
        print("✅ tkinter disponible")
        return True
    except ImportError:
        print("❌ tkinter n'est pas installé")
        print("   Sur Windows: tkinter est normalement inclus avec Python")
        print("   Sur Linux: sudo apt-get install python3-tk")
        print("   Sur Mac: tkinter est normalement inclus avec Python")
        return False


def main():
    """Fonction principale du script"""
    print("="*70)
    print(" 🚀 SHOOTER SPATIAL - Installation des dépendances 🚀")
    print("="*70)
    print()
    
    # Vérifier la version de Python
    if not verifier_python_version():
        print("\n⚠️  Veuillez installer Python 3.7 ou supérieur")
        print("   Téléchargement: https://www.python.org/downloads/")
        input("\nAppuyez sur Entrée pour fermer...")
        sys.exit(1)
    
    print()
    print("-"*70)
    print("📋 Vérification des packages requis...")
    print("-"*70)
    print()
    
    # Packages à vérifier/installer
    packages = {
        # (nom_package, nom_import, requis)
        "pygame": ("pygame", "pygame", False),  # Optionnel (musique)
    }
    
    # Vérifier tkinter (ne peut pas être installé via pip sur Windows)
    print("1. Vérification de tkinter (interface graphique)...")
    tkinter_ok = verifier_tkinter()
    print()
    
    # Vérifier et installer les autres packages
    packages_a_installer = []
    index = 2
    
    for package_pip, package_import, requis in packages.values():
        print(f"{index}. Vérification de {package_pip}...")
        if verifier_package(package_pip, package_import):
            print(f"✅ {package_pip} déjà installé")
        else:
            if requis:
                print(f"❌ {package_pip} manquant (REQUIS)")
            else:
                print(f"⚠️  {package_pip} manquant (optionnel - pour la musique)")
            packages_a_installer.append((package_pip, requis))
        print()
        index += 1
    
    # Résumé
    print("-"*70)
    if not packages_a_installer and tkinter_ok:
        print("✅ Tous les packages sont installés !")
        print("   Vous pouvez lancer le jeu avec: python shooter_gui.py")
    else:
        if packages_a_installer:
            print(f"📦 {len(packages_a_installer)} package(s) à installer:")
            for pkg, requis in packages_a_installer:
                statut = "REQUIS" if requis else "OPTIONNEL"
                print(f"   - {pkg} ({statut})")
            print()
            
            reponse = input("Voulez-vous installer les packages manquants ? (o/n): ").lower()
            if reponse in ['o', 'oui', 'y', 'yes']:
                print()
                print("-"*70)
                print("🔧 Installation en cours...")
                print("-"*70)
                print()
                
                succes = []
                echecs = []
                
                for package, requis in packages_a_installer:
                    if installer_package(package):
                        succes.append(package)
                    else:
                        echecs.append((package, requis))
                    print()
                
                # Résumé de l'installation
                print("-"*70)
                if succes:
                    print(f"✅ {len(succes)} package(s) installé(s) avec succès:")
                    for pkg in succes:
                        print(f"   ✓ {pkg}")
                    print()
                
                if echecs:
                    print(f"❌ {len(echecs)} échec(s):")
                    for pkg, requis in echecs:
                        statut = "BLOQUANT" if requis else "non bloquant"
                        print(f"   ✗ {pkg} ({statut})")
                    print()
                
                if not echecs or not any(requis for _, requis in echecs):
                    print("🎮 Le jeu peut être lancé !")
                    print("   Commande: python shooter_gui.py")
                else:
                    print("⚠️  Certains packages requis n'ont pas pu être installés")
                    print("   Le jeu risque de ne pas fonctionner correctement")
            else:
                print("\n⚠️  Installation annulée")
                if any(requis for _, requis in packages_a_installer):
                    print("   Attention: des packages requis ne sont pas installés")
        
        if not tkinter_ok:
            print()
            print("⚠️  IMPORTANT: tkinter n'est pas installé")
            print("   Le jeu ne pourra pas se lancer sans tkinter")
    
    print("-"*70)
    print()
    
    # Créer un fichier .bat pour Windows
    if os.name == 'nt':  # Windows
        print("📝 Création des fichiers de lancement pour Windows...")
        try:
            # Déterminer les chemins
            game_dir = Path(__file__).parent  # game/
            root_dir = game_dir.parent  # racine du projet
            
            # Fichier d'installation (déjà à la racine normalement)
            bat_content = """@echo off
echo ============================================
echo  SHOOTER SPATIAL - Installation
echo ============================================
echo.
cd /d "%~dp0game"
python installer_dependencies.py
echo.
pause
"""
            bat_file = root_dir / "installer_dependencies.bat"
            with open(bat_file, 'w', encoding='utf-8') as f:
                f.write(bat_content)
            print(f"✅ Fichier créé à la racine: {bat_file.name}")
            print()
            
            # Fichier pour lancer la version GUI (sans fenêtre console)
            gui_bat = """@echo off
cd /d "%~dp0game"
start "" pythonw shooter_gui.py
"""
            gui_file = root_dir / "shooter_gui.bat"
            with open(gui_file, 'w', encoding='utf-8') as f:
                f.write(gui_bat)
            print(f"✅ Fichier créé à la racine: {gui_file.name}")
            print("   Double-cliquez dessus pour lancer le jeu (version graphique)")
            print()
            
            # Fichier pour lancer la version Console
            console_bat = """@echo off
title Shooter Spatial - Console
cd /d "%~dp0game"
python shooter_console.py
pause
"""
            console_file = root_dir / "shooter_console.bat"
            with open(console_file, 'w', encoding='utf-8') as f:
                f.write(console_bat)
            print(f"✅ Fichier créé à la racine: {console_file.name}")
            print("   Double-cliquez dessus pour lancer le jeu (version console)")
            print()
        except Exception as e:
            print(f"❌ Erreur lors de la création des fichiers .bat: {e}")
    
    print("="*70)
    input("\nAppuyez sur Entrée pour fermer...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation interrompue par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        input("\nAppuyez sur Entrée pour fermer...")
        sys.exit(1)
