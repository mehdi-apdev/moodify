import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import random
from app.config import Config


class SpotifyService:
    def __init__(self):
        self.auth_manager = SpotifyOAuth(
            client_id=Config.CLIENT_ID,
            client_secret=Config.CLIENT_SECRET,
            redirect_uri=Config.REDIRECT_URI,
            scope=Config.SCOPE
        )

    def get_auth_url(self):
        return self.auth_manager.get_authorize_url()

    def get_token(self, code):
        return self.auth_manager.get_access_token(code)

    def is_token_expired(self, token_info):
        now = int(time.time())
        return token_info['expires_at'] - now < 60

    def get_recommendations(self, token, mood):
        sp = spotipy.Spotify(auth=token)

        # 1. Définition des critères audio (Target Features)
        mood_features = {
            'happy': {'target_valence': 0.8, 'min_energy': 0.6, 'seed_genres': ['pop', 'happy']},
            'sad': {'target_valence': 0.2, 'target_acousticness': 0.7, 'seed_genres': ['acoustic', 'piano', 'sad']},
            'chill': {'target_energy': 0.3, 'target_acousticness': 0.8, 'seed_genres': ['chill', 'ambient']},
            'energy': {'min_energy': 0.8, 'min_tempo': 120, 'seed_genres': ['work-out', 'electronic']},
            'party': {'min_danceability': 0.7, 'target_popularity': 60, 'seed_genres': ['party', 'dance', 'pop']},
            'focus': {'max_speechiness': 0.3, 'target_instrumentalness': 0.8, 'seed_genres': ['study', 'classical']}
        }

        features = mood_features.get(mood, mood_features['happy'])
        genres = features.pop('seed_genres')  # On extrait les genres pour les utiliser à part

        # --- STRATÉGIE EN CASCADE (CASCADE STRATEGY) ---

        raw_tracks = []

        try:
            # ÉTAPE 1 : Smart & Personal (Tes goûts + Critères stricts)
            # On récupère tes top tracks pour personnaliser
            top_tracks = sp.current_user_top_tracks(limit=3, time_range='short_term')
            seed_tracks = [t['id'] for t in top_tracks['items']]

            if seed_tracks:
                print(f"[INFO] Tentative 1 : Smart Personal pour '{mood}'")
                reco = sp.recommendations(
                    seed_tracks=seed_tracks,
                    limit=15,
                    country='FR',
                    **features  # Critères audio stricts
                )
                raw_tracks = reco.get('tracks', [])

            # ÉTAPE 2 : Smart Generic (Genres + Critères stricts) - Si étape 1 vide
            if not raw_tracks:
                print(f"[INFO] Tentative 2 : Smart Generic pour '{mood}'")
                reco = sp.recommendations(
                    seed_genres=genres[:2],  # Max 2 genres valides
                    limit=15,
                    country='FR',
                    **features
                )
                raw_tracks = reco.get('tracks', [])

            # ÉTAPE 3 : Loose Generic (Genres uniquement, sans critères stricts) - Si étape 2 vide
            if not raw_tracks:
                print(f"[INFO] Tentative 3 : Loose Generic pour '{mood}' (Critères relaxés)")
                reco = sp.recommendations(
                    seed_genres=genres[:2],
                    limit=15,
                    country='FR'
                )
                raw_tracks = reco.get('tracks', [])

        except Exception as e:
            print(f"[WARN] Erreur Algo Recommendation: {e}")

        # Si on a trouvé des musiques via l'IA, on les formate et on renvoie
        if raw_tracks:
            return self._map_tracks_to_dto(raw_tracks)

        # ÉTAPE 4 : ULTIMATE FALLBACK (Playlist Search) - Si tout le reste échoue
        print(f"[INFO] Tentative 4 : Fallback Playlist pour '{mood}'")
        return self._get_fallback_playlist_tracks(sp, mood)

    def _map_tracks_to_dto(self, tracks_list):
        """Transforme et sécurise les données pour le frontend"""
        tracks_dto = []
        seen_ids = set()  # Pour éviter les doublons

        for track in tracks_list:
            if not track or not track.get('id'):
                continue

            if track['id'] in seen_ids:
                continue

            try:
                album = track.get('album') or {'name': 'Unknown', 'images': []}
                images = album.get('images', [])
                image_url = images[0]['url'] if images else ''
                artists = track.get('artists', [])
                artist_name = artists[0]['name'] if artists else 'Unknown'

                tracks_dto.append({
                    'id': track.get('id'),
                    'title': track.get('name', 'Unknown Title'),
                    'artist': artist_name,
                    'album': album.get('name', 'Unknown Album'),
                    'albumCoverUrl': image_url,
                    'previewUrl': track.get('preview_url')
                })
                seen_ids.add(track['id'])
            except Exception:
                continue

        return tracks_dto

    def _get_fallback_playlist_tracks(self, sp, mood):
        """Méthode de secours robuste (filtre les playlists vides)"""
        mood_queries = {
            'happy': 'Happy Hits', 'sad': 'Sad Songs', 'chill': 'Chill Vibes',
            'energy': 'Workout Motivation', 'party': 'Party Mix', 'focus': 'Deep Focus'
        }
        query = mood_queries.get(mood, 'Top Hits')

        try:
            results = sp.search(q=query, type='playlist', limit=10)

            # FILTRE : On ne garde que les playlists non vides
            valid_playlists = [
                p for p in results['playlists']['items']
                if p and p.get('tracks', {}).get('total', 0) > 0
            ]

            if not valid_playlists:
                # Dernier recours absolu : Top Hits global
                print("[WARN] Aucune playlist mood trouvée, fallback sur Top Hits")
                results = sp.search(q='Top Hits', type='playlist', limit=5)
                valid_playlists = results['playlists']['items']

            if not valid_playlists:
                return []

            chosen_playlist = random.choice(valid_playlists)
            print(f"[INFO] Fallback Playlist choisie : {chosen_playlist['name']}")

            playlist_tracks = sp.playlist_items(chosen_playlist['id'], limit=30)
            raw_tracks = [item.get('track') for item in playlist_tracks.get('items', []) if item.get('track')]

            mapped = self._map_tracks_to_dto(raw_tracks)
            random.shuffle(mapped)
            return mapped[:15]

        except Exception as e:
            print(f"[ERROR] Fallback total failed: {e}")
            return []

    def create_playlist(self, token, name, track_ids):
        """Crée une playlist et y ajoute les sons"""
        sp = spotipy.Spotify(auth=token)

        # 1. On récupère l'ID de l'utilisateur
        user_id = sp.current_user()['id']

        # 2. On crée la playlist vide
        playlist = sp.user_playlist_create(user=user_id, name=name, public=False)

        # 3. On ajoute les morceaux
        if track_ids:
            sp.playlist_add_items(playlist_id=playlist['id'], items=track_ids)

        return playlist