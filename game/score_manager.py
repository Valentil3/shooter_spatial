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
                scores = json.load(f)
            
            # Migration des anciennes données: ajouter les champs manquants
            for joueur, data in scores.items():
                if "derniere_partie" not in data:
                    # Chercher la date la plus récente dans l'historique
                    if data.get("historique"):
                        derniere = data["historique"][-1]
                        data["derniere_partie"] = derniere.get("date", "Inconnue")
                        data["timestamp"] = derniere.get("timestamp", 0)
                    else:
                        data["derniere_partie"] = "Inconnue"
                        data["timestamp"] = 0
                
                # S'assurer que tous les historiques ont un timestamp
                if "historique" in data:
                    for entree in data["historique"]:
                        if "timestamp" not in entree:
                            try:
                                date_obj = datetime.strptime(entree["date"], "%Y-%m-%d %H:%M:%S")
                                entree["timestamp"] = date_obj.timestamp()
                            except:
                                entree["timestamp"] = 0
            
            return scores
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
        try:
            ancien_record = self.obtenir_meilleur_score(joueur)
            nouveau_record = score > ancien_record
            
            date_actuelle = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            timestamp = datetime.now().timestamp()
            
            # Initialiser le joueur s'il n'existe pas
            if joueur not in self.scores:
                self.scores[joueur] = {
                    "meilleur_score": 0,
                    "parties_jouees": 0,
                    "score_total": 0,
                    "derniere_partie": date_actuelle,
                    "timestamp": timestamp,
                    "historique": []
                }
            
            # Mettre à jour les statistiques
            self.scores[joueur]["parties_jouees"] += 1
            self.scores[joueur]["score_total"] += score
            self.scores[joueur]["derniere_partie"] = date_actuelle
            self.scores[joueur]["timestamp"] = timestamp
            
            if score > self.scores[joueur]["meilleur_score"]:
                self.scores[joueur]["meilleur_score"] = score
            
            # Ajouter à l'historique
            self.scores[joueur]["historique"].append({
                "score": score,
                "date": date_actuelle,
                "timestamp": timestamp
            })
            
            # Garder seulement les 10 dernières parties dans l'historique
            if len(self.scores[joueur]["historique"]) > 10:
                self.scores[joueur]["historique"] = self.scores[joueur]["historique"][-10:]
            
            self._sauvegarder_scores()
            print(f"✅ Score enregistré: {joueur} - {score} pts")
            return nouveau_record
        except Exception as e:
            print(f"❌ Erreur lors de l'enregistrement du score: {e}")
            return False
    
    def obtenir_meilleur_score(self, joueur: str) -> int:
        """Retourne le meilleur score d'un joueur"""
        if joueur in self.scores:
            return self.scores[joueur]["meilleur_score"]
        return 0
    
    def obtenir_classement(self, limite: int = 10, tri: str = "score", ordre: str = "desc") -> List[Tuple]:
        """
        Retourne le classement des meilleurs joueurs
        
        Args:
            limite (int) : Nombre maximum de joueurs à retourner (défaut: 10)
            tri (str) : Mode de tri ('score', 'date', 'pseudo') (défaut: 'score')
            ordre (str) : Ordre de tri ('asc' ou 'desc') (défaut: 'desc')
        
        Returns:
            List[Tuple] : Liste de tuples (nom_joueur, meilleur_score, date, timestamp)
                         triée selon le mode choisi
        """
        classement = [
            (joueur, 
             data["meilleur_score"],
             data.get("derniere_partie", "Inconnue"),
             data.get("timestamp", 0))
            for joueur, data in self.scores.items()
        ]
        
        # Déterminer si reverse (True = décroissant, False = croissant)
        reverse = (ordre == "desc")
        
        # Trier selon le mode choisi
        if tri == "score":
            # Trier par score
            classement.sort(key=lambda x: x[1], reverse=reverse)
        elif tri == "date":
            # Trier par date (timestamp)
            classement.sort(key=lambda x: x[3], reverse=reverse)
        elif tri == "pseudo":
            # Trier par ordre alphabétique
            classement.sort(key=lambda x: x[0].lower(), reverse=reverse)
        else:
            # Par défaut: tri par score décroissant
            classement.sort(key=lambda x: x[1], reverse=reverse)
        
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
    
    def afficher_classement(self, tri: str = "score", ordre: str = "desc"):
        """Affiche le classement dans la console"""
        print("\n" + "="*70)
        titre = "CLASSEMENT DES MEILLEURS JOUEURS"
        ordre_texte = "↓" if ordre == "desc" else "↑"
        if tri == "date":
            titre += f" (Par date {ordre_texte})"
        elif tri == "pseudo":
            titre += f" (Par pseudo {ordre_texte})"
        else:
            titre += f" (Par score {ordre_texte})"
        print(f"           {titre}")
        print("="*70)
        
        classement = self.obtenir_classement(tri=tri, ordre=ordre)
        
        if not classement:
            print("\nAucun score enregistré pour le moment.")
        else:
            for i, (joueur, score, date, _) in enumerate(classement, 1):
                if i == 1 and tri == "score":
                    medaille = "🥇"
                elif i == 2 and tri == "score":
                    medaille = "🥈"
                elif i == 3 and tri == "score":
                    medaille = "🥉"
                else:
                    medaille = f"{i:2d}."
                
                # Afficher avec date
                print(f"{medaille} {joueur:.<25} {score:>6} pts  │  {date}")
        
        print("="*70 + "\n")
    
    def exporter_html(self, fichier_sortie: str = "index.html"):
        """Exporte le classement en HTML pour affichage web avec tri interactif"""
        # Utiliser un chemin absolu basé sur l'emplacement du script
        if not Path(fichier_sortie).is_absolute():
            script_dir = Path(__file__).parent
            fichier_sortie = str(script_dir / fichier_sortie)
        
        try:
            # Récupérer tous les classements (avec les deux ordres)
            classement_score_desc = self.obtenir_classement(20, tri="score", ordre="desc")
            classement_score_asc = self.obtenir_classement(20, tri="score", ordre="asc")
            classement_date_desc = self.obtenir_classement(20, tri="date", ordre="desc")
            classement_date_asc = self.obtenir_classement(20, tri="date", ordre="asc")
            classement_pseudo_desc = self.obtenir_classement(20, tri="pseudo", ordre="desc")
            classement_pseudo_asc = self.obtenir_classement(20, tri="pseudo", ordre="asc")
        except Exception as e:
            print(f"❌ Erreur lors de la récupération du classement: {e}")
            classement_score_desc = []
            classement_score_asc = []
            classement_date_desc = []
            classement_date_asc = []
            classement_pseudo_desc = []
            classement_pseudo_asc = []
        
        html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shooter Spatial - Leaderboard 🚀</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Courier New', monospace;
            background: #0a0a1e;
            color: #fff;
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }
        
        /* Animation d'étoiles en arrière-plan */
        .stars {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
        }
        
        .star {
            position: absolute;
            width: 2px;
            height: 2px;
            background: white;
            border-radius: 50%;
            animation: twinkle 3s infinite;
        }
        
        @keyframes twinkle {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 1; }
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }
        
        /* Header du projet */
        .header {
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, rgba(26, 26, 46, 0.95) 0%, rgba(22, 33, 62, 0.95) 100%);
            border-radius: 20px;
            margin-bottom: 30px;
            box-shadow: 0 10px 50px rgba(0, 255, 136, 0.2);
            border: 2px solid rgba(0, 255, 136, 0.3);
        }
        
        h1 {
            font-size: 3.5em;
            text-shadow: 0 0 30px #00ff88, 0 0 60px #00ff88;
            color: #00ff88;
            animation: glow 2s ease-in-out infinite alternate;
            margin-bottom: 10px;
        }
        
        @keyframes glow {
            from { text-shadow: 0 0 20px #00ff88, 0 0 40px #00ff88; }
            to { text-shadow: 0 0 30px #00ff88, 0 0 70px #00ff88; }
        }
        
        .subtitle {
            font-size: 1.2em;
            color: #888;
            margin-bottom: 20px;
        }
        
        .badges {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 15px;
        }
        
        .badge {
            background: rgba(0, 255, 136, 0.2);
            color: #00ff88;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            border: 1px solid #00ff88;
        }
        
        /* Section info du jeu */
        .game-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .info-card {
            background: rgba(0, 0, 0, 0.5);
            padding: 20px;
            border-radius: 15px;
            border: 2px solid rgba(0, 255, 136, 0.2);
            transition: all 0.3s;
        }
        
        .info-card:hover {
            border-color: #00ff88;
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3);
        }
        
        .info-card h3 {
            color: #00ff88;
            margin-bottom: 10px;
            font-size: 1.3em;
        }
        
        .info-card p {
            color: #ccc;
            line-height: 1.6;
            font-size: 0.95em;
        }
        
        .info-card ul {
            list-style: none;
            padding-left: 0;
            color: #ccc;
        }
        
        .info-card ul li {
            padding: 5px 0;
            padding-left: 20px;
            position: relative;
        }
        
        .info-card ul li::before {
            content: "▸";
            position: absolute;
            left: 0;
            color: #00ff88;
        }
        
        /* Section leaderboard */
        .leaderboard-section {
            background: rgba(0, 0, 0, 0.5);
            border-radius: 20px;
            padding: 30px;
            border: 2px solid rgba(0, 255, 136, 0.3);
        }
        
        .section-title {
            text-align: center;
            font-size: 2em;
            color: #ffd700;
            margin-bottom: 25px;
            text-shadow: 0 0 20px #ffd700;
        }
        
        .sort-buttons {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        
        .sort-group {
            display: flex;
            align-items: center;
            gap: 5px;
            background: rgba(0, 0, 0, 0.3);
            padding: 5px;
            border-radius: 10px;
        }
        
        .sort-btn {
            padding: 10px 20px;
            background: rgba(0, 255, 136, 0.2);
            color: #00ff88;
            border: 2px solid #00ff88;
            border-radius: 8px;
            font-size: 0.95em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            font-family: 'Courier New', monospace;
        }
        
        .sort-btn:hover {
            background: rgba(0, 255, 136, 0.4);
            transform: translateY(-2px);
        }
        
        .sort-btn.active {
            background: #00ff88;
            color: #1a1a2e;
        }
        
        .order-icon {
            font-size: 0.8em;
            opacity: 0.7;
        }
        
        .leaderboard {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 15px;
            padding: 20px;
        }
        
        .score-entry {
            display: grid;
            grid-template-columns: 60px 1fr auto auto;
            gap: 15px;
            padding: 15px 20px;
            margin: 8px 0;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            transition: all 0.3s;
            border-left: 4px solid transparent;
            align-items: center;
        }
        
        .score-entry:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(10px);
        }
        
        .score-entry.top1 {
            border-left-color: #ffd700;
            background: rgba(255, 215, 0, 0.15);
        }
        
        .score-entry.top2 {
            border-left-color: #c0c0c0;
            background: rgba(192, 192, 192, 0.15);
        }
        
        .score-entry.top3 {
            border-left-color: #cd7f32;
            background: rgba(205, 127, 50, 0.15);
        }
        
        .rank {
            font-size: 1.5em;
            font-weight: bold;
            text-align: center;
        }
        
        .top1 .rank { color: #ffd700; }
        .top2 .rank { color: #c0c0c0; }
        .top3 .rank { color: #cd7f32; }
        
        .player {
            font-size: 1.2em;
            font-weight: bold;
        }
        
        .score {
            font-size: 1.3em;
            font-weight: bold;
            color: #00ff88;
            text-align: right;
            min-width: 120px;
        }
        
        .date {
            font-size: 0.85em;
            color: #888;
            min-width: 150px;
            text-align: right;
        }
        
        .no-scores {
            text-align: center;
            padding: 60px 20px;
            font-size: 1.3em;
            color: #888;
        }
        
        .footer {
            text-align: center;
            margin-top: 50px;
            padding: 30px;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 15px;
            border: 2px solid rgba(0, 255, 136, 0.2);
        }
        
        .footer h3 {
            color: #00ff88;
            margin-bottom: 15px;
        }
        
        .footer p {
            color: #888;
            margin: 8px 0;
        }
        
        .update-time {
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }
        
        .refresh-btn {
            display: block;
            margin: 30px auto;
            padding: 15px 40px;
            background: linear-gradient(135deg, #00ff88, #00dd77);
            color: #1a1a2e;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 5px 20px rgba(0, 255, 136, 0.4);
        }
        
        .refresh-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 30px rgba(0, 255, 136, 0.6);
        }
        
        .hidden {
            display: none;
        }
        
        @media (max-width: 768px) {
            h1 { font-size: 2em; }
            .section-title { font-size: 1.5em; }
            .game-info { grid-template-columns: 1fr; }
            .score-entry {
                grid-template-columns: 50px 1fr;
                gap: 10px;
            }
            .score, .date {
                grid-column: 2;
                text-align: left;
            }
        }
    </style>
</head>
<body>
    <div class="stars" id="stars"></div>
    
    <div class="container">
        <!-- Header du projet -->
        <div class="header">
            <h1>🚀 SHOOTER SPATIAL 🌌</h1>
            <p class="subtitle">Un jeu de tir spatial développé en Python</p>
            <div class="badges">
                <span class="badge">🐍 Python 3.7+</span>
                <span class="badge">🎮 POO + Événementiel</span>
                <span class="badge">🎓 Projet Licence Info</span>
                <span class="badge">🏆 Leaderboard en temps réel</span>
            </div>
        </div>
        
        <!-- Section Leaderboard -->
        <div class="leaderboard-section">
            <h2 class="section-title">🏆 LEADERBOARD MONDIAL</h2>
            
            <div class="sort-buttons">
                <div class="sort-group">
                    <button class="sort-btn active" onclick="changeTri('score', 'desc')" id="btn-score-desc">🏆 Score <span class="order-icon">↓</span></button>
                    <button class="sort-btn" onclick="changeTri('score', 'asc')" id="btn-score-asc">🏆 Score <span class="order-icon">↑</span></button>
                </div>
                <div class="sort-group">
                    <button class="sort-btn" onclick="changeTri('date', 'desc')" id="btn-date-desc">📅 Date <span class="order-icon">↓</span></button>
                    <button class="sort-btn" onclick="changeTri('date', 'asc')" id="btn-date-asc">📅 Date <span class="order-icon">↑</span></button>
                </div>
                <div class="sort-group">
                    <button class="sort-btn" onclick="changeTri('pseudo', 'desc')" id="btn-pseudo-desc">👤 Pseudo <span class="order-icon">Z→A</span></button>
                    <button class="sort-btn" onclick="changeTri('pseudo', 'asc')" id="btn-pseudo-asc">👤 Pseudo <span class="order-icon">A→Z</span></button>
                </div>
            </div>
            
            <div class="leaderboard">
"""
        
        # Fonction pour générer les entrées de score
        def generer_entrees(classement, tri_actif, ordre):
            if not classement:
                return '<div class="no-scores">Aucun score enregistré pour le moment.<br><br>Lancez le jeu et faites votre meilleur score !</div>'
            
            entrees = ""
            for i, (joueur, score, date, _) in enumerate(classement, 1):
                classe = ""
                if tri_actif == "score" and ordre == "desc":
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
                else:
                    medaille = f"{i}."
                
                # Échapper les caractères HTML dans le nom du joueur
                joueur_safe = joueur.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                
                # Formater la date
                date_affichage = date if date != "Inconnue" else "-"
                
                entrees += f'''
            <div class="score-entry {classe}">
                <div class="rank">{medaille}</div>
                <div class="player">{joueur_safe}</div>
                <div class="score">{score:,} pts</div>
                <div class="date">{date_affichage}</div>
            </div>
'''
            return entrees
        
        # Générer les 6 vues (3 tris × 2 ordres)
        html += f'''
            <div id="classement-score-desc" class="classement-vue">
                {generer_entrees(classement_score_desc, "score", "desc")}
            </div>
            <div id="classement-score-asc" class="classement-vue hidden">
                {generer_entrees(classement_score_asc, "score", "asc")}
            </div>
            <div id="classement-date-desc" class="classement-vue hidden">
                {generer_entrees(classement_date_desc, "date", "desc")}
            </div>
            <div id="classement-date-asc" class="classement-vue hidden">
                {generer_entrees(classement_date_asc, "date", "asc")}
            </div>
            <div id="classement-pseudo-desc" class="classement-vue hidden">
                {generer_entrees(classement_pseudo_desc, "pseudo", "desc")}
            </div>
            <div id="classement-pseudo-asc" class="classement-vue hidden">
                {generer_entrees(classement_pseudo_asc, "pseudo", "asc")}
            </div>
'''
        
        try:
            now = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
        except:
            now = "Inconnu"
        
        html += f"""
            </div>
            
            <button class="refresh-btn" onclick="location.reload()">🔄 Actualiser les scores</button>
            
            <div class="update-time">
                Dernière mise à jour : {now}
            </div>
        </div>
        
        <!-- Informations sur le jeu -->
        <div class="game-info" style="margin-top: 30px;">
            <div class="info-card">
                <h3>🎯 Objectif</h3>
                <p>Survie spatiale : détruisez un maximum d'ennemis, collectez des bonus et battez les records !</p>
            </div>
            
            <div class="info-card">
                <h3>💎 5 Types de Bonus</h3>
                <ul>
                    <li>💚 Vie +1 (max 5)</li>
                    <li>⚡ Vitesse +50%</li>
                    <li>🔫 Tir Double</li>
                    <li>🔥 Tir Triple</li>
                    <li>⚡ Tir Rapide</li>
                </ul>
            </div>
            
            <div class="info-card">
                <h3>📈 Gameplay</h3>
                <ul>
                    <li>Difficulté progressive</li>
                    <li>+10 points par ennemi</li>
                    <li>3 vies de départ</li>
                    <li>Invincibilité temporaire</li>
                </ul>
            </div>
            
            <div class="info-card">
                <h3>🕹️ Commandes</h3>
                <ul>
                    <li>← → ↑ ↓ ou ZQSD : Déplacement</li>
                    <li>Espace : Tirer</li>
                    <li>P : Pause musique</li>
                    <li>ESC : Quitter</li>
                </ul>
            </div>
        </div>
    </div>
    
    <script>
        // Génération des étoiles animées
        function createStars() {{
            const starsContainer = document.getElementById('stars');
            const starCount = 150;
            
            for (let i = 0; i < starCount; i++) {{
                const star = document.createElement('div');
                star.className = 'star';
                star.style.left = Math.random() * 100 + '%';
                star.style.top = Math.random() * 100 + '%';
                star.style.animationDelay = Math.random() * 3 + 's';
                star.style.animationDuration = (Math.random() * 2 + 2) + 's';
                starsContainer.appendChild(star);
            }}
        }}
        
        createStars();
        
        // Gestion du tri
        function changeTri(type, ordre) {{
            // Masquer tous les classements
            document.querySelectorAll('.classement-vue').forEach(el => {{
                el.classList.add('hidden');
            }});
            
            // Retirer la classe active de tous les boutons
            document.querySelectorAll('.sort-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            
            // Afficher le classement sélectionné
            const classementId = 'classement-' + type + '-' + ordre;
            document.getElementById(classementId).classList.remove('hidden');
            
            // Activer le bouton correspondant
            const btnId = 'btn-' + type + '-' + ordre;
            document.getElementById(btnId).classList.add('active');
        }}
    </script>
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
