from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
from datetime import datetime

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    quiz_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
