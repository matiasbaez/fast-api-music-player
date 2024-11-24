
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from cloudinary.utils import cloudinary_url

import cloudinary
import cloudinary.uploader
import uuid

from middleware.auth_middleware import auth_middleware
from database import get_db
from config import get_settings

from models.song import Song

router = APIRouter()
settings = get_settings()

# Configuration
cloudinary.config(
    cloud_name = settings.cloudinary_cloud_name,
    api_key = settings.cloudinary_api_key,
    api_secret = settings.cloudinary_api_secret, # Click 'View API Keys' above to copy your API secret
    secure=True
)

@router.post("/upload", status_code=201)
def upload_song(
    song: UploadFile = File(...),
    thumbnail: UploadFile = File(...),
    artist: str = Form(...),
    song_name: str = Form(...),
    hex_code: str = Form(...),
    db: Session=Depends(get_db),
    user_dic: dict=Depends(auth_middleware),):

    song_id = str(uuid.uuid4())
    upload_song_result = cloudinary.uploader.upload(song.file, resource_type="auto", folder=f'songs/{song_id}')

    upload_image_result = cloudinary.uploader.upload(thumbnail.file, resource_type="image", folder=f'songs/{song_id}')

    new_song = Song(
        id=song_id,
        title=song_name,
        artist=artist,
        song_url=upload_song_result["secure_url"],
        thumbnail_url=upload_image_result["secure_url"],
        hex_code=hex_code,
        user_id=user_dic["uid"]
    )

    db.add(new_song)
    db.commit()
    db.refresh(new_song)

    return new_song
