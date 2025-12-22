import { Component, inject, OnDestroy } from '@angular/core';
import { CommonModule, AsyncPipe } from '@angular/common';
import { Observable, BehaviorSubject, combineLatest } from 'rxjs';
import { switchMap, map, tap, finalize } from 'rxjs/operators';
import { SpotifyService } from '@core/services/spotify';
import { TrackDTO } from '@shared/api-contracts';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-playlist-view',
  standalone: true,
  imports: [CommonModule, AsyncPipe],
  templateUrl: './playlist-view.html',
  styleUrl: './playlist-view.scss'
})
export class PlaylistViewComponent implements OnDestroy {
  private spotifyService = inject(SpotifyService);
  private route = inject(ActivatedRoute);

  // État de chargement (true par défaut au démarrage)
  public isLoading = true;

  // Déclencheur pour le bouton regenerate
  private refreshTrigger$ = new BehaviorSubject<void>(undefined);

  public playlist$: Observable<TrackDTO[]> = combineLatest([
    this.route.queryParams,
    this.refreshTrigger$
  ]).pipe(
    map(([params]) => params['mood'] || 'happy'),
    // 1. On active le chargement au début de la requête
    tap(() => this.isLoading = true),
    switchMap(mood =>
      this.spotifyService.getRecommendations(mood).pipe(
        // 2. On désactive le chargement à la fin (succès ou erreur)
        finalize(() => this.isLoading = false)
      )
    )
  );

  // Gestion Audio
  private currentAudio: HTMLAudioElement | null = null;
  public playingTrackId: string | null = null;

  regenerate(): void {
    // On force l'affichage du spinner immédiatement au clic
    this.isLoading = true;
    this.refreshTrigger$.next();
  }

  togglePreview(previewUrl: string | null, trackId: string): void {
    if (!previewUrl) return;

    if (this.playingTrackId === trackId) {
      this.stopAudio();
      return;
    }

    this.stopAudio();
    this.currentAudio = new Audio(previewUrl);
    this.currentAudio.volume = 0.5;
    this.currentAudio.play().catch(err => console.error("Erreur lecture:", err));
    this.playingTrackId = trackId;

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

  ngOnDestroy(): void {
    this.stopAudio();
  }
}
