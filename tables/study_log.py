from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from tables.user import User

Base = declarative_base()


class StudyLog(Base):
    __tablename__ = "studyLog"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP, nullable=True)

    def __init__(self, user_id, start_time):
        self.user_id = user_id
        self.start_time = start_time

    def __str__(self):
        return f"id: {self.id}, 아이디: {self.user_id}," \
               f"시작 시각: {self.start_time}, 종료 시각: {self.end_time}"
