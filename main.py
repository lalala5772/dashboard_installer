import sys
import serial
import schedule
import time
from datetime import datetime
from multiprocessing import Process, Lock
import pymysql
import cv2
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
        

#로컬 db에 저장하는 코드
def dbsaver(imageUrl):
    data = sensorData()
    
    sensordb = pymysql.connect(
    user='root',
    passwd='1234',
    host='localhost',
    db='dataDB'
    )
    
    cursor = sensordb.cursor(pymysql.cursors.DictCursor)

    
    try:
        sql = "INSERT INTO sensor(date, soilMoist, temperature, state, imageUrl) VALUES(DEFAULT, %s, %s, %s, %s)"
        val = (float(data[0]), float(data[1]), data[2], imageUrl)
        cursor.execute(sql, val)
    
        sensordb.commit()
    
    finally:
        sensordb.close()
        print(data)


        

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

    dbsaver(output_path)



    
    
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

