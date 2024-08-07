import tensorflow as tf
import numpy as np

print(tf.__version__)
class ModelGas:
    def __init__(self) -> None:
        self.name_model = 'gas_mode_ann.h5'
        self.labels = ['No Fire', 'Fire']

        self.model = tf.keras.models.load_model(self.name_model)

    def predict(self, gas, h, t):
        gas = gas - 200
        input_data = np.array([[gas, h, t]])
        result = self.model.predict(input_data)
        idx = 1 if result[0][0] > 0.5 else 0
        return self.labels[idx] == 'Fire'
