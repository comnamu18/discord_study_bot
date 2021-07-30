from enum import Enum, auto


class DbEnum(Enum):
    CREATE_TABLE_SUCCESS = auto()
    CREATE_TABLE_FAILED = auto()

    """
    GET_ALL_USERS_SUCCESS = auto()
    GET_ALL_USERS_FAILED = auto()

    GET_MY_STUDY_LOGS_SUCCESS = auto()
    GET_MY_STUDY_LOGS_FAILED = auto()
    
    이것들은 일단 작성은 했는데 리턴형이 있는 것들이라 적용하진 않음.
    """

    START_STUDY_SUCCESS = auto()
    START_STUDY_FAILED = auto()

    END_STUDY_SUCCESS = auto()
    END_STUDY_NO_START = auto()
    END_STUDY_FAILED = auto()
