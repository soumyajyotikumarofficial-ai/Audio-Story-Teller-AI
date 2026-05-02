import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { StoryForm } from './story-form/story-form';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, StoryForm],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('AI Audio Storyteller');
}
