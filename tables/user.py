from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, TIMESTAMP

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    study_amount = Column(Integer)
    study_count = Column(Integer)
    last_start_time = Column(TIMESTAMP, nullable=True)
    last_end_time = Column(TIMESTAMP, nullable=True)

    def __init__(self, user_id, user_name):
        self.id = user_id
        self.name = user_name
        self.study_amount = 0
        self.study_count = 0

    def __str__(self):
        return f"유저아이디: {self.id}, 유저명: {self.name}, 총 공부시간: {self.study_amount}, 총 공부횟수: {self.study_count}," \
               f" 마지막 로그인 시각: {self.last_start_time}, 마지막 로그아웃 시각: {self.last_end_time}"
