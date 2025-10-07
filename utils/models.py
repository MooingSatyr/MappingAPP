from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class VRLI(Base):
    __tablename__ = 'VRLI'
    time = Column(Float)
    range_ = Column(Float)
    azimuth = Column(Float)
    elevation = Column(Float)
    filename = Column(String)
    file_size_mb = Column(Float)
    label = Column(Integer)
    velocity = Column(Float)
    data_id = Column(Integer, primary_key=True)

# Подключение к БД
engine = create_engine('sqlite:///VRLI.db', echo=False)
SessionLocal = sessionmaker(bind=engine)
