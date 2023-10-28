import sys
import serial
import schedule
import time
from datetime import datetime
from multiprocessing import Process, Lock
import pymysql
import cv2
import requests
import json

#import numpy as np


#Arduino
PORT = '/dev/ttyACM0'
BaudRate = 9600

ARD= serial.Serial(PORT,BaudRate)
    

def sensorData():
    time.sleep(0.1)

    Data = ARD.readline().decode()

    DataList = Data.split(',')

    return DataList


def dbsaver():
    # sensor_value = sensorData()
    # sensor_key = [ 'soilMoist', 'temperature']
    #sensor_data = zip(sensor_key, sensor_data)

    url = "http://15.164.90.233:7077/create/sensor_data"
    sensor_data = {"soilMoist": 29.9, "temperature": 24, }
    headers = {'Content-Type': 'application/json'}
    data_str = json.dumps(sensor_data, default=str)

    ## 생성 시에는 POST 를 사용함
    response = requests.post(url, data = data_str, headers = headers)

    if response.status_code == 200:
        print("OK")
    else:
        print("Error")


    


    






        

def exit():
    sys.exit()

def take_Pic():

    cap = cv2.VideoCapture(0) 

    ret, frame = cap.read()  

    if ret:
        now = datetime.now()
        output_path = 'images/'  + now.strftime('%Y-%m-%d_%H:%M:%S') + '.jpg'
    
        cv2.imwrite(output_path, frame)
        print(f"Captured image saved at {output_path}")
    else:
        print("Failed to capture image")

    cap.release()
    cv2.destroyAllWindows()

    # dbsaver(output_path) 
    dbsaver()



    
    
def auto_Cam():
    schedule.every().day.at("08:00").do(take_Pic)
    schedule.every().day.at("13:00").do(take_Pic)
    schedule.every().day.at("18:00").do(take_Pic)


    while True:
        schedule.run_pending()
        time.sleep(1)


    
if __name__ == '__main__':
 
    data_process = Process(target = auto_Cam)
        
    data_process.start()
        
    data_process.join()

