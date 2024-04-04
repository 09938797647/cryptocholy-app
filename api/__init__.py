import os
from urllib.parse import urlparse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

from api.authorization import validate_user_init_data
from core.settings import Config
from core.utils.cache import (
    get_cache_bytes_value,
    set_file_cache,
    format_bytes_cache_key,
)

app = FastAPI()

origins = [
    "http://localhost:3000",  # React app
    "http://localhost:8080",  # API server
    urlparse(os.getenv("NEXT_PUBLIC_API_URL")).hostname,
    "https://quiz.joincommunity.xyz",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


API_TOKEN = os.environ.get("API_TOKEN")


@app.get("/api/static/{image_path:path}")
async def get_image(image_path: str):
    key = format_bytes_cache_key(image_path)
    image = get_cache_bytes_value(key)
    if not image:
        full_path = Config.STATIC_ROOT_PATH / image_path
        if not full_path.exists():
            return JSONResponse(
                {"error": {"message": "Image not found"}}, status_code=404
            )
        image = open(Config.STATIC_ROOT_PATH / image_path, "rb").read()
        set_file_cache(key, image)

    return Response(content=image, media_type="image/jpeg")
