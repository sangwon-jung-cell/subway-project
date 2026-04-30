import json
import os

def convert_aihub_to_yolo(json_dir, output_dir):
    # 카테고리 매핑
    category_map = {
    "person": 0,
    "turnstile_trespassing": 1
    }
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            with open(os.path.join(json_dir, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 이미지 정보 추출
            img_w = data['metadata']['width']
            img_h = data['metadata']['height']
            
            # 각 프레임별로 txt 파일 생성 (YOLO는 이미지당 1개의 txt 필요)
            for frame in data.get('frames', []):
                frame_num = frame['number']
                image_name = frame['image']
                txt_filename = image_name.replace('.jpg', '.txt')
                
                yolo_lines = []
                for anno in frame.get('annotations', []):
                    code = anno['category']['code']
                    if code in category_map:
                        class_id = category_map[code]            
                        # 좌표 추출
                        x = anno['label']['x']
                        y = anno['label']['y']
                        w = anno['label']['width']
                        h = anno['label']['height']
                        
                        # YOLO 포맷으로 정규화
                        x_center = (x + w / 2) / img_w
                        y_center = (y + h / 2) / img_h
                        norm_w = w / img_w
                        norm_h = h / img_h
                        
                        yolo_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {norm_w:.6f} {norm_h:.6f}")
                
                # 파일 저장
                if yolo_lines:
                    with open(os.path.join(output_dir, txt_filename), 'w') as out_f:
                        out_f.write("\n".join(yolo_lines))

# 실행
json_path = './aihub_json_folder'  # JSON 파일들이 들어있는 폴더
output_path = './yolo_labels'      # 변환된 TXT를 저장할 폴더
convert_aihub_to_yolo(json_path, output_path)
print("변환 완료!")