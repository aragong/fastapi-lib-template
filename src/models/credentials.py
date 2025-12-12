from pydantic import BaseModel


class EmailCredentials(BaseModel):
    """User credentials for authentication."""

    email: str
    password: str
