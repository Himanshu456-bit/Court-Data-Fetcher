from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.database import Base
import datetime

class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    case_type = Column(String(100), index=True)
    case_number = Column(Integer)
    year = Column(Integer)
    query_timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    raw_responses = relationship("RawResponse", back_populates="query")
    judgments = relationship("Judgment", back_populates="query")


class RawResponse(Base):
    __tablename__ = "raw_responses"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("queries.id"))
    raw_html_or_json = Column(Text)
    response_timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    query = relationship("Query", back_populates="raw_responses")

class Judgment(Base):
    __tablename__ = "judgments"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("queries.id"))
    file_name = Column(String(255))
    file_path_or_url = Column(String(500))
    download_timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    query = relationship("Query", back_populates="judgments")
