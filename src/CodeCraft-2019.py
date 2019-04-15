import time
start_time=time.time()

import logging
import sys

from manage4 import Manage
from load_save_data import *

# logging.basicConfig(level=logging.DEBUG,
#                     filename='../logs/CodeCraft-2019.log',
#                     format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     filemode='a')




def main():
    if len(sys.argv) != 6:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    preset_answer_path = sys.argv[4]
    answer_path = sys.argv[5]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("preset_answer_path is %s" % (preset_answer_path))
    logging.info("answer_path is %s" % (answer_path))

    data_car, data_road, data_cross = load_data(car_path, road_path, cross_path)
    data_preset, preset_time = load_preset(preset_answer_path)
    # process

    manage = Manage(data_car, data_road, data_cross, data_preset, preset_time)
    results = manage.running()

    # to write output file
    save_data(answer_path, results)

if __name__ == "__main__":
    main()
    end_time = time.time()
    print(int(end_time - start_time),'s')