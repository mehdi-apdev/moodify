import { Routes } from '@angular/router';
import { PlaylistViewComponent } from './features/playlist-view/playlist-view';
import { MoodSelectorComponent } from './features/mood-selector/mood-selector';

export const routes: Routes = [
  // Page d'accueil = Mood Selector
  { path: '', component: MoodSelectorComponent },

  // Page de résultats = Playlist
  { path: 'playlist', component: PlaylistViewComponent }
];
