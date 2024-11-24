
from sqlalchemy import Column, TEXT, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base

class Song(Base):
    __tablename__ = "songs"

    id = Column(TEXT, primary_key=True, index=True)
    title = Column(VARCHAR(100))
    artist = Column(TEXT)
    song_url = Column(TEXT)
    thumbnail_url = Column(TEXT)
    hex_code = Column(VARCHAR(6))
    user_id = Column(TEXT, ForeignKey("users.id"))
    # user = relationship("User", back_populates="songs")