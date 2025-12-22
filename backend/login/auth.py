from flask import Blueprint, redirect, session, request, jsonify, flash
from spotipy.oauth2 import SpotifyOAuth
from config import sp_oauth

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@auth_bp.route('/logout')
def logout():
    session.pop('spotify_token', None)
    return redirect('/')

@auth_bp.route('/callback')
def callback():
    # Récupération du code envoyé par Spotify ou erreur si refus
    code = request.args.get('code')
    error = request.args.get('error')

    if error:
        #Quand on appuie sur annulé lors de la connexion
        return redirect('/')

    if not code:
        flash("Erreur : Aucun code fourni par Spotify.", "error")
        return redirect('/')

    try:
        # Échange du code contre le token
        token_info = sp_oauth.get_access_token(code)
        access_token = token_info['access_token']
        session['spotify_token'] = access_token

        # frontend_url = 'http://localhost:4200/musique'
        # return redirect(frontend_url)

        #return only backend
        # return jsonify({
        #     "message": "Authentification réussie !",
        #     "spotify_token": access_token,
        #     "note": "Le token est stocké en session (cookie)."
        # })
        return redirect('/')

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

