"""A small Python client for Wan 3.0-compatible video generation APIs."""

import os
import time
from typing import Any, Dict, Iterable, Optional

import requests
from dotenv import load_dotenv

load_dotenv()


class WanAPI:
    """Submit Wan 3.0 video jobs and retrieve their asynchronous results."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("MUAPI_API_KEY")
        if not self.api_key:
            raise ValueError("An API key is required. Set MUAPI_API_KEY or pass api_key.")
        self.base_url = (base_url or os.getenv("WAN_API_BASE_URL") or "https://api.muapi.ai/api/v1").rstrip("/")
        self.headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}

    def text_to_video(
        self, prompt: str, *, aspect_ratio: str = "16:9", duration: int = 5,
        resolution: str = "720p", seed: Optional[int] = None, audio: bool = False,
    ) -> Dict[str, Any]:
        """Generate video from text using the Wan 3.0 text-to-video endpoint."""
        payload: Dict[str, Any] = {
            "prompt": prompt, "aspect_ratio": aspect_ratio, "duration": duration,
            "resolution": resolution, "audio": audio,
        }
        if seed is not None:
            payload["seed"] = seed
        return self._post("wan-3.0-t2v", payload)

    def image_to_video(
        self, prompt: str, images_list: Iterable[str], *, aspect_ratio: str = "16:9",
        duration: int = 5, resolution: str = "720p", seed: Optional[int] = None,
        audio: bool = False,
    ) -> Dict[str, Any]:
        """Animate one or more image references with a text motion prompt."""
        payload: Dict[str, Any] = {
            "prompt": prompt, "images_list": list(images_list), "aspect_ratio": aspect_ratio,
            "duration": duration, "resolution": resolution, "audio": audio,
        }
        if seed is not None:
            payload["seed"] = seed
        return self._post("wan-3.0-i2v", payload)

    def reference_to_video(
        self, prompt: str, *, images_list: Optional[Iterable[str]] = None,
        video_urls: Optional[Iterable[str]] = None, audio_urls: Optional[Iterable[str]] = None,
        aspect_ratio: str = "16:9", duration: int = 5, resolution: str = "720p",
    ) -> Dict[str, Any]:
        """Create video conditioned on image, video, or audio references."""
        payload: Dict[str, Any] = {
            "prompt": prompt, "aspect_ratio": aspect_ratio, "duration": duration,
            "resolution": resolution,
        }
        if images_list:
            payload["images_list"] = list(images_list)
        if video_urls:
            payload["video_urls"] = list(video_urls)
        if audio_urls:
            payload["audio_urls"] = list(audio_urls)
        return self._post("wan-3.0-reference-to-video", payload)

    def upload_file(self, file_path: str) -> Dict[str, Any]:
        """Upload a local reference asset for a subsequent generation request."""
        with open(file_path, "rb") as file_data:
            response = requests.post(
                f"{self.base_url}/upload_file", headers={"x-api-key": self.api_key},
                files={"file": file_data}, timeout=120,
            )
        response.raise_for_status()
        return response.json()

    def get_result(self, request_id: str) -> Dict[str, Any]:
        """Retrieve the current state and output of a generation job."""
        response = requests.get(f"{self.base_url}/predictions/{request_id}/result", headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def wait_for_completion(self, request_id: str, poll_interval: int = 5, timeout: int = 900) -> Dict[str, Any]:
        """Poll a job until it completes, fails, or reaches the timeout."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            result = self.get_result(request_id)
            status = result.get("status", "").lower()
            if status in {"completed", "succeeded", "success"}:
                return result
            if status in {"failed", "error", "cancelled"}:
                raise RuntimeError(f"Wan generation {status}: {result.get('error', result)}")
            time.sleep(poll_interval)
        raise TimeoutError(f"Timed out waiting for Wan job {request_id}.")

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(f"{self.base_url}/{path}", json=payload, headers=self.headers, timeout=120)
        response.raise_for_status()
        return response.json()
