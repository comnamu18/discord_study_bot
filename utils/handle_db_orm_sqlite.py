from utils.handle_time_orm import calculate_elapsed_object

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utils.User import User



class DB_Handler:
    def __init__(self, db_name):
        self.engine = create_engine(f"sqlite:///{db_name}", echo=True)
        self.session = sessionmaker(bind=self.engine)()

    def create_user_table(self):
        User.__table__.create(bind=self.engine, checkfirst=True)

    def get_all_users(self):
        return self.session.query(User).all()

    def get_user_object_by_user_name(self, user_name):
        return self.session.query(User).filter_by(user_nm=user_name).first()

    def start_study(self, user_name, current_time):
        print(f"start study : {current_time}")

        user = self.get_user_object_by_user_name(user_name)
        user.last_login_hms = current_time
        user.last_out_hms = None

        self.session.commit()

    def end_study(self, user_name, current_time):
        print(f"end study : {current_time}")

        user = self.get_user_object_by_user_name(user_name)
        elapsed_time = calculate_elapsed_object(user.last_login_hms, current_time).total_seconds()

        user.std_amt += elapsed_time
        user.std_cnt += 1
        user.last_login_hms = None
        user.last_out_hms = current_time

        self.session.commit()


    def delete_user(self, user_name):
        user = self.get_user_object_by_user_name(user_name)
        self.session.delete(user)
        self.session.commit()
