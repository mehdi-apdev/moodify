import { Routes } from '@angular/router';
import { MoodSelectorComponent } from './features/mood-selector/mood-selector';
import { PlaylistViewComponent } from './features/playlist-view/playlist-view';
import { authGuard } from './core/guards/auth.guard'; // Vérifie que le chemin est bon (ou @core si tu as des alias)
import { Login } from './features/login/login';

export const routes: Routes = [
  // 1. La route publique (Landing Page)
  { path: 'login', component: Login },

  // 2. La racine redirige vers l'app (et déclenche le Guard)
  // Comme ça, si tu es connecté, tu arrives direct sur l'app. Sinon -> Login.
  {
    path: '',
    redirectTo: 'moods',
    pathMatch: 'full'
  },

  // 3. Page d'accueil de l'app (Choix du mood) -> PROTÉGÉE
  {
    path: 'moods',
    component: MoodSelectorComponent,
    canActivate: [authGuard]
  },

  // 4. Page Playlist -> PROTÉGÉE
  {
    path: 'playlist',
    component: PlaylistViewComponent,
    canActivate: [authGuard]
  },

  // 5. Filet de sécurité : toute adresse inconnue renvoie vers le login
  { path: '**', redirectTo: 'login' }
];
