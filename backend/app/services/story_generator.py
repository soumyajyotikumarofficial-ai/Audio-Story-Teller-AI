import logging
import os
from dotenv import load_dotenv
import google.generativeai as genai
from app.services.rag_service import get_relevant_chunks

load_dotenv()
MODEL_NAME = "gemini-1.5-flash"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY is not set. Create a backend/.env file with your Gemini key.")

genai.configure(api_key=GOOGLE_API_KEY)
logger = logging.getLogger(__name__)


def _build_fallback_story(plot_points: list, genre: str, duration: int, reference_text: str) -> str:
    story_lines = [
        f"This is a {duration}-minute {genre.lower()} audio story built from your plot points.",
        "The narration flows through vivid scenes and memorable characters.",
    ]
    for index, point in enumerate(plot_points, start=1):
        clean_point = point.strip().rstrip('.')
        if clean_point:
            story_lines.append(f"Scene {index}: {clean_point.capitalize()}.")
    if reference_text and reference_text != "No additional references provided.":
        story_lines.append("It also includes inspiration from the references you provided.")
    story_lines.append("In the end, the hero learns something important and the scene closes beautifully.")
    return "\n\n".join(story_lines)


def generate_story(plot_points: list, genre: str, duration: int, references: dict):
    relevant_chunks = get_relevant_chunks(references, plot_points)
    reference_text = relevant_chunks or "No additional references provided."

    prompt_text = (
        f"Create a {duration}-minute {genre} audio story based on these plot points:\n"
        f"{chr(10).join(f'- {point}' for point in plot_points)}\n\n"
        f"References: {reference_text}\n\n"
        "Write a narrative for audio storytelling with character descriptions, "
        "scene settings, and sensory details. Include multiple characters with distinct personalities. "
        "Assign different voice types to each character (e.g., deep voice for narrator, high-pitched for child, "
        "gruff for villain). Make it engaging and concise."
    )

    try:
        model = genai.GenerativeModel(
            MODEL_NAME,
            generation_config={
                "temperature": 0.75,
                "top_p": 0.9,
                "max_output_tokens": 1000,
            }
        )
        response = model.generate_content(prompt_text)
        story_text = response.text.strip()
        if story_text:
            return story_text
        raise RuntimeError("Model returned empty text")
    except Exception:
        logger.exception("AI story generation failed, using fallback story generator")
        return _build_fallback_story(plot_points, genre, duration, reference_text)