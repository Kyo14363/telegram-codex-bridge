"""Optional image analysis helpers.

The bridge can enrich URL fetches that include image URLs. This module stays
optional: when requests, google-genai, or GOOGLE_API_KEY are missing, callers
receive None and the text-only URL pipeline continues.
"""

from __future__ import annotations

import base64
import logging
import os
import time
from typing import List, Optional, Tuple


logger = logging.getLogger(__name__)

try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    requests = None
    REQUESTS_AVAILABLE = False

try:
    from google import genai as _genai

    _api_key = os.getenv("GOOGLE_API_KEY")
    _genai_client = _genai.Client(api_key=_api_key) if _api_key else None
    GENAI_AVAILABLE = _genai_client is not None
except ImportError:
    _genai = None
    _genai_client = None
    GENAI_AVAILABLE = False


DEFAULT_CONFIG = {
    "IMAGE_ANALYSIS_ENABLED": False,
    "MAX_IMAGES_PER_MESSAGE": 5,
    "IMAGE_ANALYSIS_TIMEOUT": 30,
}


def download_image_to_base64(image_url: str, timeout: int = 30) -> Optional[Tuple[str, str]]:
    if not REQUESTS_AVAILABLE or requests is None:
        logger.info("[image] requests is not installed; skipping image download")
        return None

    try:
        resp = requests.get(
            image_url,
            timeout=timeout,
            headers={"User-Agent": "TelegramCodexBridge/0.1"},
        )
        if resp.status_code != 200:
            logger.warning("[image] HTTP %s for %s", resp.status_code, image_url[:120])
            return None

        content_type = resp.headers.get("Content-Type", "image/jpeg")
        if "png" in content_type:
            mime_type = "image/png"
        elif "gif" in content_type:
            mime_type = "image/gif"
        elif "webp" in content_type:
            mime_type = "image/webp"
        else:
            mime_type = "image/jpeg"

        if len(resp.content) < 1000:
            logger.warning("[image] downloaded image is too small: %s bytes", len(resp.content))
            return None
        if len(resp.content) > 20 * 1024 * 1024:
            logger.warning("[image] downloaded image is too large: %s bytes", len(resp.content))
            return None

        return base64.b64encode(resp.content).decode("utf-8"), mime_type
    except Exception as exc:
        logger.warning("[image] download failed: %s", exc)
        return None


def describe_image_via_gemini(
    b64_data: str,
    mime_type: str,
    context: str = "",
    max_retries: int = 3,
) -> Optional[str]:
    if not GENAI_AVAILABLE or _genai is None or _genai_client is None:
        return None

    prompt_text = (
        "Describe the image for an engineering or research assistant. "
        "Focus on concrete visible details, text, charts, UI state, entities, "
        "and anything useful for source review. Avoid speculation."
    )
    if context:
        prompt_text += f"\n\nRelevant surrounding text:\n{context[:800]}"

    image_bytes = base64.b64decode(b64_data)
    image_part = _genai.types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

    for attempt in range(max_retries):
        try:
            response = _genai_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt_text, image_part],
            )
            description = (response.text or "").strip()
            return description or None
        except Exception as exc:
            is_retryable = any(code in str(exc) for code in ("429", "500", "503", "Resource exhausted"))
            if is_retryable and attempt < max_retries - 1:
                time.sleep(2**attempt + 1)
                continue
            logger.warning("[image] Gemini analysis failed: %s", exc)
            return None
    return None


def describe_image_from_bytes(image_bytes: bytes, mime_type: str = "image/jpeg", context: str = "") -> Optional[str]:
    if not GENAI_AVAILABLE:
        return None
    if not image_bytes or len(image_bytes) < 1000:
        return None
    if len(image_bytes) > 20 * 1024 * 1024:
        return None

    b64_data = base64.b64encode(image_bytes).decode("utf-8")
    return describe_image_via_gemini(b64_data, mime_type, context)


def analyze_images(image_urls: List[str], context: str = "", config: dict | None = None) -> Optional[str]:
    cfg = config or DEFAULT_CONFIG
    if not cfg.get("IMAGE_ANALYSIS_ENABLED", False):
        return None
    if not GENAI_AVAILABLE:
        logger.info("[image] GOOGLE_API_KEY/google-genai unavailable; skipping image analysis")
        return None
    if not image_urls:
        return None

    max_images = int(cfg.get("MAX_IMAGES_PER_MESSAGE", 5))
    timeout = int(cfg.get("IMAGE_ANALYSIS_TIMEOUT", 30))
    descriptions = []

    for idx, image_url in enumerate(image_urls[:max_images], start=1):
        downloaded = download_image_to_base64(image_url, timeout=timeout)
        if downloaded is None:
            descriptions.append(f"[image {idx}] download failed")
            continue
        b64_data, mime_type = downloaded
        description = describe_image_via_gemini(b64_data, mime_type, context)
        descriptions.append(f"[image {idx}] {description or 'analysis failed'}")

    if not descriptions:
        return None
    return "Image analysis:\n\n" + "\n\n".join(descriptions)
