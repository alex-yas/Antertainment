from sqlalchemy import Column, Integer, String

from .base import Base


class Ant(Base):
    id = Column(Integer,primary_key = True, index=True)
    name = Column(String,nullable= False)
    description = Column(String,nullable=False)
