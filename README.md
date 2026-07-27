# Wan 3.0 API — Python Wrapper

[![Powered by MuAPI](https://img.shields.io/badge/Powered%20by-MuAPI-6366f1?style=flat-square)](https://muapi.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

A focused Python SDK and MCP server for Wan 3.0-compatible AI video-generation APIs. It supports text-to-video, image-to-video, multimodal reference-to-video, file upload, and asynchronous job polling.

## Install

```bash
git clone https://github.com/Anil-matcha/Wan-3.0-API.git
cd Wan-3.0-API
pip install -r requirements.txt
cp .env.example .env
```

Set `MUAPI_API_KEY` in `.env`. Set `WAN_API_BASE_URL` only if you use a compatible provider other than the default MuAPI base URL.

## Quick start

```python
from wan_api import WanAPI

api = WanAPI()
job = api.text_to_video(
    "A cinematic tracking shot of a red fox crossing a snowy forest at sunrise",
    aspect_ratio="16:9",
    duration=5,
    resolution="720p",
)

result = api.wait_for_completion(job["request_id"])
print(result)
```

## Image to video

```python
job = api.image_to_video(
    prompt="The subject turns toward camera as a gentle breeze moves their hair.",
    images_list=["https://example.com/reference.jpg"],
    aspect_ratio="9:16",
    duration=5,
)
```

## API surface

| Method | Purpose |
| --- | --- |
| `text_to_video()` | Create a video from a text prompt. |
| `image_to_video()` | Animate one or more image URLs. |
| `reference_to_video()` | Condition a video on image, video, or audio references. |
| `upload_file()` | Upload a local reference file. |
| `get_result()` / `wait_for_completion()` | Retrieve an asynchronous job's output. |

## MCP server

Expose Wan tools to MCP-capable clients:

```bash
python mcp_server.py
```

The server provides `text_to_video`, `image_to_video`, `reference_to_video`, and `get_task_status` tools.

## Endpoint compatibility

The client uses `wan-3.0-t2v`, `wan-3.0-i2v`, and `wan-3.0-reference-to-video` paths beneath `WAN_API_BASE_URL`. If your provider names its endpoints differently, pass that provider's compatible base URL or adapt the small client module before use.

## License

[MIT](LICENSE)
