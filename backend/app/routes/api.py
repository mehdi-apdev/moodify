import traceback
from flask import Blueprint, jsonify, request
from app.decorators import login_required
from app.services.spotify.auth_manager import SpotifyAuthManager
from app.services.spotify.spotify_service import SpotifyService

api_bp = Blueprint('api', __name__)

auth_manager = SpotifyAuthManager()
spotify_service = SpotifyService(auth_manager)

@api_bp.route('/recommendations')
@login_required
def get_recommendations():
    access_token = request.cookies.get('spotify_access_token')
    if not access_token:
        return jsonify({'error': 'Unauthorized: No token cookie found'}), 401

    mood = request.args.get('mood', 'happy')
    try:
        tracks = spotify_service.get_recommendations(access_token, mood)
        return jsonify(tracks)
    except Exception as e:
        print(f"[CRASH] Erreur sur la mood '{mood}':")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/playlists', methods=['POST'])
@login_required
def save_playlist():
    access_token = request.cookies.get('spotify_access_token')
    if not access_token:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    name = data.get('name')
    track_ids = data.get('track_ids')

    if not name or not track_ids:
        return jsonify({'error': 'Missing name or tracks'}), 400

    try:
        result = spotify_service.create_playlist(access_token, name, track_ids)
        return jsonify({'success': True, 'id': result['id']})
    except Exception as e:
        print(f"[ERROR] Save Playlist: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tracks/save', methods=['POST'])
@login_required
def save_track():
    access_token = request.cookies.get('spotify_access_token')
    data = request.json
    track_id = data.get('track_id')

    if not track_id:
        return jsonify({'error': 'Missing track_id'}), 400

    try:
        spotify_service.save_track(access_token, track_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tracks/save', methods=['DELETE'])
@login_required
def remove_track():
    access_token = request.cookies.get('spotify_access_token')
    track_id = request.args.get('track_id')

    if not track_id:
        return jsonify({'error': 'Missing track_id'}), 400

    try:
        spotify_service.remove_track(access_token, track_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
