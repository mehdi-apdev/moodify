from flask import Blueprint, redirect, request, make_response
from app.services.spotify import SpotifyService
from app.config import Config

auth_bp = Blueprint('auth', __name__)
spotify_service = SpotifyService()


@auth_bp.route('/login')
def login():
    return redirect(spotify_service.get_auth_url())


@auth_bp.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = spotify_service.get_token(code)

    # Au lieu de stocker dans session['token_info'], on prépare la redirection
    response = make_response(redirect(f"{Config.FRONTEND_URL}/"))

    # On injecte le token d'accès dans un cookie sécurisé
    # Note : En prod, secure doit être True (HTTPS). En dev local, False est requis.
    response.set_cookie(
        'spotify_access_token',
        token_info['access_token'],
        httponly=True,  # Empêche le JS de lire le cookie (Protection XSS)
        secure=False,  # Mettre True si tu passes en HTTPS
        samesite='Lax',  # Protection CSRF basique
        max_age=3600  # Expire dans 1h (comme le token Spotify)
    )

    return response