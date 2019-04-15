from shortest_path import *


class Manage(object):
	def __init__(self, data_car, data_road, data_cross, data_preset, preset_time):
		self.data_car = data_car
		self.data_road = data_road
		self.data_cross = data_cross
		self.data_preset = data_preset
		self.presetNum = len(data_preset)

		self.use_roadNum = dict()
		self.crossId2roadId = dict()
		self.crossIds = ''
		self.route = dict()  # 开始结束路口到最小路径映射
		self.flag = 0
		self.flag2 = 0
		self.flag3 = 0
		self.path, self.id2index = floyd(self.data_road, self.data_cross, self.crossIds, self.flag, self.flag3)

		self.road_dic = dict()
		for road in self.data_road:
			start2end = road.startId + '_' + road.endId
			self.crossId2roadId[start2end] = road
			self.road_dic[road.roadId] = start2end
			if road.isDuplex == '1':
				cross_ids = road.endId + '_' + road.startId
				self.crossId2roadId[cross_ids] = road
			if road.laneNum > 4:
				self.flag3 = 1
				# self.road_dic[road.roadId] = cross_ids


		# 车辆按速度排序
		sort_carByv = list()
		car_dictionary = dict()

		for car in self.data_car:			
			if car.preset == 1:
				car.planTime = preset_time[car.carId]
			if car.startId in car_dictionary.keys():
				car_dictionary[car.startId].append(car)
			else:
				car_dictionary[car.startId] = [car]

		key_car = list(car_dictionary.keys())
		max_length = 0
		for key in key_car:
			car_dictionary[key].sort(key=lambda x:(-x.priority, x.planTime, -x.maxSpeed))
			car_num = len(car_dictionary[key])
			if car_num > max_length:
				max_length = car_num

		for i in range(max_length):
			for key in key_car:
				if len(car_dictionary[key]) > i:
					sort_carByv.append(car_dictionary[key][i])
		self.data_car = sort_carByv


	def running(self):
		results = ''
		num = 0
		if self.flag3 == 1:
			block_road = 5000
			everyTime = 27
			preset_num = 0
		else:
			block_road = 5000
			everyTime = 12
			preset_num = 0

		long = (len(self.data_car) - num) // everyTime
		for i in range(long):
			if i + 1 == long:
				movingCars = self.data_car[everyTime * i + num:]
			else:
				movingCars = self.data_car[everyTime * i + num: everyTime * (i + 1) + num]
			for car in movingCars:
				
				if car.maxSpeed < 8 and self.flag == 0:
					self.flag = 1
				cross_idStart = car.startId
				cross_idEnd = car.endId
				if car.preset == 1:
					preset_num += 1
					if preset_num >= self.presetNum // 10:
						min_road = self.data_preset[car.carId]
						min_path = list()
						last = ''
						for road in min_road:
							s2e = self.road_dic[road]
							data = s2e.split('_')
							# last = ''
							if data[0] == car.startId:
								min_path.append(data[0])
								min_path.append(data[1])
								last = data[1]
							elif data[1] == car.startId:
								min_path.append(data[1])
								min_path.append(data[0])
								last = data[0]
							elif last == data[0]:
								min_path.append(data[1])
								last = data[1]
							else:
								min_path.append(data[0])
								last = data[0]
					else:
						min_path = shortest_path(self.data_cross, self.path, self.id2index[cross_idStart],self.id2index[cross_idEnd])
						self.flag2 = 1
				else:
					min_path = shortest_path(self.data_cross, self.path, self.id2index[cross_idStart], self.id2index[cross_idEnd])
				road_data = list()
				for j in range(len(min_path) - 1):
					self.crossIds = min_path[j] + '_' + min_path[j + 1]
					if self.crossIds in self.use_roadNum.keys():
						self.use_roadNum[self.crossIds] += 1
					else:
						self.use_roadNum[self.crossIds] = 0
					if self.use_roadNum[self.crossIds] > block_road:
						self.path, self.id2index = floyd(self.data_road, self.data_cross, self.crossIds, self.flag, self.flag3)
						self.use_roadNum[self.crossIds] = 0
					road_data.append(self.crossId2roadId[self.crossIds])
				road_ids = ''
				for k in range(len(road_data) - 1):
					road_ids += road_data[k].roadId + ','
				road_ids += road_data[-1].roadId
				if car.preset == 1 and self.flag2 == 1:
					result = str('(' + car.carId + ',' + str(car.planTime) + ',' + road_ids + ')')
					self.flag2 = 0
				elif car.preset == 1:
					continue
				else:
					result = str('(' + car.carId + ',' + str(car.planTime + i) + ',' + road_ids + ')')
				results += str(result) + '\n'
		return results



