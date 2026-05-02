from gtts import gTTS
import os
import time


def generate_audio(story_text: str, language: str, storage_type: str):
    """
    Generate audio from story text using Google Text-to-Speech.
    
    Args:
        story_text: The story content to convert to speech
        language: Language code (e.g., 'en' for English)
        storage_type: Storage type ('local' or 'cloud')
    
    Returns:
        URL path to the generated audio file
    """
    try:
        # Truncate text for faster audio generation (limit to ~5000 chars = ~10 mins)
        max_chars = 5000
        truncated_text = story_text[:max_chars]
        if len(story_text) > max_chars:
            truncated_text += "... [Story continued]"
        
        # Generate TTS using gTTS with optimization
        tts = gTTS(
            text=truncated_text,
            lang=language,
            slow=False,
            tld='com'
        )
        
        # Save audio locally
        audio_dir = "data/audio"
        os.makedirs(audio_dir, exist_ok=True)
        
        # Use unique filename with timestamp
        timestamp = int(time.time())
        audio_filename = f"story_{language}_{timestamp}.mp3"
        audio_path = os.path.join(audio_dir, audio_filename)
        tts.save(audio_path)
        
        # Return URL path for serving
        return f"/audio/{audio_filename}"
    except Exception as e:
        raise RuntimeError(f"Error generating audio: {str(e)}")