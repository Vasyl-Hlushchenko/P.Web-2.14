from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.database.models import AuthUser
from src.repository import authusers as repository_users
from src.services.auth import auth_service
from src.conf.config import settings
from src.schemas import AuthUserDb

router = APIRouter(prefix="/avatar", tags=["avatar"])


@router.get("/me", response_model=AuthUserDb)
async def read_authusers_me(current_user: AuthUser = Depends(auth_service.get_current_user)):
    """
    The read_authusers_me function returns the current user's information.
    
    :param current_user: AuthUser: Get the current user
    :return: The current user
    :doc-author: Trelent
    """
    return current_user


@router.patch('/update', response_model=AuthUserDb)
async def update_avatar_authuser(file: UploadFile = File(), current_user: AuthUser = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    The update_avatar_authuser function takes in a file, current_user and db.
        It then uploads the file to cloudinary using the public id of RestApi13/{current_user.username}{current_user.id}
        The function then returns a user with an updated avatar.
    
    :param file: UploadFile: Upload the file to cloudinary
    :param current_user: AuthUser: Get the current user
    :param db: Session: Get the database session
    :return: A user object
    :doc-author: Trelent
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    public_id = f'RestApi13/{current_user.username}{current_user.id}'
    cloudinary.uploader.upload(file.file, public_id=public_id, overwrite=True)
    src_url = cloudinary.CloudinaryImage(public_id).build_url(width=250, height=250, crop='fill')
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user