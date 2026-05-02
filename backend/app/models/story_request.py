from pydantic import BaseModel
from typing import List, Optional

class StoryRequest(BaseModel):
    plot_points: List[str]
    genre: str
    duration: int  # in minutes
    language: Optional[str] = "en"
    pdf_files: Optional[List[str]] = None
    youtube_urls: Optional[List[str]] = None
    other_references: Optional[List[str]] = None
    storage_type: str = "local"  # "local" or "cloud"