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
  

2. 데이터 준비:

  # 폴더 등을 직접 만들고 본인이 가진 사진 넣기
  # 이미지 이름과 txt파일 이름이 동일해야 YOLO 학습 가능
  예를들어: subway-project/AI/yolo_dataset/images/train/img1.jpg
          subway-project/AI/yolo_dataset/labels/train/img1.jpg


3. 도커 빌드하기:

  # (본인경로)../subway-project
  docker-compose up --build # 맨 처음 이미지 생성
  docker exec -it subway_ai Nvidia-smi # GPU 잘 잡히는지 확인

  다시 시작: docker-compose up (이미 빌드된 이미지를 사용해 바로 컨테이너 실행)
  완전히 끄기: docker-compose down (실행 중인 컨테이너를 멈추고 삭제. 이미지는 그대로 남음)


4. 컨테이너 내부 접속

  # 컨테이너가 실행 중일 때
  docker exec -it subway_ai /bin/bash


# 파일 구조가 이렇게 되어있어야 됨

subway-project/
└── AI/
|    ├── Dockerfile_ai
|    ├── data.yaml
|    ├── train.py
|    └── yolo_dataset/   <-- data.yaml의 path가 가리키는 곳
|        ├── images/
|        │   ├── train/
|        │   ├── val/
|        │   └── test/
|        └── labels/     <-- 이미지와 같은 구조의 라벨 폴더가 필요함
|            ├── train/
|            ├── val/
|            └── test/
|
└── backend/
|         ├── database.py
|         ├── requirements.txt
|         ├── static # 무단침입 발생시 캡쳐한 이미지 저장 겨로
|         ├── main.py
|         ├── Dockerfile_backend
|         └── __pycache__
|
|
└── frontend/
          ├── .html
          ├── .css
          ├── .js


## 🚀 학습 방법 (Training)
# yolo_dataset 상위 폴더(보통 /usr/src/app)에서 실행(batch size, epochs, imgsz 수정 가능)

yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=100 imgsz=640 batch=16