from typing import List
from datetime import datetime, timedelta
from sqlalchemy import and_

from sqlalchemy.orm import Session

from src.database.models import User, AuthUser
from src.schemas import UserModel


async def get_users(skip: int, limit: int, db: Session, user: AuthUser) -> List[User]:
    """
    The get_users function returns a list of users.
    
    :param skip: int: Skip a certain number of users in the database
    :param limit: int: Limit the number of users returned
    :param db: Session: Pass the database session to the function
    :param user: AuthUser: Get the user's id from the database
    :return: A list of users
    :doc-author: Trelent
    """
    return db.query(User).filter(User.authuser_id == user.id).offset(skip).limit(limit).all()


async def get_user(user_id: int, db: Session, user: AuthUser) -> User:
    """
    The get_user function takes in a user_id and returns the User object with that id.
    It also checks to make sure that the user is authorized to access this information.
    
    :param user_id: int: Specify the user id of the user we want to get
    :param db: Session: Pass the database session to the function
    :param user: AuthUser: Check if the user is logged in
    :return: A user object
    :doc-author: Trelent
    """
    return db.query(User).filter(and_(User.id == user_id, User.authuser_id == user.id)).first()


async def create_user(body: UserModel, db: Session, user: AuthUser) -> User:
    """
    The create_user function creates a new user in the database.
    
    :param body: UserModel: Get the data from the request body
    :param db: Session: Connect to the database
    :param user: AuthUser: Get the user id from the authuser object
    :return: The user object
    :doc-author: Trelent
    """
    user = User(first_name=body.first_name, 
    second_name=body.second_name, 
    email=body.email, 
    phone=body.phone, 
    birthaday=body.birthaday, 
    description=body.description,
    authuser_id=user.id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def update_user(user_id: int, body: UserModel, db: Session, user: AuthUser) -> User| None:
    """
    The update_user function updates a user in the database.
        Args:
            user_id (int): The id of the user to update.
            body (UserModel): The updated User object to store in the database.
    
    :param user_id: int: Get the user with that id
    :param body: UserModel: Pass the user model to the function
    :param db: Session: Access the database
    :param user: AuthUser: Get the user id from the token
    :return: The updated user
    :doc-author: Trelent
    """
    usr= db.query(User).filter(and_(User.id == user_id, User.authuser_id == user.id)).first()
    if usr:
        usr.first_name = body.first_name
        usr.second_name = body.second_name
        usr.email = body.email
        usr.phone = body.phone
        usr.birthaday = body.birthaday
        usr.description = body.description
        usr.authuser_id = user.id
        db.commit()
    return usr


async def remove_user(user_id: int, db: Session, user: AuthUser)  -> User | None:
    """
    The remove_user function removes a user from the database.
        Args:
            user_id (int): The id of the user to be removed.
            db (Session): A session object for interacting with the database. 
    
    :param user_id: int: Specify the user id of the user to be deleted
    :param db: Session: Pass the database session to the function
    :param user: AuthUser: Check if the user is authorized to delete a user
    :return: The user that was deleted or none if the user didn't exist
    :doc-author: Trelent
    """
    user = db.query(User).filter(and_(User.id == user_id, User.authuser_id == user.id)).first()
    if user:
        db.delete(user)
        db.commit()
    return user


async def get_users_by_some_info(some_info: str, db: Session, user: AuthUser) -> List[User]:
    """
    The get_users_by_some_info function takes a string and returns a list of users that have the string in their first name, second name or email.
        Args:
            some_info (str): The string to search for.
            db (Session): A database session object.
            user (AuthUser): An authenticated user object.
    
    :param some_info: str: Pass the information that we want to search for
    :param db: Session: Create a connection to the database
    :param user: AuthUser: Get the user id from the database
    :return: A list of users with the specified information
    :doc-author: Trelent
    """
    response = []
    users = db.query(User).filter(User.authuser_id == user.id).all()
    for usr in users:
        if some_info.lower() in usr.first_name.lower() and usr not in response:
            response.append(usr)
        if some_info.lower() in usr.second_name.lower() and usr not in response:
            response.append(usr)
        if some_info.lower() in usr.email.lower() and usr not in response:
            response.append(usr)
            
    return response


async def get_birthday_per_week(days: int, db: Session, user: AuthUser) -> User:
    """
    The get_birthday_per_week function returns a list of users whose birthday is within the next 7 days.
        Args:
            days (int): The number of days to look ahead for birthdays.
            db (Session): A database session object that can be used to query the database.
    
    :param days: int: Specify the number of days in which we want to get the birthdays
    :param db: Session: Access the database
    :param user: AuthUser: Get the user id of the current logged in user
    :return: A list of users whose birthdays are in the next 7 days
    :doc-author: Trelent
    """
    response = []
    all_users = db.query(User).filter(User.authuser_id == user.id).all()
    if all_users:
        for usr in all_users:
            if timedelta(0) <= ((usr.birthaday.replace(year=int((datetime.now()).year))) - datetime.now().date()) <= timedelta(days):
                response.append(usr)

    return response

