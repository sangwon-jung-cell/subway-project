# subway-project
1. 코드 가져오기:

  git clone https://github.com/sangwon-jung-cell/subway-project.git
  cd subway-project

2. 데이터 준비:

  yolo_dataset/images/train 폴더 등을 직접 만들고 본인이 가진 사진 넣기
  aihub_json_folder/ 폴더 만들고 JSON 파일 넣기

3. 도커 빌드 및 변환:

  docker build -t subway-yolo .
  변환 스크립트 실행해서 .txt 파일들 생성 확인

도커 컨테이너 실행 명령어(gpu 사용)
  docker run -it --gpus all -v ${PWD}:/usr/src/app subway-yolo
  
  nvidia-smi (이 명령어 쳐보고 gpu 모델명과 메모리 정표가 표로 뜬다면 성공)
