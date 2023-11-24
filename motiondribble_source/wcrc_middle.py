import os
import time

first = 0
second = 0
timer = 0
toggle = 0
state = 0

# Define file paths as variables
base_path = '/home/secret/wcrc/'
coordinates = os.path.join(base_path, 'average_hip_x.txt')
order = os.path.join(base_path, 'order.txt')

while True:
    time.sleep(1)
    with open(coordinates, 'r') as c:
        center_line = c.read()
        center_line = center_line.replace("\n","")
        try:
            center_line = float(center_line)
        except:
            center_line = 0

        # 예상경로 내에 장애물이 잡히지 않을 때
        if center_line == 0:
            print('nothing there')
            first = 0
            second = 0

        # 예상경로 내에 장애물이 잡히기 시작
        elif center_line != 0:
            print('something existed!')

            # coordinates 측정
            if (first == 0) or (second == 0):
                with open(coordinates, 'r') as c:
                    center_line = c.read()
                    center_line = center_line.replace("\n","")
                    try:
                        center_line = float(center_line)
                    except:
                        center_line = 0  
                first = center_line
                # print('FIRST checked !')

                time.sleep(1)
                with open(coordinates, 'r') as c:
                    center_line = c.read()
                    center_line = center_line.replace("\n","")
                    try:
                        center_line = float(center_line)
                    except:
                        center_line = 0
                second = center_line
                # print('SECOND checked !')
                   
                #if first == 0 and first == 0

            else:
                if (320 < first < 420):
                    print('something coming from rightside !')
                    # coordinates 결과2
                    if 0 < (first - second) < 10:
                        print('오른쪽 장애물이 피하고 있습니다.')
                        with open(order, 'w') as o:
                            o.write('0')   # 0: 직진ㄱ
                    elif -10 < (first - second) <= 0:
                        print('오른쪽의 장애물이 왼쪽으로 피하고 있습니다. 한번 더 확인합니다')
                        center_line = 0
                    else:
                        print('장애물이 (오른쪽으로) 직진하고 있습니다. 살짝 오른쪽으로 비켜갑니다')
                        with open(order, 'w') as o:
                            o.write('2')   # 1: 왼쪽으로 피하셈
                elif (220 < first < 320):
                    print('something coming from leftside !')
                    if 0 < (first - second) < 10:
                        print('왼쪽의 장애물이 피하고 있습니다.')
                        with open(order, 'w') as o:
                            o.write('0')   # 0: 직진ㄱ
                    elif -10 < (first - second) <= 0:
                        print('왼쪽의 장애물이 오른쪽으로 피하고 있습니다. 한번 더 확인합니다')
                        center_line = 0
                    else:
                        print('장애물이 (왼쪽으로) 직진하고 있습니다. 살짝 왼쪽으로 비켜갑니다')
                        with open(order, 'w') as o:
                            o.write('1')   # 2: 오른쪽으로 피하셈