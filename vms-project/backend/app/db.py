# backend/app/db.py
from sqlalchemy import create_engine, Column, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
import uuid

DATABASE_URL = "sqlite:///./vms.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def new_id():
    return str(uuid.uuid4())

class Result(Base):
    __tablename__ = "results"
    id = Column(String, primary_key=True, index=True)
    stream_id = Column(String)
    model = Column(String)
    output = Column(JSON)

    def dict(self):
        return {"id": self.id, "stream_id": self.stream_id, "model": self.model, "output": self.output}

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(String, primary_key=True, index=True)
    stream_id = Column(String)
    level = Column(String)
    message = Column(String)
    data = Column(JSON)

Base.metadata.create_all(bind=engine)
