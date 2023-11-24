import math
import cv2
import numpy as np
from time import time
import mediapipe as mp
import matplotlib.pyplot as plt
from mediapipe.framework.formats import landmark_pb2
from mediapipe import solutions
import time

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# Initializing mediapipe pose class.
# mediapipe pose class를 초기화 한다.
mp_pose = mp.solutions.pose
 
# Setting up the Pose function.
# pose detect function에 image detect=True, 최소감지신뢰도 = 0.3, 모델 복잡도 =2를 준다.
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)
 
# Initializing mediapipe drawing class, useful for annotation.
# mediapipe의 drawing class를 초기화한다.
mp_drawing = mp.solutions.drawing_utils



def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

  # Loop through the detected poses to visualize.
    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

    # Draw the pose landmarks.
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style())
    return annotated_image

def print_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    print('pose landmarker result: {}'.format(result))

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='yolov8n-pose.pt'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

cap = cv2.VideoCapture(2)
with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("카메라를 찾을 수 없습니다.")
            # 동영상을 불러올 경우는 'continue' 대신 'break'를 사용합니다.
            continue

        # 필요에 따라 성능 향상을 위해 이미지 작성을 불가능함으로 기본 설정합니다.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # 포즈 주석을 이미지 위에 그립니다.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        
        results = pose.process(image)
 
        # 포즈 랜드마크가 있는지 확인합니다.
        left_hip_x_values = []
        right_hip_x_values = []

        # 포즈가 존재하면
        if results.pose_landmarks:
            image_height, image_width, _ = image.shape

            for i in range(23, 25):
                landmark_name = mp_pose.PoseLandmark(i).name
                landmark_x = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].x * image_width)
                landmark_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].y * image_height)
                
                
                if landmark_name == 'LEFT_HIP':
                    left_hip_x_values.append(landmark_x)
                elif landmark_name == 'RIGHT_HIP':
                    right_hip_x_values.append(landmark_x)

            # 힙 랜드마크가 하나 이상 발견되었는지 확인합니다.
            if left_hip_x_values or right_hip_x_values:
                # 적어도 하나의 힙 랜드마크가 발견되면 평균 x 값을 계산합니다.
                all_hip_x_values = left_hip_x_values + right_hip_x_values
                average_hip_x = sum(all_hip_x_values) / len(all_hip_x_values)
            else:
                # 힙 랜드마크가 없으면 average_hip_x를 0으로 설정합니다.
                average_hip_x = 0.0

            print(average_hip_x)
            # 출력 및 파일 저장
            with open('average_hip_x.txt', 'w') as file:
                file.write(str(average_hip_x))
        # 포즈가 존재하지 않으면
        else:
            with open('average_hip_x.txt', 'w') as file:
                file.write(str(0.0))           
                       
            # 출력
            # print(f'LEFT_HIP x values: {left_hip_x_values}')
            # print(f'RIGHT_HIP x values: {right_hip_x_values}')
            # print(f'AVERAGE ALL_HIP x: {average_hip_x}')

                
            # # 파일에서 읽어서 출력
            # with open('average_hip_x.txt', 'r') as file:
            #     read_average_hip_x = file.read()

            # # 평균값 출력
            # print(f'Read Average HIP x: {read_average_hip_x}')
                
            # Display the found normalized landmarks.
                # print(f'{mp_pose.PoseLandmark(i).name}:\n{results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value]}')
          

        cv2.imshow('Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()