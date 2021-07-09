from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_nm = Column("USER_NM", String(20), primary_key=True)
    std_amt = Column("STD_AMT", Integer)
    std_cnt = Column("STD_CNT", Integer)
    last_login_hms = Column("LAST_LOGIN_HMS", TIMESTAMP, nullable=True)
    last_out_hms = Column("LAST_OUT_HMS", TIMESTAMP, nullable=True)

    def __init__(self, user_nm):
        self.user_nm = user_nm
        self.std_amt = 0
        self.std_cnt = 0

    def __str__(self):
        return f"user_nm={self.user_nm}, std_amt={self.std_amt}, std_cnt={self.std_cnt}, " \
               f"last_login_hms={self.last_login_hms}, last_out_hms={self.last_out_hms}"
