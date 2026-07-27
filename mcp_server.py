"""MCP server exposing the Wan 3.0 Python client as agent tools."""

import json
from typing import Optional

from mcp.server.fastmcp import FastMCP
from wan_api import WanAPI

mcp = FastMCP("Wan 3.0 API Server")


def _api() -> WanAPI:
    return WanAPI()


@mcp.tool()
def text_to_video(prompt: str, aspect_ratio: str = "16:9", duration: int = 5, resolution: str = "720p", audio: bool = False) -> str:
    """Generate a Wan video from a descriptive text prompt."""
    return json.dumps(_api().text_to_video(prompt, aspect_ratio=aspect_ratio, duration=duration, resolution=resolution, audio=audio), indent=2)


@mcp.tool()
def image_to_video(prompt: str, images_list: list[str], aspect_ratio: str = "16:9", duration: int = 5, resolution: str = "720p", audio: bool = False) -> str:
    """Animate one or more image URLs into a Wan video."""
    return json.dumps(_api().image_to_video(prompt, images_list, aspect_ratio=aspect_ratio, duration=duration, resolution=resolution, audio=audio), indent=2)


@mcp.tool()
def reference_to_video(prompt: str, images_list: Optional[list[str]] = None, video_urls: Optional[list[str]] = None, audio_urls: Optional[list[str]] = None, aspect_ratio: str = "16:9", duration: int = 5, resolution: str = "720p") -> str:
    """Generate a Wan video conditioned on image, video, and/or audio URLs."""
    return json.dumps(_api().reference_to_video(prompt, images_list=images_list, video_urls=video_urls, audio_urls=audio_urls, aspect_ratio=aspect_ratio, duration=duration, resolution=resolution), indent=2)


@mcp.tool()
def get_task_status(request_id: str) -> str:
    """Get the status and outputs for a Wan generation job."""
    return json.dumps(_api().get_result(request_id), indent=2)


if __name__ == "__main__":
    mcp.run()
