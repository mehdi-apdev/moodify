import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
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
  getRecommendations(): Observable<TrackDTO[]> {
    // On ajoute l'option 'withCredentials: true' pour envoyer le cookie
    return this.http.get<TrackDTO[]>(`${this.apiUrl}/recommendations`, {
      withCredentials: true
    });
  }
}
