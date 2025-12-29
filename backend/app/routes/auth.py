from flask import Blueprint, redirect, request, make_response, jsonify
from app.decorators import login_required
from app.services.spotify.auth_manager import SpotifyAuthManager
from app.services.spotify.spotify_service import SpotifyService
from app.config import Config

auth_bp = Blueprint('auth', __name__)

auth_manager = SpotifyAuthManager()
spotify_service = SpotifyService(auth_manager)


@auth_bp.route('/login')
def login():
    return redirect(spotify_service.auth_manager.get_auth_url())


@auth_bp.route('/logout')
def logout():
    response = jsonify({'success': True})
    response.set_cookie(
        'spotify_access_token',
        '',
        expires=0,
        httponly=True,
        samesite='Lax'
    )
    return response


@auth_bp.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = spotify_service.auth_manager.get_token(code)

    response = make_response(redirect(f"{Config.FRONTEND_URL}/"))
    response.set_cookie(
        'spotify_access_token',
        token_info['access_token'],
        httponly=True,
        secure=False,
        samesite='Lax',
        max_age=3600
    )
    return response


@auth_bp.route('/me')
@login_required
def check_auth():
    return jsonify({'authenticated': True})
