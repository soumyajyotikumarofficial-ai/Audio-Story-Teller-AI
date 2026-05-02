import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface GenerateStoryRequest {
  plot_points: string;
  genre: string;
  duration: number;
  language: string;
  storage_type: string;
  youtube_urls: string;
  other_references: string;
  files?: File[];
}

export interface GenerateStoryResponse {
  story: string;
  audio_url: string;
}

@Injectable({
  providedIn: 'root',
})
export class StoryService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  generateStory(request: GenerateStoryRequest): Observable<GenerateStoryResponse> {
    const formData = new FormData();
    formData.append('plot_points', request.plot_points);
    formData.append('genre', request.genre);
    formData.append('duration', request.duration.toString());
    formData.append('language', request.language);
    formData.append('storage_type', request.storage_type);
    formData.append('youtube_urls', request.youtube_urls);
    formData.append('other_references', request.other_references);

    if (request.files) {
      request.files.forEach((file) => {
        formData.append('files', file, file.name);
      });
    }

    return this.http.post<GenerateStoryResponse>(
      `${this.apiUrl}/generate-story`,
      formData
    );
  }
}
