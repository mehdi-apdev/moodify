import { Component, inject } from '@angular/core'; // Ajout de inject
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router'; // Ajout du Router

interface Mood {
  label: string;
  emoji: string;
  id: string;
}

@Component({
  selector: 'app-mood-selector',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './mood-selector.html',
  styleUrls: ['./mood-selector.scss']
})
export class MoodSelectorComponent {
  private router = inject(Router); // Injection du Router

  moods: Mood[] = [
    { label: 'Happy', emoji: '☀️', id: 'happy' },
    { label: 'Relaxed', emoji: '☕', id: 'chill' },
    { label: 'Energetic', emoji: '⚡', id: 'energy' },
    { label: 'Melancholic', emoji: '🌧️', id: 'sad' },
    { label: 'Focused', emoji: '🧠', id: 'focus' },
    { label: 'Party', emoji: '🎉', id: 'party' }
  ];

  onMoodSelect(moodId: string): void {
    console.log(`Mood selected: ${moodId}`);
    // Navigation vers la page playlist
    this.router.navigate(['/playlist'], { queryParams: { mood: moodId } });
  }
}
