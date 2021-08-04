# discord_study_bot

Discord 랜선 각자 모여 코딩용 bot

## Bot 실행법

1. `.env.example`을 참고해서 `.env` 파일 생성 또는 환경 변수 추가
2. Docker 이미지 빌드 후 컨테이너 실행

## POETRY 사용 방법

``` sh
# 현재 프로젝트의 의존성 설치
poetry install
# 패키지 업데이트
poetry update
# 개발환경에서 필요한 패키지 설치 방식
poetry add "django=3.0.0"
# 개발환경 패키지 삭제
poetry remove pytest
# 설치된 모든 패키지를 보여준다.
poetry show
# 소스를 배포가능한 형태(tarball, wheel)로 빌드한다.
poetry build
# poetry로 가상환경(virtualenv)을 관리하는 방법
poetry env use {파이썬경로 or python3}
```

## Reference

[Python으로 Discord Bot 만들기 Tutorial](https://realpython.com/how-to-make-a-discord-bot-python/)

[Python 기반 Discord Bot](https://github.com/team-play-together/together-bot)

[Poetry 사용법](https://velog.io/@hj8853/Poetry%EB%A5%BC-%EC%82%AC%EC%9A%A9%ED%95%98%EC%97%AC-%EA%B0%80%EC%83%81%ED%99%98%EA%B2%BD-%EB%A7%8C%EB%93%A4%EA%B8%B0)
