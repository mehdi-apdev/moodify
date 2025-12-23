import { Injectable, inject } from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@env/environment';
import { TrackDTO } from '@shared/api-contracts';

@Injectable({
  providedIn: 'root',
})
export class SpotifyService {
  // Injection de dépendance
  private http = inject(HttpClient);

  // Récupération de l'URL depuis l'environnement (Mock ou Prod)
  private apiUrl = environment.apiUrl;

  /**
   * Récupère les recommandations
   * Retourne un Observable qui contient une liste de TrackDTO
   */
  getRecommendations(mood: string): Observable<TrackDTO[]> {
    // On prépare les paramètres pour l'URL (ex: ?mood=sad)
    const params = new HttpParams().set('mood', mood);

    return this.http.get<TrackDTO[]>(`${this.apiUrl}/recommendations`, {
      params, // On attache les paramètres
      withCredentials: true
    });
  }

  createPlaylist(name: string, trackIds: string[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/playlists`, { name, track_ids: trackIds }, {
      withCredentials: true
    });
  }

  checkAuth(): Observable<any> {
    return this.http.get(`${this.apiUrl}/me`, { withCredentials: true });
  }

  // Appelle le backend pour détruire le cookie
  logout(): Observable<any> {
    return this.http.get(`${this.apiUrl}/logout`, { withCredentials: true });
  }

  saveTrack(trackId: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/tracks/save`, { track_id: trackId }, {
      withCredentials: true
    });
  }

  unlikeTrack(trackId: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/tracks/save`, {
      params: { track_id: trackId },
      withCredentials: true
    });
  }
}
