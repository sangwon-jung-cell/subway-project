import json
import os
import shutil
import glob

# --- 설정 구간 ---
CLASS_MAP = {
    "person": 0, "child": 0, "wheelchair": 0, 
    "merchant": 0, "stroller": 0,
    "turnstile_trespassing": 1
}

def convert_aihub_to_yolo(json_folder, raw_img_root, output_img_dir, output_lbl_dir):
    # 출력 폴더 생성
    os.makedirs(output_img_dir, exist_ok=True)
    os.makedirs(output_lbl_dir, exist_ok=True)

    # 1. 폴더 내의 모든 .json 파일 목록 가져오기
    json_files = glob.glob(os.path.join(json_folder, "*.json"))
    
    if not json_files:
        print(f"JSON 파일을 찾을 수 없습니다: {json_folder}")
        return

    for json_path in json_files:
        print(f"처리 중: {os.path.basename(json_path)}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        video_id = str(data['id'])
        img_w = data['metadata']['width']
        img_h = data['metadata']['height']
        
        for frame in data['frames']:
            original_img_name = frame['image']
            new_base_name = f"{video_id}_{os.path.splitext(original_img_name)[0]}"
            
            # 이미지 경로 설정 (raw_data/images/train/2248321/frame_xxxx.jpg)
            src_img_path = os.path.join(raw_img_root, video_id, original_img_name)
            dst_img_path = os.path.join(output_img_dir, f"{new_base_name}.jpg")
            
            # 이미지 복사
            if os.path.exists(src_img_path):
                shutil.copy(src_img_path, dst_img_path)
            else:
                # 가끔 경로 구조가 다를 수 있으니 체크
                continue

            # 라벨 TXT 생성
            with open(os.path.join(output_lbl_dir, f"{new_base_name}.txt"), 'w') as lf:
                for anno in frame['annotations']:
                    category_code = anno['category']['code']
                    if category_code in CLASS_MAP:
                        cls_id = CLASS_MAP[category_code]
                        box = anno['label']
                        
                        # YOLO 정규화 계산
                        x_center = (box['x'] + box['width'] / 2.0) / img_w
                        y_center = (box['y'] + box['height'] / 2.0) / img_h
                        w = box['width'] / img_w
                        h = box['height'] / img_h
                        
                        lf.write(f"{cls_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")

# --- 실행부 ---
# 사용자가 말씀하신 경로 그대로 지정했습니다.
convert_aihub_to_yolo(
    json_folder='raw_data/labels/train', 
    raw_img_root='raw_data/images/train', 
    output_img_dir='yolo_dataset/images/train', 
    output_lbl_dir='yolo_dataset/labels/train'
)

print("✅ 모든 변환이 완료되었습니다!")