from enums.db_enum import DbEnum

import utils.handle_time
from tables.user import User
from tables.study_log import StudyLog

from sqlalchemy.orm import sessionmaker as sqlalchemy_sessionmaker
from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy.exc import SQLAlchemyError


class DbHandler:
    def __init__(self, db_name):
        print(f"DbHandler init {db_name}")

        self.engine = sqlalchemy_create_engine(db_name)
        self.sessionMaker = sqlalchemy_sessionmaker(autocommit=False, bind=self.engine)
        self.create_tables()

    def create_tables(self):
        try:
            with self.sessionMaker() as currentSession:
                User.__table__.create(bind=self.engine, checkfirst=True)
                StudyLog.__table__.create(bind=self.engine, checkfirst=True)
                currentSession.commit()
                return DbEnum.CREATE_TABLE_SUCCESS
        except SQLAlchemyError as sqlError:
            print(sqlError)
            return DbEnum.CREATE_TABLE_FAILED

    def get_all_users(self):
        with self.sessionMaker() as currentSession:
            return currentSession.query(User).all()

    def get_my_study_logs(self, user_id):
        with self.sessionMaker() as currentSession:
            return currentSession.query(StudyLog).filter_by(user_id=user_id).all()

    def start_study(self, user, current_time):
        user_id = user.id
        user_name = user.name
        print(f"start study : {current_time}")

        try:
            with self.sessionMaker() as currentSession:
                user = currentSession.query(User).filter_by(id=user_id).first()

                if user is None:
                    user = User(user_id, user_name)
                    currentSession.add(user)

                user.last_start_time = current_time
                user.last_end_time = None

                # 가장 최근 스터디 기록
                recent_study_log = currentSession.query(StudyLog).filter_by(user_id=user_id) \
                    .order_by(StudyLog.id.desc()).first()

                # 로그가 없음 = 첫 스터디
                if recent_study_log is None:
                    currentSession.add(StudyLog(user_id, user_name, current_time))
                # recent_study_log.end_time is None -> 지난 스터디에서 !bye를 안 함
                elif recent_study_log.end_time is None:
                    recent_study_log.start_time = current_time
                else:
                    currentSession.add(StudyLog(user_id, user_name, current_time))

                currentSession.commit()
                return DbEnum.START_STUDY_SUCCESS

        except SQLAlchemyError as sqlError:
            print(sqlError)
            return DbEnum.START_STUDY_FAILED

    def end_study(self, user, current_time):
        user_id = user.id
        user_name = user.name
        print(f"end study : {current_time}")

        try:
            with self.sessionMaker() as currentSession:
                user = currentSession.query(User).filter_by(id=user_id).first()

                if user is None or user.last_end_time is not None:
                    return DbEnum.END_STUDY_NO_START

                elapsed_time = utils.handle_time. \
                    calculate_elapsed(user.last_start_time, current_time).total_seconds()

                user.study_amount += elapsed_time
                user.study_count += 1
                user.last_end_time = current_time

                recent_study_log = currentSession.query(StudyLog).filter_by(user_id=user_id) \
                    .order_by(StudyLog.id.desc()).first()
                recent_study_log.end_time = current_time

                currentSession.commit()
                return DbEnum.END_STUDY_SUCCESS

        except SQLAlchemyError as sqlError:
            print(sqlError)
            return DbEnum.END_STUDY_FAILED

    def delete_user(self, user_id):
        with self.sessionMaker() as currentSession:
            user = currentSession.query(User).filter_by(id=user_id).first()
            currentSession.delete(user)
            currentSession.commit()

    def __del__(self):
        print(f"DbHandler del")
        self.sessionMaker.close_all()
