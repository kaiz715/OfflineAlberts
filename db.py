from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    JSON,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import random
import config


Base = declarative_base()
engine = create_engine("sqlite:///albert.db")


class Question(Base):
    __tablename__ = "questions"

    question_title = Column("question_title", String, primary_key=True)
    answer_1_id = Column("answer_1_id", String)
    answer_2_id = Column("answer_2_id", String)
    answer_3_id = Column("answer_3_id", String)
    answer_4_id = Column("answer_4_id", String)
    correct_answer = Column("correct_answer", Integer)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
