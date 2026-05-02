from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
import os
import json
from app.services import story_generator, audio_generator, rag_service

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _parse_json_list(value: str):
    if not value:
        return []
    try:
        result = json.loads(value)
        return result if isinstance(result, list) else [result]
    except json.JSONDecodeError:
        return [item.strip() for item in value.splitlines() if item.strip()]


@router.post("/generate-story")
async def generate_story(
    plot_points: str = Form(...),
    genre: str = Form(...),
    duration: int = Form(...),
    language: str = Form("en"),
    storage_type: str = Form("local"),
    youtube_urls: str = Form("[]"),
    other_references: str = Form("[]"),
    files: List[UploadFile] = File(None),
):
    try:
        plot_points_list = _parse_json_list(plot_points)
        youtube_urls_list = _parse_json_list(youtube_urls)
        other_references_list = _parse_json_list(other_references)

        file_paths = []
        if files:
            for file in files:
                file_path = os.path.join(UPLOAD_DIR, file.filename)
                with open(file_path, "wb") as f:
                    f.write(await file.read())
                file_paths.append(file_path)

        reference_data = rag_service.process_references(
            [],
            youtube_urls_list,
            other_references_list,
            file_paths,
        )

        story_text = story_generator.generate_story(
            plot_points_list,
            genre,
            duration,
            reference_data,
        )

        audio_path = audio_generator.generate_audio(
            story_text,
            language,
            storage_type,
        )

        return {
            "story": story_text,
            "audio_url": audio_path,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))