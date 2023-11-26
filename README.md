# motion_dribble for W.C.R.C
= 움직임 예측 회피 주행 알고리즘

<목차>
１. 개발 동기
２. 개발 내용
  ⅰ. Flow Chart
  ⅱ. Motion Estimation Part
  ⅲ. Evasion Logic Part
  ⅳ. Simulation Drive Part
3. 참고 사항

## 1. 개발 동기

기존의 주행 로봇 및 모바일 로봇은 Local Path Planning 중에 마주치
는 이동 장애물, 특히 사람과의 접촉을 피하기 위해 약간의 회피 동작이
나 속도 조절, 때로는 정지를 택하는 경향이 있다. 이로 인해 주행의 흐
름이 끊기며, 비선형적이고 부드럽지 못한 서비스가 제공되는 문제가 발
생한다.
이러한 한계를 극복하고자, 본 프로젝트는 선형적이며 원활한 주행을
중점으로 한 새로운 기술을 개발하였다. 이를 통해 접촉 회피와 경로 계
획의 효율을 높이고, 주행 중 불필요한 중단 없이 사용자에게 더 높은
수준의 서비스를 제공할 수 있도록 하였다.
새로운 주행 알고리즘은 비선형적인 행동 패턴이 아닌, 선형적이며 유
연한 동작을 강조하며, 최적의 경로 선택과 동시에 최소한의 인터럽션으
로 주행을 진행한다. 이를 통해 기존의 불편한 서비스 경험을 극복하고,
고객에게 높은 수준의 안정성과 부드러운 주행을 제공하는 것을 목표로
한다.

## 2. 개발 내용

로봇에 탑재된 카메라에 인식되는 사람의 골반 좌표를 인식하고, 방향을
예측하여 부딪히지 않도록 경로를 수정해 회피 주행

## ⅰ. Flow Chart

![image (1)](https://github.com/john4299/Ros_Delivery_Service/assets/140477578/1f6dfa19-a4db-49d6-9e5e-dfe6f156c9ed)

## ⅱ. Motion Estimation Part

웹캠을 통한 화면 촬영에서 인식된 사람의 자세를 추출하기 위해
MediaPipe Pose Estimation을 활용하고 있다. 특히, 특정 프레임에서
추출된 좌표 값을 기반으로 사람의 보행 방향을 정확하게 예측하는 고도
의 알고리즘을 개발하였다.
이 시스템은 먼저 웹캠으로부터 수집된 영상에서 MediaPipe Pose
Estimation을 활용하여 다양한 신체 부위의 좌표를 정확하게 추출한다.
이를 통해 높은 정밀도의 자세 정보를 획득하고, 특히 발, 무릎, 엉덩이,
어깨 등과 같은 핵심 부위의 움직임을 감지한다.
다음으로, 특정 프레임에서 추출된 좌표 값을 이용하여 사람의 보행 방
향을 예측하는 알고리즘을 적용한다. 이 과정에서는 과거의 프레임과 현
재 프레임 간의 좌표 변화를 분석하고, 이동 패턴을 식별하여 보행 방향
을 동적으로 예측한다.

![image (2)](https://github.com/john4299/Ros_Delivery_Service/assets/140477578/a4b93f24-0a98-4ea3-a9b9-bbe41803cc13)
골반의 포인트(왼쪽 엉덩이, 오른쪽 엉덩이)를 감지하고 양쪽 포인트의
중앙값을 추출하여 .txt파일에 실시간으로 저장한다.

## ⅲ. Evasion Logic Part

주행하고 있는 로봇의 시야 범위 내에 Motion Estimation Part에서
저장된 사람 허벅지의 중앙값을 읽을 때 첫 번째(First Check) 체크를
하고 한 발자국 단위로 좌, 우로 움직이는 부분을 두 번째(Second
Check)체크를 한다. 이렇게 함으로써 사람이 마주했을 때 다음 행동 방
향이 어디로 향할지 예측할 수 있다. 예측 방향과 위치가 로봇의 주행
경로와 겹칠 경우 로봇은 사람의 보행 방향 반대로 회피하여 주행 후 다
시 기존 주행 경로로 복귀 한다. 만약 예측 정보가 로봇 주행 경로에 영
향을 미치지 않는다면 로봇은 대상을 무시하고 기존 경로대로 주행한다.
![image (3)](https://github.com/john4299/Ros_Delivery_Service/assets/140477578/e3f7e6c2-9b7b-4189-a484-3ecbb823a2f9)

## ⅳ. Simulation Drive Part

주행하고 있는 상태를 보고 사람이 존재하면 해당 로직이 실현되는 상
태를 확인하기 위하여 ROS에서 Gazebo를 제작하여 가상 시뮬레이션을
실행했다. 실제 차량을 가정하여 사람이 앞을 막아서고 가려는 방향으로
모션을 취했을 때 제작한 모빌리티가 피하면서 주행함을 확인할 수 있
다.

![image (4)](https://github.com/john4299/Ros_Delivery_Service/assets/140477578/1afd043b-03d3-4dca-85d0-c958c35160c2)
 위의 그림은 Evasion Logic Part에
서 읽어온 좌우 상태값으로 가재보
모빌리티가 사람을 상대로 왼쪽으로
갈지 오른쪽으로 갈지 ROS패키지 안
에서 알고리즘 구현을 나타낸 코드이
다.
아래 그림은 웹캠 카메라로 지나가
는 사람을 확인한 후 좌표값을 실시
간으로 보내면서 그에 맞는 상황을
시뮬레이션하는 전체 구상을 나타내
었다.
![image (5)](https://github.com/john4299/Ros_Delivery_Service/assets/140477578/7ea2a492-52ab-4b28-b598-bc909c0f25e0)

## 3. 참고사항

가. MediaPipePoseEstimation [nicknochnack]
(https://github.com/nicknochnack/MediaPipePoseEstimation)

나. PoseNet keypoint로 skeleton 그리기 [Leeys]
(https://machineindeep.tistory.com/28)

다. ultralytics
(https://github.com/ultralytics/ultralytics)

라. mediapipe pose classification model - webcam streaming
environment [주홍색 코딩]
(https://kwonkai.tistory.com/129)

인원(최수혁,김종빈,조예봄,이종호)
