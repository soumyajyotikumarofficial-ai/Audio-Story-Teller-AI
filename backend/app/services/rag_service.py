import os
import re
from collections import Counter
from pypdf import PdfReader
from youtube_transcript_api import YouTubeTranscriptApi


def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def _tokenize(text: str):
    return re.findall(r"\b\w+\b", text.lower())


def _split_text(text: str, chunk_size: int = 600, overlap: int = 100):
    text = _clean_text(text)
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end].strip())
        start += chunk_size - overlap
    return chunks


def _load_pdf(path: str) -> str:
    reader = PdfReader(path)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def _load_youtube_transcript(url: str) -> str:
    if "youtube.com" not in url and "youtu.be" not in url:
        return ""
    video_id = None
    if "v=" in url:
        video_id = url.split("v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[-1].split("?")[0]
    if not video_id:
        return ""

    try:
        transcript = YouTubeTranscriptApi().fetch(video_id)
        return " ".join(item.text for item in transcript)
    except Exception:
        return ""


def process_references(pdf_files, youtube_urls, other_refs, uploaded_files):
    texts = []

    for pdf in pdf_files + uploaded_files:
        if pdf.lower().endswith(".pdf") and os.path.exists(pdf):
            texts.append(_load_pdf(pdf))

    for url in youtube_urls:
        transcript = _load_youtube_transcript(url)
        if transcript:
            texts.append(transcript)

    for ref in other_refs:
        if os.path.isfile(ref):
            with open(ref, "r", encoding="utf-8", errors="ignore") as f:
                texts.append(f.read())
        else:
            texts.append(ref)

    chunks = []
    for text in texts:
        chunks.extend(_split_text(text))

    return {"chunks": chunks}


def _overlap_score(query_tokens, chunk_tokens):
    query_counter = Counter(query_tokens)
    chunk_counter = Counter(chunk_tokens)
    return sum(min(query_counter[token], chunk_counter[token]) for token in query_counter)


def get_relevant_chunks(reference_data, plot_points):
    if not reference_data or not plot_points or len(reference_data["chunks"]) == 0:
        return ""

    query = " ".join(plot_points)
    query_tokens = _tokenize(query)

    scored_chunks = []
    for chunk in reference_data["chunks"]:
        chunk_tokens = _tokenize(chunk)
        score = _overlap_score(query_tokens, chunk_tokens)
        if score > 0:
            scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda item: item[0], reverse=True)
    selected_chunks = [chunk for _, chunk in scored_chunks[:4]]
    return "\n\n".join(selected_chunks)