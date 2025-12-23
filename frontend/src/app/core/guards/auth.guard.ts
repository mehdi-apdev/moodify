import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router'; // Ajout de Router
import { SpotifyService } from '@core/services/spotify';
import { map, catchError, of } from 'rxjs';

export const authGuard: CanActivateFn = (route, state) => {
  const spotifyService = inject(SpotifyService);
  const router = inject(Router); // On injecte le routeur Angular

  return spotifyService.checkAuth().pipe(
    // Si le backend répond "200 OK", c'est bon, on laisse passer
    map(() => true),

    // Si le backend répond "401 Unauthorized" (ou autre erreur)
    catchError(() => {
      // On reste dans Angular et on va sur /login
      router.navigate(['/login']);

      // On bloque l'accès à la page demandée (return false)
      return of(false);
    })
  );
};
