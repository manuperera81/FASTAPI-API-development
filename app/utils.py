from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    """
    It hashes the password.

    :param password: The password to hash
    :type password: str
    :return: The hash of the password.
    """
    return pwd_context.hash(password)


def verify(plane_pw, hashed_pw):
    return pwd_context.verify(plane_pw, hashed_pw)
