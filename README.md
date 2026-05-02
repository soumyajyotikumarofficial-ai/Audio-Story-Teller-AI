# AI Audio Storyteller

An AI-powered web application that generates audio stories based on user-provided plot points, genre, and references.

## Features

- Generate stories using Google Gemini free-tier API
- RAG (Retrieval-Augmented Generation) using local text embeddings
- Text-to-Speech with sound effects and background music
- Support for multiple languages
- Local and cloud storage options
- Upload PDFs, YouTube URLs, and other references

## Setup

### Backend

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file with:
   ```
   GOOGLE_API_KEY=your_gemini_api_key
   ```

5. Run the backend:
   ```
   python run.py
   ```

### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend/frontend-app
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the frontend:
   ```
   ng serve
   ```

## Usage

1. Open the frontend in your browser (http://localhost:4200)
2. Enter plot points, select genre and duration
3. Upload references (PDFs, YouTube URLs, etc.)
4. Choose language and storage type
5. Generate your audio story!

## Technologies Used

- Backend: Python, FastAPI, Google Gemini free-tier API
- Frontend: Angular
- Audio: gTTS, PyDub
- Storage: Local file system, AWS S3 (optional)
- Local embeddings: Sentence Transformers