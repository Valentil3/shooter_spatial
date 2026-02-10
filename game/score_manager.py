"""
Gestionnaire de scores pour le Shooter Spatial
"""

import json
from pathlib import Path
from typing import List, Tuple
from datetime import datetime


class ScoreManager:
    """
    Gestionnaire de scores pour le Shooter Spatial
    
    Fonctionnalités :
    - Enregistrement des scores avec historique
    - Classement des meilleurs joueurs
    - Statistiques détaillées par joueur
    - Export HTML pour affichage web
    
    Attributs :
        fichier (Path) : Chemin du fichier JSON de sauvegarde
        scores (dict) : Dictionnaire contenant tous les scores
    """
    
    def __init__(self, fichier: str = "scores.json"):
        """Initialise le gestionnaire avec le fichier de scores"""
        # Utiliser un chemin absolu basé sur l'emplacement du script
        if not Path(fichier).is_absolute():
            script_dir = Path(__file__).parent
            self.fichier = script_dir / fichier
        else:
            self.fichier = Path(fichier)
        self.scores = self._charger_scores()
    
    def _charger_scores(self) -> dict:
        """Charge les scores depuis le fichier JSON"""
        if not self.fichier.exists():
            return {}
        
        try:
            with open(self.fichier, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    def _sauvegarder_scores(self):
        """Sauvegarde les scores dans le fichier JSON"""
        try:
            with open(self.fichier, 'w', encoding='utf-8') as f:
                json.dump(self.scores, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Erreur lors de la sauvegarde des scores: {e}")
    
    def enregistrer_score(self, joueur: str, score: int) -> bool:
        """
        Enregistre un nouveau score pour un joueur
        
        Args:
            joueur (str) : Nom du joueur
            score (int) : Score obtenu
        
        Returns:
            bool : True si c'est un nouveau record personnel, False sinon
        
        Note:
            L'historique conserve les 10 dernières parties
        """
        ancien_record = self.obtenir_meilleur_score(joueur)
        nouveau_record = score > ancien_record
        
        # Initialiser le joueur s'il n'existe pas
        if joueur not in self.scores:
            self.scores[joueur] = {
                "meilleur_score": 0,
                "parties_jouees": 0,
                "score_total": 0,
                "historique": []
            }
        
        # Mettre à jour les statistiques
        self.scores[joueur]["parties_jouees"] += 1
        self.scores[joueur]["score_total"] += score
        
        if score > self.scores[joueur]["meilleur_score"]:
            self.scores[joueur]["meilleur_score"] = score
        
        # Ajouter à l'historique
        self.scores[joueur]["historique"].append({
            "score": score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Garder seulement les 10 dernières parties dans l'historique
        if len(self.scores[joueur]["historique"]) > 10:
            self.scores[joueur]["historique"] = self.scores[joueur]["historique"][-10:]
        
        self._sauvegarder_scores()
        return nouveau_record
    
    def obtenir_meilleur_score(self, joueur: str) -> int:
        """Retourne le meilleur score d'un joueur"""
        if joueur in self.scores:
            return self.scores[joueur]["meilleur_score"]
        return 0
    
    def obtenir_classement(self, limite: int = 10) -> List[Tuple[str, int]]:
        """
        Retourne le classement des meilleurs joueurs
        
        Args:
            limite (int) : Nombre maximum de joueurs à retourner (défaut: 10)
        
        Returns:
            List[Tuple[str, int]] : Liste de tuples (nom_joueur, meilleur_score)
                                     triée par score décroissant
        """
        classement = [
            (joueur, data["meilleur_score"])
            for joueur, data in self.scores.items()
        ]
        
        # Trier par score décroissant
        classement.sort(key=lambda x: x[1], reverse=True)
        
        return classement[:limite]
    
    def obtenir_statistiques(self, joueur: str) -> dict:
        """Retourne les statistiques d'un joueur"""
        if joueur not in self.scores:
            return {
                "meilleur_score": 0,
                "parties_jouees": 0,
                "score_moyen": 0,
                "score_total": 0
            }
        
        data = self.scores[joueur]
        score_moyen = 0
        if data["parties_jouees"] > 0:
            score_moyen = data["score_total"] / data["parties_jouees"]
        
        return {
            "meilleur_score": data["meilleur_score"],
            "parties_jouees": data["parties_jouees"],
            "score_moyen": round(score_moyen, 1),
            "score_total": data["score_total"]
        }
    
    def afficher_classement(self):
        """Affiche le classement dans la console"""
        print("\n" + "="*50)
        print("           CLASSEMENT DES MEILLEURS JOUEURS")
        print("="*50)
        
        classement = self.obtenir_classement()
        
        if not classement:
            print("\nAucun score enregistré pour le moment.")
        else:
            for i, (joueur, score) in enumerate(classement, 1):
                if i == 1:
                    medaille = "🥇"
                elif i == 2:
                    medaille = "🥈"
                elif i == 3:
                    medaille = "🥉"
                else:
                    medaille = f"{i:2d}."
                
                print(f"{medaille} {joueur:.<30} {score:>6} pts")
        
        print("="*50 + "\n")
    
    def exporter_html(self, fichier_sortie: str = "index.html"):
        """Exporte le classement en HTML pour affichage web"""
        # Utiliser un chemin absolu basé sur l'emplacement du script
        if not Path(fichier_sortie).is_absolute():
            script_dir = Path(__file__).parent
            fichier_sortie = str(script_dir / fichier_sortie)
        
        try:
            classement = self.obtenir_classement(20)
        except Exception as e:
            print(f"❌ Erreur lors de la récupération du classement: {e}")
            classement = []
        
        html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shooter Spatial - Leaderboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        
        h1 {
            text-align: center;
            font-size: 3em;
            margin: 40px 0;
            text-shadow: 0 0 20px #00ff88;
            color: #00ff88;
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { text-shadow: 0 0 10px #00ff88, 0 0 20px #00ff88; }
            to { text-shadow: 0 0 20px #00ff88, 0 0 40px #00ff88; }
        }
        
        .leaderboard {
            background: rgba(0, 0, 0, 0.5);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 50px rgba(0, 255, 136, 0.2);
        }
        
        .score-entry {
            display: flex;
            justify-content: space-between;
            padding: 15px 20px;
            margin: 10px 0;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            transition: all 0.3s;
            border-left: 4px solid transparent;
        }
        
        .score-entry:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(10px);
        }
        
        .score-entry.top1 {
            border-left-color: #ffd700;
            background: rgba(255, 215, 0, 0.1);
        }
        
        .score-entry.top2 {
            border-left-color: #c0c0c0;
            background: rgba(192, 192, 192, 0.1);
        }
        
        .score-entry.top3 {
            border-left-color: #cd7f32;
            background: rgba(205, 127, 50, 0.1);
        }
        
        .rank {
            font-size: 1.5em;
            font-weight: bold;
            min-width: 60px;
        }
        
        .top1 .rank { color: #ffd700; }
        .top2 .rank { color: #c0c0c0; }
        .top3 .rank { color: #cd7f32; }
        
        .player {
            flex-grow: 1;
            font-size: 1.2em;
        }
        
        .score {
            font-size: 1.3em;
            font-weight: bold;
            color: #00ff88;
            min-width: 100px;
            text-align: right;
        }
        
        .no-scores {
            text-align: center;
            padding: 60px;
            font-size: 1.5em;
            color: #888;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            color: #888;
            font-size: 0.9em;
        }
        
        .update-time {
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 0.85em;
        }
        
        .refresh-btn {
            display: block;
            margin: 30px auto;
            padding: 15px 40px;
            background: #00ff88;
            color: #1a1a2e;
            border: none;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .refresh-btn:hover {
            background: #00dd77;
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 SHOOTER SPATIAL 🚀</h1>
        <div class="leaderboard">
"""
        
        if not classement:
            html += '<div class="no-scores">Aucun score enregistré pour le moment.<br><br>Lancez le jeu et faites votre meilleur score !</div>'
        else:
            for i, (joueur, score) in enumerate(classement, 1):
                classe = ""
                if i == 1:
                    classe = "top1"
                    medaille = "🥇"
                elif i == 2:
                    classe = "top2"
                    medaille = "🥈"
                elif i == 3:
                    classe = "top3"
                    medaille = "🥉"
                else:
                    medaille = f"{i}."
                
                # Échapper les caractères HTML dans le nom du joueur
                joueur_safe = joueur.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                
                html += f'''
            <div class="score-entry {classe}">
                <div class="rank">{medaille}</div>
                <div class="player">{joueur_safe}</div>
                <div class="score">{score:,} pts</div>
            </div>
'''
        
        try:
            now = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
        except:
            now = "Inconnu"
        
        html += f"""
        </div>
        <button class="refresh-btn" onclick="location.reload()">🔄 Actualiser</button>
        <div class="update-time">
            Dernière mise à jour : {now}
        </div>
        <div class="footer">
            <p>🎮 Shooter Spatial - Classement des meilleurs joueurs 🎮</p>
            <p style="margin-top: 10px; font-size: 0.8em;">Actualisez la page après chaque partie pour voir les nouveaux scores</p>
        </div>
    </div>
</body>
</html>
"""
        
        try:
            with open(fichier_sortie, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"✅ Leaderboard exporté dans {fichier_sortie}")
            return True
        except IOError as e:
            print(f"❌ Erreur lors de l'export HTML: {e}")
            return False
        except Exception as e:
            print(f"❌ Erreur inattendue lors de l'export HTML: {e}")
            return False