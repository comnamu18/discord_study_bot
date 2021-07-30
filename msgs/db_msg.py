from enums.db_enum import DbEnum

db_msgs = {
    DbEnum.CREATE_TABLE_SUCCESS: "테이블 생성 성공",
    DbEnum.CREATE_TABLE_FAILED: "테이블 생성 실패",

    DbEnum.START_STUDY_SUCCESS: "{time} : 안녕하세요 {name}님!",
    DbEnum.START_STUDY_FAILED: "공부 시작 실패",

    DbEnum.END_STUDY_SUCCESS: "{time} : 안녕히가세요 {name}님!",
    DbEnum.END_STUDY_NO_START: "{name}님은 최근에 공부를 시작하신 적이 없으시네요",
    DbEnum.END_STUDY_FAILED: "공부 시작 실패"
}
