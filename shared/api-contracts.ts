// ---------------------------------------------------------
// OUTPUT : Ce que le Backend renvoie au Frontend
// ---------------------------------------------------------

export interface TrackDTO {
  id: string;            // ID Spotify (ex: "11dFghPX...")
  title: string;         // Titre de la chanson
  artist: string;        // Nom de l'artiste principal
  albumCoverUrl: string; // URL de l'image (300x300 min)
  previewUrl: string | null; // URL de l'extrait audio (si dispo)
  externalUrl: string;   // Lien pour ouvrir dans Spotify
}

export interface PlaylistResponseDTO {
  playlistId: string;    // ID unique généré par notre back
  tracks: TrackDTO[];    // La liste des sons
}

// ---------------------------------------------------------
// INPUT : Ce que le Frontend envoie au Backend
// ---------------------------------------------------------

export interface MoodSubmissionDTO {
  /** * Valence (Positivité) 
   * 0.0 (Triste) à 1.0 (Joyeux) 
   */
  valence: number; 

  /** * Énergie
   * 0.0 (Calme) à 1.0 (Explosif) 
   */
  energy: number;

  /** * Envie de bouger
   * 0 = Non, 1 = Un peu, 2 = Beaucoup
   */
  danceability: number;

  /** * Présence de paroles
   * true = Avec paroles, false = Instrumental
   */
  hasLyrics: boolean;
}