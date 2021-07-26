import utils.handle_time
from table.user import User
from table.studyLog import StudyLog

from sqlalchemy.orm import sessionmaker as sqlalchemy_sessionmaker
from sqlalchemy import create_engine as sqlalchemy_create_engine


class DbHandler:
    def __init__(self, db_name):
        print(f"DbHandler init {db_name}")

        self.engine = sqlalchemy_create_engine(db_name)
        self.sessionMaker = sqlalchemy_sessionmaker(autocommit=False, bind=self.engine)
        self.create_tables()

    def create_tables(self):
        with self.sessionMaker() as currentSession:
            User.__table__.create(bind=self.engine, checkfirst=True)
            StudyLog.__table__.create(bind=self.engine, checkfirst=True)
            currentSession.commit()

    def get_all_users(self):
        with self.sessionMaker() as currentSession:
            return currentSession.query(User).all()

    def get_all_study_logs(self, user_name):
        with self.sessionMaker() as currentSession:
            return currentSession.query(StudyLog).filter_by(user_name=user_name).all()

    def start_study(self, user_name, current_time):
        print(f"start study : {current_time}")

        with self.sessionMaker() as currentSession:
            user = currentSession.query(User).filter_by(name=user_name).first()

            if user is None:
                user = User(user_name)
                currentSession.add(user)

            user.last_start_time = current_time
            user.last_end_time = None

            # 가장 최근 스터디 기록
            recent_study_log = currentSession.query(StudyLog).filter_by(user_name=user_name) \
                .order_by(StudyLog.id.desc()).first()

            # 로그가 없음 = 첫 스터디
            if recent_study_log is None:
                currentSession.add(StudyLog(user_name, current_time))
            # recent_study_log.end_time is None -> 지난 스터디에서 !bye를 안 함
            elif recent_study_log.end_time is None:
                recent_study_log.start_time = current_time
            else:
                currentSession.add(StudyLog(user_name, current_time))

            currentSession.commit()

    def end_study(self, user_name, current_time):
        print(f"end study : {current_time}")

        with self.sessionMaker() as currentSession:
            user = currentSession.query(User).filter_by(name=user_name).first()

            if user is None or user.last_end_time is not None:
                return f"{user_name}님은 최근에 공부를 시작하신 적이 없네요"

            elapsed_time = utils.handle_time. \
                calculate_elapsed(user.last_start_time, current_time).total_seconds()

            user.study_amount += elapsed_time
            user.study_count += 1
            user.last_end_time = current_time

            recent_study_log = currentSession.query(StudyLog).filter_by(user_name=user_name) \
                .order_by(StudyLog.id.desc()).first()
            recent_study_log.end_time = current_time

            currentSession.commit()

    def delete_user(self, user_name):
        with self.sessionMaker() as currentSession:
            user = currentSession.query(User).filter_by(name=user_name).first()
            currentSession.delete(user)
            currentSession.commit()

    def __del__(self):
        print(f"DbHandler del")
        self.sessionMaker.close_all()
