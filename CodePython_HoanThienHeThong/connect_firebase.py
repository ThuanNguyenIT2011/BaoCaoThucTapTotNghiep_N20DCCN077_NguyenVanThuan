from firebase_admin import db, credentials
import firebase_admin

class FireBaseConnect:
    def __init__(self) -> None:
        self.cred = credentials.Certificate("credentials.json")
        self.app = firebase_admin.initialize_app(self.cred, {"databaseURL": "https://nhanthongminh-9fb6f-default-rtdb.asia-southeast1.firebasedatabase.app/"})
        self.ref = db.reference("/")

        self.arr_info_key_sensor = ['Gas', 'Humidity', 'Temperature'] 

    def get_data_by_key(self, key):
        return db.reference(key).get()

    def get_data_sensor(self):
        gas = db.reference('Gas').get()
        h = db.reference('Humidity').get()
        t = db.reference('Temperature').get()
        return {"Gas": gas, "Humidity": h, "Temperature": t}
    
    def update_node_by_key(self, key, value):
        db.reference('/').update({key: value})

# test1 = FireBaseConnect()
# print(test1.get_data_sensor()['Gas'])
# test1.update_node_by_key('predict_door', True)