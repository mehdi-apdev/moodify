import { Component, inject, OnDestroy } from '@angular/core';
import { CommonModule, AsyncPipe, NgOptimizedImage } from '@angular/common';
import {Observable, switchMap} from 'rxjs';
import { SpotifyService } from '@core/services/spotify';
import { TrackDTO } from '@shared/api-contracts';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-playlist-view',
  standalone: true,
  imports: [CommonModule, AsyncPipe, NgOptimizedImage],
  templateUrl: './playlist-view.html',
  styleUrl: './playlist-view.scss'
})
export class PlaylistViewComponent implements OnDestroy {
  private spotifyService = inject(SpotifyService);
  private route = inject(ActivatedRoute); // On injecte la route active pour lire l'URL

  public playlist$: Observable<TrackDTO[]> = this.route.queryParams.pipe(
    switchMap(params => {
      // On récupère le mood dans l'URL (ou 'happy' par défaut)
      const currentMood = params['mood'] || 'happy';
      console.log('Chargement de la playlist pour :', currentMood);

      // On appelle le service avec le bon mood
      return this.spotifyService.getRecommendations(currentMood);
    })
  );

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
