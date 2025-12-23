/**
 * CONTRAT D'INTERFACE - MOODIFY
 * Ce fichier est la source de vérité entre le Frontend (Angular) et le Backend.
 * * CODES HTTP UTILISÉS :
 * - 200 OK : Requête réussie (renvoie les données).
 * - 201 Created : Ressource créée (ex: playlist sauvegardée).
 * - 400 Bad Request : Données envoyées invalides (ex: mood manquant).
 * - 401 Unauthorized : Token Spotify expiré ou invalide.
 * - 403 Forbidden : Accès interdit (ex: feature Premium utilisée par un Free).
 * - 404 Not Found : Ressource introuvable.
 * - 500 Internal Server Error : Erreur côté serveur (bug).
 */

// =========================================================
// 1. SECTION UTILISATEUR (User)
// =========================================================

export interface UserProfileDTO {
  id: string;            // ID unique Spotify
  displayName: string;   // Nom affiché (ex: "Mehdi Dev")
  email: string;         // Email du compte
  profileImageUrl?: string; // URL de la photo de profil (optionnelle)
  
  /**
   * Type d'abonnement Spotify.
   * 'premium' permet d'utiliser les features avancées.
   * 'free' ou 'open' restreint certaines actions.
   */
  product: 'premium' | 'free' | 'open' | string;
}

// =========================================================
// 2. SECTION QUESTIONNAIRE (Input)
// =========================================================

export interface MoodSubmissionDTO {
  /** * Valence (Positivité) 
   * 0.0 (Triste/Déprimé) à 1.0 (Joyeux/Eupharique) 
   */
  valence: number; 

  /** * Énergie
   * 0.0 (Calme/Zen) à 1.0 (Explosif/Intense) 
   */
  energy: number;

  /** * Envie de bouger (Danceability)
   * 0 = Non, 1 = Un peu, 2 = Beaucoup
   */
  danceability: number;

  /** * Présence de paroles (Instrumentalness)
   * true = Avec paroles, false = Instrumental (Focus/Travail)
   */
  hasLyrics: boolean;
}

// =========================================================
// 3. SECTION MUSIQUE & PLAYLIST (Output)
// =========================================================

export interface TrackDTO {
  id: string;            // ID Spotify (ex: "11dFghPX...")
  title: string;         // Titre de la chanson
  artist: string;        // Nom de l'artiste principal
  albumCoverUrl: string; // URL de l'image (300x300 min)
  
  /**
   * URL de l'extrait audio (30s).
   * Peut être null si Spotify ne fournit pas d'extrait pour ce titre.
   */
  previewUrl: string | null; 
  
  externalUrl: string;   // Lien profond pour ouvrir dans l'app Spotify
  spotifyUrl?: string;
  duration_ms: number;
}

export interface PlaylistResponseDTO {
  playlistId: string;    // ID unique généré par notre backend (UUID)
  createdAt: string;     // Date ISO (ex: "2025-10-24T10:00:00Z")
  tracks: TrackDTO[];    // La liste des musiques générées
}

// =========================================================
// 4. SECTION ERREURS (Shared)
// =========================================================

export interface ApiError {
  statusCode: number;    // Ex: 404
  message: string;       // Message lisible pour l'utilisateur
  timestamp: string;     // Date de l'erreur
  path?: string;         // L'URL qui a planté (optionnel)
}