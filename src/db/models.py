from sqlalchemy import Column, DateTime, Integer, String, Interval
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from .database import engine

Base = declarative_base()

class Down(Base):
    __tablename__ = "downs"

    id = Column(Integer, primary_key=True)
    operation = Column(String, default=None)
    url = Column(String, default=None)
    start = Column(DateTime(timezone=True), server_default=func.now())
    end = Column(DateTime(timezone=True), nullable=True, default=None)
    delta = Column(Interval(), nullable=True, default=None)

    def __repr__(self):
        return f"<Down {self.operation} - {self.url}>"

Base.metadata.create_all(engine)
