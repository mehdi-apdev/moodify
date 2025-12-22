from flask import Flask
from flask_cors import CORS
from login.auth import auth_bp
from music.music import *

app = Flask(__name__)

app.secret_key = 'Yemp3PLOUGTUBZSXTYU458524568BURNOUT7418tgv52963aze0rty0'

#REMETTRE POUR FRONTEND
# CORS(app, origins=["http://localhost:4200"], supports_credentials=True)
#TEST UNIQUEMENT EN BACKEND
CORS(app, supports_credentials=True)
#Liaison connexion
app.register_blueprint(auth_bp)
#Liaison choix emotion et génération playlist
app.register_blueprint(music_bp, url_prefix='/music')

@app.route('/')
def home():
    token = session.get('spotify_token')

    if not token:
        return '<a href="/login">Se connecter avec Spotify</a>'
    else:
        return """
                <a href="/logout">Se déconnecter</a>
                <p>Connecté ! Choisissez une émotion pour générer une playlist.</p>

        <label>Emotion :</label>
        <select id="emo">
            <option value="joyeux">Joyeux</option>
            <option value="triste">Triste</option>
            <option value="sport">Sport</option>
            <option value="colere">Colère</option>
            <option value="detendu">Détendu</option>
            <option value="soiree">Soirée</option>
        </select>
        
        <button onclick="lancerRecherche()">Générer les musiques 🎵</button>
        
        <hr>
        
        <div id="resultats"></div>

        <script>
            // --- FONCTION 1 : Récupérer et afficher les musiques ---
            async function lancerRecherche() {
                const emo = document.getElementById('emo').value;
                const div = document.getElementById('resultats');
                div.innerHTML = "Chargement en cours...";

                try {
                    // Appel à l'API get_recommendations (préfixe /music)
                    const res = await fetch('/music/recommendations', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({emotions: [emo]})
                    });
                    
                    const data = await res.json();
                    div.innerHTML = ""; // On vide le message de chargement

                    if(data.error) {
                        div.innerHTML = "Erreur : " + data.error;
                        return;
                    }

                    // On boucle sur chaque musique pour créer l'affichage
                    if(data.tracks && data.tracks.length > 0) {
                        data.tracks.forEach(track => {
                            // Pour chaque musique, on ajoute une ligne HTML avec le bouton Ajouter
                            div.innerHTML += `
                                <div style="margin-bottom: 15px; border-bottom: 1px solid #ccc; padding-bottom: 10px;">
                                    <strong>${track.title}</strong> - <em>${track.artist}</em><br>
                                    
                                    <button onclick="ajouter('${track.id}', '${emo}', this)" style="margin-top:5px; cursor:pointer;">
                                        ➕ Ajouter à la playlist
                                    </button>
                                </div>
                            `;
                        });
                    } else {
                        div.innerHTML = "Aucune musique trouvée.";
                    }

                } catch(e) {
                    div.innerHTML = "Erreur JS : " + e;
                }
            }

            // --- FONCTION 2 : Ajouter une musique spécifique ---
            async function ajouter(id, emotion, btn) {
                // Petit effet visuel
                btn.disabled = true;
                btn.innerText = "Ajout en cours...";

                try {
                    // Appel à l'API add_to_playlist
                    const res = await fetch('/music/add_to_playlist', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({track_id: id, emotion_name: emotion})
                    });
                    
                    const data = await res.json();

                    if(data.success) {
                        btn.innerText = "✅ Ajouté !";
                        // Optionnel : on peut laisser le bouton désactivé pour éviter les doublons
                    } else {
                        btn.innerText = "❌ Erreur";
                        alert(data.error);
                        btn.disabled = false; // On réactive si erreur pour réessayer
                    }
                } catch(e) {
                    console.error(e);
                    btn.innerText = "Erreur Réseau";
                }
            }
        </script>
        """

if __name__ == '__main__':
    #Lancement du serveur sur le port 5000
    app.run(port=5000, debug=True)



