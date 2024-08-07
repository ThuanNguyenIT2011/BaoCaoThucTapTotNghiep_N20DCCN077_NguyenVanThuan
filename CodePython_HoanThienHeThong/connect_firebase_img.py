import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import storage
import os

class FireBaseImage:
    def __init__(self) -> None:
        self.cred = credentials.Certificate("credentials.json")
        self.app = firebase_admin.initialize_app(self.cred, {
            'storageBucket': 'nhanthongminh-9fb6f.appspot.com',
        }, name='storage')

        self.db = firestore.client(app=self.app) 
        self.bucket = storage.bucket(app=self.app)
        self.folder_path = "data/"

    def get_image_blobs(self):
        blobs = self.bucket.list_blobs(prefix=self.folder_path)
        return blobs
    
    def get_image_last(self):
        images_col = self.bucket.list_blobs(prefix=self.folder_path)
        images_list = sorted(list(images_col), key=lambda blob: blob.updated, reverse=True)
        print(images_list[0])
        latest_blob = images_list[0] if images_list else None
        str_name = None
        if latest_blob:
            latest_image_url = latest_blob.public_url
            str_name = latest_blob.public_url.split('/')[-1]

        images_col = self.bucket.list_blobs(prefix=self.folder_path)
        
        for blob in images_col:
            name_file = blob.name
            image_name = name_file.split('/')[-1]
            print(image_name)

            if image_name == str_name:
                image_path = os.path.join('datalocal', image_name)
                blob.download_to_filename(image_path)
                # print(image_path)
                return image_path
        return str_name 

# test = FireBaseImage()
# print(test.get_image_last())
