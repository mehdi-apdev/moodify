import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { SpotifyService } from '@core/services/spotify';
import { map, catchError, of } from 'rxjs';

export const authGuard: CanActivateFn = (route, state) => {
  const spotifyService = inject(SpotifyService);

  return spotifyService.checkAuth().pipe(
    map(() => true), // Si 200 OK -> On laisse passer
    catchError(() => {
      // Si 401 ou erreur -> On redirige vers le login Backend
      // On utilise window.location pour sortir de l'app Angular et aller vers Flask
      window.location.href = 'http://127.0.0.1:5000/login';
      return of(false); // On bloque la navigation Angular
    })
  );
};
