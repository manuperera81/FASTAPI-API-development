from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

"""
    It takes a user_credentials object, which is a UserLogin object, which is a Pydantic model, and a db
    object, which is a Session object, which is a SQLAlchemy object

    :param user_credentials: schemas.UserLogin
    :type user_credentials: schemas.UserLogin
    :param db: Session = Depends(database.get_db)
    :type db: Session
    :return: A dictionary with two keys: access_token and token_type.
    """

"""
    The `login` function takes user credentials, checks if they are valid, and returns an access token
    if they are.
    
    :param user_credentials: The `user_credentials` parameter is of type `OAuth2PasswordRequestForm`. It
    is used to retrieve the username and password entered by the user during the login process
    :type user_credentials: OAuth2PasswordRequestForm
    :param db: The `db` parameter is a dependency injection for the database session. It is used to
    interact with the database and perform queries
    :type db: Session
    :return: a dictionary with two keys: "access_token" and "token_type". The value of "access_token" is
    the access token generated using the user's credentials, and the value of "token_type" is "bearer".
    """


@router.post('/login', response_model=schemas.Token)
def login(user_credentials:  OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # username =
    # password =

    # The line `user = db.query(models.User).filter(models.User.email ==
    # user_credentials.username).first()` is querying the database to find a user with the email that
    # matches the username entered by the user during the login process.
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,  detail=f"Invalid Credentials")

    # create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
