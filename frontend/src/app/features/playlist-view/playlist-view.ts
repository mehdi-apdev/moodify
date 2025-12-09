import { Component, inject, OnDestroy } from '@angular/core';
import { CommonModule, AsyncPipe, NgOptimizedImage } from '@angular/common';
import { Observable } from 'rxjs';
import { SpotifyService } from '@core/services/spotify';
import { TrackDTO } from '@shared/api-contracts';

@Component({
  selector: 'app-playlist-view',
  standalone: true,
  imports: [CommonModule, AsyncPipe, NgOptimizedImage],
  templateUrl: './playlist-view.html',
  styleUrl: './playlist-view.scss'
})
export class PlaylistViewComponent implements OnDestroy {
  private spotifyService = inject(SpotifyService);
  public playlist$: Observable<TrackDTO[]> = this.spotifyService.getRecommendations();

  // Gestion de l'audio
  private currentAudio: HTMLAudioElement | null = null;
  public playingTrackId: string | null = null; // Pour savoir quel bouton afficher (Play ou Pause)

  togglePreview(previewUrl: string | null, trackId: string): void {
    if (!previewUrl) return;

    // Cas 1 : On clique sur le son déjà en cours -> On met en pause
    if (this.playingTrackId === trackId) {
      this.stopAudio();
      return;
    }

    // Cas 2 : On change de son -> On stop l'ancien d'abord
    this.stopAudio();

    // On lance le nouveau
    this.currentAudio = new Audio(previewUrl);
    this.currentAudio.play();
    this.playingTrackId = trackId;

    // Quand le son finit, on remet l'état à zéro
    this.currentAudio.onended = () => {
      this.playingTrackId = null;
    };
  }

  private stopAudio(): void {
    if (this.currentAudio) {
      this.currentAudio.pause();
      this.currentAudio = null;
      this.playingTrackId = null;
    }
  }

  // Nettoyage si l'utilisateur quitte la page
  ngOnDestroy(): void {
    this.stopAudio();
  }
}
