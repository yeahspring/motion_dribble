1. pose_estimation.py : media_pipe Live Streaming을 켜기 위한 python 코드 입니다.
webcam을 이용해 사람을 detecting하고, pose estimation을 통해 좌표를 추출합니다.

2. wcrc_middle.py : pose_estimation으로 추출한 좌표 값을 전달 받아 이동 동선을 예측하고 그에 따른 로봇의 회피 경로를 생성해주는 알고리즘이 작성되어 있는 코드입니다.

3. /my_mobile/src/my_robot_description/src/teleop_twist_keyboard.py : 회피 경로 생성 알고리즘을 바탕으로 정해진 state value를 전달 받아 gazebo의 로봇을 주행시키는 코드입니다.

4. average_hip_x.txt 와 order.txt : 각각 추출된 좌표값을 저장하는 txt, 회피 경로 state value를 저장하는 txt 입니다.

5. 그 외 my_mobile 폴더 내의 코드들은 gazebo를 실행하기 위한 ROS2 Package 입니다.
