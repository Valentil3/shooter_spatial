"""
Serveur HTTP local pour afficher le site web des scores
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

# Configuration
PORT = 8000
DOSSIER = Path(__file__).parent

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handler HTTP personnalisé"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DOSSIER), **kwargs)
    
    def end_headers(self):
        # Ajouter les headers CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Personnalise les messages de log"""
        print(f"[{self.address_string()}] {format % args}")

def demarrer_serveur():
    """Démarre le serveur HTTP"""
    
    print("="*60)
    print("  🚀 SERVEUR WEB - SHOOTER SPATIAL")
    print("="*60)
    print()
    
    # Vérifier que index.html existe
    fichier_index = DOSSIER / "index.html"
    fichier_scores = DOSSIER / "scores.json"
    
    if not fichier_index.exists():
        print("❌ ERREUR : index.html non trouvé !")
        print(f"   Recherché dans : {DOSSIER}")
        return
    
    if not fichier_scores.exists():
        print("⚠️  ATTENTION : scores.json non trouvé !")
        print("   Le site web ne pourra pas afficher les scores.")
        print()
    
    print(f"📂 Dossier : {DOSSIER}")
    print(f"🌐 Port    : {PORT}")
    print()
    
    # Créer le serveur
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            url = f"http://localhost:{PORT}/index.html"
            
            print(f"✅ Serveur démarré avec succès !")
            print()
            print(f"🌍 Ouvrez votre navigateur à l'adresse :")
            print(f"   {url}")
            print()
            print("💡 Le navigateur devrait s'ouvrir automatiquement...")
            print()
            print("⚠️  Pour arrêter le serveur : Ctrl+C")
            print("="*60)
            print()
            
            # Ouvrir automatiquement le navigateur
            webbrowser.open(url)
            
            # Démarrer le serveur
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n")
        print("="*60)
        print("🛑 Serveur arrêté par l'utilisateur")
        print("="*60)
    except OSError as e:
        if e.errno == 10048 or e.errno == 98:  # Port déjà utilisé
            print(f"❌ ERREUR : Le port {PORT} est déjà utilisé !")
            print()
            print("💡 Solutions :")
            print(f"   1. Changez le PORT dans le script (actuellement {PORT})")
            print(f"   2. Ou fermez l'application qui utilise le port {PORT}")
        else:
            print(f"❌ ERREUR : {e}")

if __name__ == "__main__":
    demarrer_serveur()