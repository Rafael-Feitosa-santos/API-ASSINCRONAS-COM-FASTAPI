from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published_at: Optional[datetime] = None
