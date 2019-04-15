import re
import queue

# 车辆类
class Car(object):
    def __init__(self, car_id, start_id, end_id, max_speed, plan_time, priority, preset):
        self.carId = car_id
        self.startId = start_id
        self.endId = end_id
        self.maxSpeed = max_speed
        self.planTime = plan_time
        self.priority = priority
        self.preset = preset
        # self.startTime = 0

    def get_planTime(self):
        return self.planTime

    def get_maxSpeed(self):
        return self.maxSpeed

    def get_Id(self):        
        return int(self.carId)



# 道路类
class Road(object):
    def __init__(self, road_id, road_length, max_speed, lane_mum, start_id, end_id, is_duplex):
        self.roadId = road_id
        self.roadLength = road_length
        self.maxSpeed = max_speed
        self.laneNum = lane_mum
        self.startId = start_id
        self.endId = end_id
        self.isDuplex = is_duplex



# 路口类
class Cross(object):
    def __init__(self, cross_id, up_id, right_id, down_id, left_id):
        self.crossId = cross_id
        self.upId = up_id
        self.rightId = right_id
        self.downId = down_id
        self.leftId = left_id
        self.roadidlist = [up_id, right_id, down_id, left_id]


def load_data(car_path, road_path, cross_path):
    with open(car_path, 'r') as car_read:
        data_car = list()
        for data in car_read:
            data = data.split(',')
            if data[0][0] == '#':
                continue
            data[0] = re.findall('\d+', data[0])[0]
            data[-1] = re.findall('\d+', data[-1])[0]
            for i in range(len(data)):
                data[i] = data[i].strip()
            data_car.append(Car(data[0], data[1], data[2], int(data[3]), int(data[4]), int(data[5]), int(data[6])))

    # 加载道路信息
    with open(road_path, 'r') as road_read:
        data_road = list()
        for data in road_read:
            data = data.split(',')
            if data[0][0] == '#':
                continue
            data[0] = re.findall('\d+', data[0])[0]
            data[-1] = re.findall('\d+', data[-1])[0]
            for i in range(len(data)):
                data[i] = data[i].strip()
            # print(data[0])
            data_road.append(Road(data[0], int(data[1]), int(data[2]), int(data[3]), data[4], data[5], data[6]))

    # 加载路口信息
    with open(cross_path, 'r') as cross_read:
        data_cross = list()
        for data in cross_read:
            data = data.split(',')
            if data[0][0] == '#':
                continue
            data[0] = re.findall('\d+', data[0])[0]
            data[-1] = re.findall('.?\d+', data[-1])[0]
            for i in range(len(data)):
                data[i] = data[i].strip()
            # for i in range(1,len(data)):
            #     if data[i] == '1':
            #         data[i] = '-' + data[i]
            data_cross.append(Cross(data[0], data[1], data[2], data[3], data[4]))

    return data_car, data_road, data_cross



def load_preset(preset_path):
    with open(preset_path, 'r') as preset_read:
        data_preset = dict()
        preset_time = dict()
        for data in preset_read:
            data2 = data.split(',')
            if data2[0][0] == '#':
                continue
            data2[0] = re.findall('\d+', data2[0])[0]
            data2[-1] = re.findall('\d+', data2[-1])[0]
            for i in range(len(data2)):
                data2[i] = data2[i].strip()
            carId = data2[0]
            startTime = data2[1]
            min_path = data2[2:]
            data_preset[carId] = min_path
            preset_time[carId] = int(startTime)
            # data_preset[carId] = data
            # startTime = data[1]
            # path = data[2:]
            # data_car[carId].startTime = startTime
            # data_car[carId].path = path
            # data_preset[carId] = data_car[carId]
            # data_car.pop(carId)

        return data_preset, preset_time

def save_data(answer_path, results):
    with open(answer_path, 'w') as answer_read:
        answer_read.write(results)
