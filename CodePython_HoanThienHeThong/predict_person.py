from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf # type: ignore

import facenet
import imutils # type: ignore
import os
import sys
import math
import pickle
import align.detect_face
import numpy as np
import cv2 # type: ignore
import collections
from sklearn.svm import SVC # type: ignore

class ModelPredictPerson:
    def __init__(self) -> None:
        self.MINSIZE = 20
        self.THRESHOLD = [0.6, 0.7, 0.7]
        self.FACTOR = 0.709
        self.IMAGE_SIZE = 182
        self.INPUT_IMAGE_SIZE = 160
        self.CLASSIFIER_PATH = 'Models/facemodel.pkl'
        self.FACENET_MODEL_PATH = 'Models/20180402-114759.pb'

        with open(self.CLASSIFIER_PATH, 'rb') as file:
            self.model, self.class_names = pickle.load(file)
        print("Custom Classifier, Successfully loaded")

        with tf.Graph().as_default():
            # Cai dat GPU neu co
            self.gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.6)
            self.sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=self.gpu_options, log_device_placement=False))

            with self.sess.as_default():
                # Load the model
                print('Loading feature extraction model')
                facenet.load_model(self.FACENET_MODEL_PATH)

                # Get input and output tensors
                self.images_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("input:0")
                self.embeddings = tf.compat.v1.get_default_graph().get_tensor_by_name("embeddings:0")
                self.phase_train_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("phase_train:0")
                self.embedding_size = self.embeddings.get_shape()[1]

                self.pnet, self.rnet, self.onet = align.detect_face.create_mtcnn(self.sess, "align")

                self.people_detected = set()
                self.person_detected = collections.Counter()

    def predict_image(self, IMAGE_PATH):
        frame = cv2.imread(IMAGE_PATH)
        frame = imutils.resize(frame, width=600)

        # frame = cv2.flip(frame, 1)

        bounding_boxes, _ = align.detect_face.detect_face(frame, self.MINSIZE, self.pnet, self.rnet, self.onet, self.THRESHOLD, self.FACTOR)

        faces_found = bounding_boxes.shape[0]

        try:
            if faces_found > 1:
                cv2.putText(frame, "Only one face", (0, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                            1, (255, 255, 255), thickness=1, lineType=2)
                return False
            elif faces_found > 0:
                det = bounding_boxes[:, 0:4]
                bb = np.zeros((faces_found, 4), dtype=np.int32)
                print(bb)
                for i in range(faces_found):
                    bb[i][0] = det[i][0]
                    bb[i][1] = det[i][1]
                    bb[i][2] = det[i][2]
                    bb[i][3] = det[i][3]
                    # print(bb[i][3]-bb[i][1])
                    # print(frame.shape[0])
                    # print((bb[i][3]-bb[i][1])/frame.shape[0])
                    if (bb[i][3]-bb[i][1])/frame.shape[0]>0.25:
                        cropped = frame[bb[i][1]:bb[i][3], bb[i][0]:bb[i][2], :]
                        scaled = cv2.resize(cropped, (self.INPUT_IMAGE_SIZE, self.INPUT_IMAGE_SIZE),
                                            interpolation=cv2.INTER_CUBIC)
                        scaled = facenet.prewhiten(scaled)
                        scaled_reshape = scaled.reshape(-1, self.INPUT_IMAGE_SIZE, self.INPUT_IMAGE_SIZE, 3)
                        feed_dict = {images_placeholder: scaled_reshape, phase_train_placeholder: False}
                        emb_array = self.sess.run(self.embeddings, feed_dict=feed_dict)

                        predictions = self.model.predict_proba(emb_array)
                        best_class_indices = np.argmax(predictions, axis=1)
                        best_class_probabilities = predictions[
                            np.arange(len(best_class_indices)), best_class_indices]
                        best_name = self.class_names[best_class_indices[0]]
                        print("Name: {}, Probability: {}".format(best_name, best_class_probabilities))

                        if best_class_probabilities > 0.8:
                            return True
                        else:
                            return False
                    else:
                        return False
            else:
                return False
        except:
            return False

test1 = ModelPredictPerson()
print(test1.predict_image('photo40.jpg'))