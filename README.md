# subway-project
1. 코드 가져오기:

  git clone https://github.com/sangwon-jung-cell/subway-project.git

  # 충돌 방지
  git fetch origin # 원격 변경사항 확인
  git diff main origin/main # 차이점 비교
  git merge origin/main         # 내 로컬 경로의 파일과 main branch 내용 병합

  #  git pull을 하기 전에는 로컬에서 작업하던 내용을 commit 하거나 stash (임시 저장) 해두는 것이 좋습니다. 작업 중인 변경 사항이 남아있으면 git pull 명령어가 실행되지 않고 에러를 뱉을 수 있거든요.

  git pull origin main          # 로컬에서 수정한 게 없다면
  git pull --rebase origin main # 커밋이 만들어져있다면
  


2. 도커 빌드하기:

  # (본인경로)../subway-project
  docker-compose up --build # 맨 처음 이미지 생성

  다시 시작: docker-compose up (이미 빌드된 이미지를 사용해 바로 컨테이너 실행)
  완전히 끄기: docker-compose down (실행 중인 컨테이너를 멈추고 삭제. 이미지는 그대로 남음)



/app/ (여기가 파이썬이 실행되는 시작점)
├── main.py
├── api/
│   └── detection.py
└── model/
    └── best.pt




http://localhost:8000/static/index.html 경로로 열어서 테스트