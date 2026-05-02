import { Component, OnInit } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { firstValueFrom } from 'rxjs';
import { timeout } from 'rxjs/operators';
import { StoryService } from '../story';

@Component({
  selector: 'app-story-form',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './story-form.html',
  styleUrls: ['./story-form.scss'],
})
export class StoryForm implements OnInit {
  storyForm!: FormGroup;
  isLoading = false;
  generatedStory = '';
  pdfUrl = '';
  audioUrl = '';
  selectedFiles: File[] = [];
  errorMessage = '';
  loadingProgress = 0;
  loadingMessage = '';

  genres = [
    'Fantasy',
    'Science Fiction',
    'Mystery',
    'Adventure',
    'Romance',
    'Horror',
    'Comedy',
  ];
  languages = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'Hindi' },
    { code: 'bn', name: 'Bengali' },
    { code: 'ta', name: 'Tamil' },
    { code: 'te', name: 'Telugu' },
    { code: 'mr', name: 'Marathi' },
    { code: 'gu', name: 'Gujarati' },
    { code: 'kn', name: 'Kannada' },
    { code: 'ml', name: 'Malayalam' },
    { code: 'pa', name: 'Punjabi' },
    { code: 'or', name: 'Odia' },
    { code: 'ur', name: 'Urdu' },
    { code: 'as', name: 'Assamese' },
  ];

  constructor(private fb: FormBuilder, private storyService: StoryService) {}

  ngOnInit() {
    this.storyForm = this.fb.group({
      plot_points: [
        '',
        [
          Validators.required,
          Validators.minLength(10),
        ],
      ],
      genre: ['Fantasy', Validators.required],
      duration: [5, [Validators.required, Validators.min(1)]],
      language: ['en', Validators.required],
      storage_type: ['local', Validators.required],
      youtube_urls: [''],
      other_references: [''],
    });
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files) {
      this.selectedFiles = Array.from(input.files);
    }
  }

  async onSubmit(): Promise<void> {
    if (this.storyForm.invalid) {
      this.errorMessage = 'Please fill in all required fields correctly.';
      return;
    }

    this.isLoading = true;
    this.loadingProgress = 0;
    this.errorMessage = '';
    this.generatedStory = '';
    this.pdfUrl = '';

    // Simulate progress updates while the backend responds
    const progressInterval = setInterval(() => {
      if (this.loadingProgress < 80) {
        this.loadingProgress = Math.min(80, this.loadingProgress + Math.random() * 12 + 5);
      }
    }, 500);

    try {
      this.loadingMessage = 'Analyzing your story idea...';
      this.loadingProgress = 10;

      const response = await firstValueFrom(
        this.storyService
          .generateStory({
            ...this.storyForm.value,
            files: this.selectedFiles,
          })
          .pipe(timeout(60000))
      );

      if (response) {
        this.loadingMessage = 'Finalizing...';
        this.loadingProgress = 95;
        this.generatedStory = response.story;
        this.pdfUrl = response.pdf_url.startsWith('http')
          ? response.pdf_url
          : `http://localhost:8000${response.pdf_url}`;
        this.audioUrl = response.audio_url.startsWith('http')
          ? response.audio_url
          : `http://localhost:8000${response.audio_url}`;
        this.loadingProgress = 100;
      }
    } catch (error: any) {
      const backendDetail = error?.error?.detail || error?.message || error?.statusText;
      if (error?.name === 'TimeoutError') {
        this.errorMessage =
          'The request took too long. Please try again or reduce the story duration.';
      } else if (backendDetail) {
        this.errorMessage = `Failed to generate story: ${backendDetail}`;
      } else {
        this.errorMessage =
          error instanceof Error
            ? error.message
            : 'Failed to generate story. Please try again.';
      }
    } finally {
      clearInterval(progressInterval);
      this.loadingProgress = 0;
      this.loadingMessage = '';
      setTimeout(() => {
        this.isLoading = false;
      }, 300);
    }
  }

  resetForm(): void {
    this.storyForm.reset({
      genre: 'Fantasy',
      duration: 5,
      language: 'en',
      storage_type: 'local',
    });
    this.selectedFiles = [];
    this.generatedStory = '';
    this.pdfUrl = '';
    this.audioUrl = '';
    this.errorMessage = '';
  }
}
