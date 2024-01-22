from jose import JWTError, jwt
from datetime import datetime, timedelta,timezone
from .import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


# SECRET_KEY
# Algorthm
# Experation_time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    """
    It takes a dictionary of data, adds an expiry date to it, and then encodes it using the JWT library
    :return: A JWT token
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encodeed_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encodeed_jwt


def verify_access_token(token: str, credentials_exception):
    """
    The function `verify_access_token` verifies the access token by decoding it using a secret key and
    algorithm, and returns the user ID extracted from the token.

    :param token: The `token` parameter is a string that represents the access token that needs to be
    verified
    :type token: str
    :param credentials_exception: The `credentials_exception` parameter is an exception that is raised
    when the access token is not valid or does not contain the required information. It is used to
    handle authentication errors and provide a meaningful error message to the user
    :return: the token_data, which is an instance of the TokenData class from the schemas module.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    The function `get_current_user` retrieves the current user based on the provided access token and
    database session.

    :param token: The `token` parameter is a string that represents the access token provided by the
    client. It is used to authenticate and authorize the user making the request
    :type token: str
    :param db: The `db` parameter is of type `Session` and is used to access the database session. It is
    obtained by calling the `get_db` function from the `database` module
    :type db: Session
    :return: the user object.
    """
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
