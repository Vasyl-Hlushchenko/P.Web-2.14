from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session


from src.database.db import get_db
from src.database.models import AuthUser
from src.schemas import UserModel, UserResponse
from src.repository import users as repository_users
from src.services.auth import auth_service

router = APIRouter(prefix='/users', tags=["users"])


@router.get("/all", response_model=List[UserResponse], description='No more than 15 requests per 2 minute',
            dependencies=[Depends(RateLimiter(times=15, seconds=120))])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     current_user: AuthUser = Depends(auth_service.get_current_user)):
    """
    The read_users function returns a list of users.
    
    :param skip: int: Specify how many records to skip
    :param limit: int: Limit the number of users returned
    :param db: Session: Pass the database session to the repository
    :param current_user: AuthUser: Get the current user
    :return: A list of users
    :doc-author: Trelent
    """
    users = await repository_users.get_users(skip, limit, db, current_user)
    return users


@router.get("/find/{some_info}", response_model=List[UserResponse], description='No more than 15 requests per 2 minute',
            dependencies=[Depends(RateLimiter(times=15, seconds=120))])
async def find_users_by_some_info(some_info: str, db: Session = Depends(get_db),
                                  current_user: AuthUser = Depends(auth_service.get_current_user)):
    """
    The find_users_by_some_info function is used to find users by some info.
        Args:
            some_info (str): The user's name, email or phone number.
    
    :param some_info: str: Pass the search string to the function
    :param db: Session: Get the database session
    :param current_user: AuthUser: Get the current user
    :return: A list of users
    :doc-author: Trelent
    """
    users = await repository_users.get_users_by_some_info(some_info, db, current_user)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
    return users


@router.get("/birthday/{days}", response_model=List[UserResponse], description='No more than 15 requests per 2 minute',
            dependencies=[Depends(RateLimiter(times=15, seconds=120))])
async def find_birthday_per_week(days: int, db: Session = Depends(get_db),
                                 current_user: AuthUser = Depends(auth_service.get_current_user)):
    """
    The find_birthday_per_week function returns a list of users that have their birthday in the next 7 days.
        The function takes an integer as input, which is the number of days to look ahead for birthdays.
        It then queries the database and returns a list of users with their birthday in that time frame.
    
    :param days: int: Specify the amount of days that we want to search for birthdays
    :param db: Session: Inject the database session into the function
    :param current_user: AuthUser: Get the current user
    :return: A list of users with a birthday in the next 7 days
    :doc-author: Trelent
    """
    users = await repository_users.get_birthday_per_week(days, db, current_user)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
    return users


@router.get("/{user_id}", response_model=UserResponse, description='No more than 15 requests per 2 minute',
            dependencies=[Depends(RateLimiter(times=15, seconds=120))])
async def read_user(user_id: int, db: Session = Depends(get_db),
                    current_user: AuthUser = Depends(auth_service.get_current_user)):
    """
    The read_user function is a GET endpoint that returns the user with the given ID.
    If no such user exists, it raises an HTTP 404 error.
    
    :param user_id: int: Specify the type of the parameter
    :param db: Session: Pass the database session to the repository layer
    :param current_user: AuthUser: Get the current user
    :return: A user
    :doc-author: Trelent
    """
    user = await repository_users.get_user(user_id, db, current_user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, description='No more than 15 requests per 2 minute',
            dependencies=[Depends(RateLimiter(times=15, seconds=120))], status_code=status.HTTP_201_CREATED)
async def create_user(body: UserModel, db: Session = Depends(get_db),
                      current_user: AuthUser = Depends(auth_service.get_current_user)):
    """
    The create_user function creates a new user in the database.
        It takes a UserModel object as input, and returns an HTTP response with the newly created user's information.
    
    
    :param body: UserModel: Specify the type of data that will be passed to the function
    :param db: Session: Pass the database session to the repository
    :param current_user: AuthUser: Get the current user from the database
    :return: A usermodel object
    :doc-author: Trelent
    """
    return await repository_users.create_user(body, db, current_user)


@router.put("/put/{user_id}", response_model=UserResponse, description='No more than 15 requests per 2 minute',
            dependencies=[Depends(RateLimiter(times=15, seconds=120))])
async def update_user(body: UserModel, user_id: int, db: Session = Depends(get_db),
                      current_user: AuthUser = Depends(auth_service.get_current_user)):
    """
    The update_user function updates a user in the database.
        It takes an id, and a body containing the fields to update.
        The function returns the updated user.
    
    :param body: UserModel: Specify the data that will be passed to the function
    :param user_id: int: Get the user id from the url
    :param db: Session: Get the database session
    :param current_user: AuthUser: Get the current user
    :return: A usermodel object
    :doc-author: Trelent
    """
    user = await repository_users.update_user(user_id, body, db, current_user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/remove/{user_id}", response_model=UserResponse, description='No more than 15 requests per 2 minute',
            dependencies=[Depends(RateLimiter(times=15, seconds=120))])
async def remove_user(user_id: int, db: Session = Depends(get_db),
                      current_user: AuthUser = Depends(auth_service.get_current_user)):
    """
    The remove_user function removes a user from the database.
    
    :param user_id: int: Specify the user id of the user to be deleted
    :param db: Session: Pass the database session to the function
    :param current_user: AuthUser: Get the user id of the logged in user
    :return: The removed user
    :doc-author: Trelent
    """
    user = await repository_users.remove_user(user_id, db, current_user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user