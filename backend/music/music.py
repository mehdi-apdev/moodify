import json
import os
import random
import traceback
from flask import Blueprint, request, jsonify, session
import spotipy

music_bp = Blueprint('music', __name__)


#Chargement du JSON
def load_emotion_map():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, 'emotions.json')  #
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


EMOTION_MAP = load_emotion_map()

#à utiliser dans le front pour recup les valeurs
def parse_spotify_tracks(items):
    cleaned_tracks = []
    for track in items:
        album = track.get('album', {})
        images = album.get('images', [])
        image_url = images[0]['url'] if images else None
        cleaned_tracks.append({
            "id": track['id'],
            "title": track['name'],
            "artist": track['artists'][0]['name'],
            "image_url": image_url,
            "spotify_url": track['external_urls']['spotify'],
            "uri": track['uri']
        })
    return cleaned_tracks


#va lancer la génération des musiques en fonction de l'émotion
@music_bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    token = session.get('spotify_token')  #
    if not token:
        return jsonify({"error": "Non connecté"}), 401

    sp = spotipy.Spotify(auth=token)

    try:
        data = request.get_json()
        user_emotions = data.get('emotions', [])

        selected_genres = []
        for emotion in user_emotions:
            clean_key = emotion.lower()
            if clean_key in EMOTION_MAP:
                selected_genres.extend(EMOTION_MAP[clean_key])

        if not selected_genres:
            return jsonify({"error": "Aucun genre"}), 400

        unique_genres = list(set(selected_genres))
        random.shuffle(unique_genres)

        tracks_clean = []
        attempts = 0
        #va boucler 3 fois pour rechercher les musiques (parfois ne trouve rien sur la première boucle
        #3 pour être sur
        while not tracks_clean and attempts < 3 and attempts < len(unique_genres):
            chosen_genre = unique_genres[attempts]
            attempts += 1
            search_query = f'genre:"{chosen_genre}"'

            # Recherche avec retry si offset trop grand
            for offset in [random.randint(0, 50), 0]:
                results = sp.search(q=search_query, type='track', limit=12, offset=offset, market='from_token')
                items = results.get('tracks', {}).get('items', [])
                if items:
                    tracks_clean = parse_spotify_tracks(items)
                    break

        if not tracks_clean:
            return jsonify({"error": "Aucune musique trouvée"}), 404

        return jsonify({"tracks": tracks_clean})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Erreur interne"}), 500


#va permettre d'ajouter la musique générée à la playlist spotify
@music_bp.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    token = session.get('spotify_token')
    if not token:
        return jsonify({"error": "Non connecté"}), 401

    sp = spotipy.Spotify(auth=token)

    try:
        data = request.get_json()
        track_id = data.get('track_id')
        emotion_name = data.get('emotion_name')

        if not track_id or not emotion_name:
            return jsonify({"error": "Manque track_id ou emotion_name"}), 400

        user_id = sp.current_user()['id']

        #Cherche le nom exact comme stocké dans spotify
        target_name = emotion_name.strip().lower()
        playlist_name_display = emotion_name.strip().capitalize()


        playlist_id = None
        current = sp.current_user_playlists(limit=50)

        for p in current['items']:
            current_p_name = p['name'].strip().lower()
            current_p_owner = p['owner']['id']

        # Ajout du son
        uris = [track_id] if track_id.startswith("spotify:track:") else [f"spotify:track:{track_id}"]
        sp.playlist_add_items(playlist_id, uris)

        return jsonify({"success": True, "message": "Ajouté"})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500