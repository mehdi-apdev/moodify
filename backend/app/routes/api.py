import traceback  # <--- Ajout important
from flask import Blueprint, jsonify, request
from app.services.spotify import SpotifyService

api_bp = Blueprint('api', __name__)
spotify_service = SpotifyService()


@api_bp.route('/recommendations')
def get_recommendations():
    access_token = request.cookies.get('spotify_access_token')

    if not access_token:
        return jsonify({'error': 'Unauthorized: No token cookie found'}), 401

    mood = request.args.get('mood', 'happy')

    try:
        tracks = spotify_service.get_recommendations(access_token, mood)
        return jsonify(tracks)

    except Exception as e:
        # On imprime l'erreur complète dans le terminal pour toi
        print(f"[CRASH] Erreur sur la mood '{mood}':")
        traceback.print_exc()

        # On renvoie 500 (Erreur Serveur) au lieu de 401, avec le message d'erreur
        return jsonify({'error': str(e)}), 500