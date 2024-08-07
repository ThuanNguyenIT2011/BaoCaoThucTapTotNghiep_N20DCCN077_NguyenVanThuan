from connect_firebase_img import FireBaseImage
from  connect_firebase import FireBaseConnect
from gas import ModelGas

import ModelImage

import time

import logging
import threading

connect_data = FireBaseConnect()
connect_data_img = FireBaseImage()
model_gas = ModelGas()

def predict_person():
    path = connect_data_img.get_image_last()
    print(f'Path {path}')
    if path != None:
        label = ModelImage.predict_image(path)
        print(label)
        connect_data.update_node_by_key('predict_door', label)
        if(label == True):
            time.sleep(5)
        time.sleep(1)


def predict_fire():
    data_sensor = connect_data.get_data_sensor()
    gas = data_sensor['Gas']
    h = data_sensor['Humidity']
    t = data_sensor['Temperature']
    result = model_gas.predict(gas, h, t)
    print(result)
    connect_data.update_node_by_key('predict_fire', result)

def task_predict_person():
    while True:
        predict_person()
        time.sleep(1)

def task_predict_fire():
    while True:
        predict_fire()
        time.sleep(1)


task1_predict_person = threading.Thread(target=task_predict_person, args=())
task2_predict_fire = threading.Thread(target=task_predict_fire, args=())

task1_predict_person.start()
task2_predict_fire.start()

# predict_fire()
# predict_person()
