import { Routes } from '@angular/router';
import { MoodSelectorComponent } from './features/mood-selector/mood-selector';
import { PlaylistViewComponent } from './features/playlist-view/playlist-view';
import { authGuard } from '@core/guards/auth.guard';

export const routes: Routes = [
  // Page d'accueil (Choix du mood) -> PROTÉGÉE
  {
    path: '',
    component: MoodSelectorComponent,
    canActivate: [authGuard]
  },

  // Page Playlist -> PROTÉGÉE
  {
    path: 'playlist',
    component: PlaylistViewComponent,
    canActivate: [authGuard]
  },

  // Redirection par défaut
  { path: '**', redirectTo: '' }
];
