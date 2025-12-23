import { Component, inject, OnDestroy, ChangeDetectorRef } from '@angular/core'; // <--- AJOUT import
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
  private cdr = inject(ChangeDetectorRef); // <--- AJOUT Injection

  public isLoading = true;
  public isSaving = false;
  public successMessage: string | null = null;

  private refreshTrigger$ = new BehaviorSubject<void>(undefined);

  public playlist$: Observable<TrackDTO[]> = combineLatest([
    this.route.queryParams,
    this.refreshTrigger$
  ]).pipe(
    map(([params]) => params['mood'] || 'happy'),
    tap(() => {
      this.isLoading = true;
      this.successMessage = null;
    }),
    switchMap(mood =>
      this.spotifyService.getRecommendations(mood).pipe(
        finalize(() => this.isLoading = false)
      )
    )
  );

  private currentAudio: HTMLAudioElement | null = null;
  public playingTrackId: string | null = null;

  regenerate(): void {
    this.isLoading = true;
    this.successMessage = null;
    this.refreshTrigger$.next();
  }

  savePlaylist(tracks: TrackDTO[]): void {
    if (!tracks || tracks.length === 0 || this.isSaving) return;

    this.isSaving = true;
    this.successMessage = null;

    const mood = this.route.snapshot.queryParams['mood'] || 'My Mood';
    const name = `Moodify ${mood.charAt(0).toUpperCase() + mood.slice(1)} Mix`;
    const trackIds = tracks.map(t => t.id);

    console.log('Starting save for:', name); // Debug

    this.spotifyService.createPlaylist(name, trackIds)
      .pipe(
        finalize(() => {
          // C'EST ICI LA CLÉ : On force l'interface à se débloquer
          this.isSaving = false;
          this.cdr.detectChanges(); // <--- UPDATE FORCÉ
          console.log('Save finished, UI updated.');
        })
      )
      .subscribe({
        next: () => {
          console.log('Success!');
          this.successMessage = `Playlist "${name}" saved to your library!`;
          this.cdr.detectChanges(); // On force l'affichage du message vert

          // On efface le message après 4 secondes
          setTimeout(() => {
            this.successMessage = null;
            this.cdr.detectChanges(); // On force la disparition du message
          }, 4000);
        },
        error: (err) => {
          console.error('Error:', err);
          alert('Error saving playlist. Check console.');
        }
      });
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

  logout(): void {
    // On appelle le backend pour supprimer le cookie
    this.spotifyService.logout().subscribe({
      next: () => {
        // Une fois déconnecté, on recharge l'application.
        // Le AuthGuard détectera l'absence de cookie et renverra vers le Login.
        window.location.href = '/';
      },
      error: (err) => {
        console.error('Erreur lors de la déconnexion', err);
        // Même en cas d'erreur, on force la redirection par sécurité
        window.location.href = '/';
      }
    });
  }

  ngOnDestroy(): void {
    this.stopAudio();
  }
}
