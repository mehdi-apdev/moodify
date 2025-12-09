import { Routes } from '@angular/router';
import { PlaylistViewComponent } from './features/playlist-view/playlist-view';

export const routes: Routes = [
  { path: '', redirectTo: 'playlist', pathMatch: 'full' },
  { path: 'playlist', component: PlaylistViewComponent }
];
